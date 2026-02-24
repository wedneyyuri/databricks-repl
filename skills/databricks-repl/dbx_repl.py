"""
Databricks RLM REPL — CLI wrapper.

Manages session lifecycle, command execution, output capture,
step tracking, and eviction detection. All output is JSON to stdout.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

PREVIEW_MAX = 200


# ---------------------------------------------------------------------------
# SDK helpers (lazy import)
# ---------------------------------------------------------------------------

def _get_workspace_client(profile=None):
    """Create a WorkspaceClient with optional profile. Lazy SDK import."""
    try:
        from databricks.sdk import WorkspaceClient
    except ImportError:
        _error_exit(
            "AuthError",
            "databricks-sdk is not installed. Run: pip install databricks-sdk",
        )
    kwargs = {}
    if profile:
        kwargs["profile"] = profile
    return WorkspaceClient(**kwargs)


def _error_exit(error_type, message):
    """Print a JSON error to stdout and exit."""
    print(json.dumps({"status": error_type, "message": message}))
    sys.exit(1)


# ---------------------------------------------------------------------------
# File I/O helpers (immutable patterns)
# ---------------------------------------------------------------------------

def _read_json(path):
    """Read a JSON file and return its contents."""
    with open(path) as f:
        return json.load(f)


def _write_json(path, data):
    """Write data as formatted JSON to a file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def _write_text(path, content):
    """Write text content to a file."""
    with open(path, "w") as f:
        f.write(content)


def _now_iso():
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _preview(text, max_len=PREVIEW_MAX):
    """Return a truncated preview of text."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def _resolve_paths(project_dir):
    """Resolve session.json and repl_outputs paths from project dir."""
    base = Path(project_dir)
    return {
        "project_dir": str(base),
        "session_file": str(base / "session.json"),
        "output_dir": str(base / "repl_outputs"),
    }


def _load_session(paths):
    """Load session.json or exit with NoSession error."""
    session_file = paths["session_file"]
    if not os.path.exists(session_file):
        _error_exit("NoSession", f"No session.json found in {paths['project_dir']}. Run 'create' first.")
    return _read_json(session_file)


def _set_active_command(paths, active_command):
    """Persist active_command to session.json (transient field during execution)."""
    session = _read_json(paths["session_file"])
    _write_json(paths["session_file"], {**session, "active_command": active_command})


def _clear_active_command(paths):
    """Remove active_command from session.json."""
    session = _read_json(paths["session_file"])
    cleared = {k: v for k, v in session.items() if k != "active_command"}
    _write_json(paths["session_file"], cleared)


def _step_prefix(step, tag):
    """Build the zero-padded step prefix like '003_train'."""
    return f"{step:03d}_{tag}"


def _highest_existing_step(output_dir):
    """Scan repl_outputs/ for .cmd.py files and return the highest step number found."""
    if not os.path.isdir(output_dir):
        return 0
    highest = 0
    for name in os.listdir(output_dir):
        if name.endswith(".cmd.py") and len(name) >= 4 and name[:3].isdigit():
            try:
                step_num = int(name[:3])
                if step_num > highest:
                    highest = step_num
            except ValueError:
                pass
    return highest


# ---------------------------------------------------------------------------
# Bootstrap injection
# ---------------------------------------------------------------------------

def _read_bootstrap():
    """Read repl_bootstrap.py from the same directory as this script."""
    bootstrap_path = Path(__file__).parent / "repl_bootstrap.py"
    if not bootstrap_path.exists():
        _error_exit("ConfigError", f"repl_bootstrap.py not found at {bootstrap_path}")
    with open(bootstrap_path) as f:
        return f.read()


# ---------------------------------------------------------------------------
# Databricks execution helpers
# ---------------------------------------------------------------------------

def _create_context(client, cluster_id):
    """Create an execution context on the cluster."""
    try:
        from databricks.sdk.service.compute import Language
        ctx = client.command_execution.create(
            cluster_id=cluster_id,
            language=Language.PYTHON,
        ).result()
        return ctx.id
    except Exception as e:
        msg = str(e)
        if "TERMINATED" in msg or "not running" in msg.lower():
            _error_exit("ClusterNotRunning", f"Cluster {cluster_id} is not running. Start it first.")
        if "limit" in msg.lower() and "context" in msg.lower():
            _error_exit("ContextLimitReached", "145 execution context limit reached. Destroy unused sessions.")
        raise


def _destroy_context(client, cluster_id, context_id):
    """Destroy an execution context. Ignores already-gone contexts."""
    try:
        client.command_execution.destroy(
            cluster_id=cluster_id,
            context_id=context_id,
        )
    except Exception:
        pass


def _submit_command(client, cluster_id, context_id, code):
    """Submit code for execution without blocking. Returns (wait, command_id).

    The returned wait object can be polled with _await_command().
    Raises _EvictedException if the context was evicted during submit.
    """
    try:
        from databricks.sdk.service.compute import Language
    except ImportError:
        _error_exit("AuthError", "databricks-sdk is not installed.")

    try:
        wait = client.command_execution.execute(
            cluster_id=cluster_id,
            context_id=context_id,
            language=Language.PYTHON,
            command=code,
        )
        return wait, wait.command_id
    except Exception as e:
        if _is_eviction_error(e):
            raise _EvictedException(str(e))
        raise


def _await_command(wait, timeout=600):
    """Block until the submitted command completes. Returns the SDK result object.

    Raises _EvictedException if the context was evicted while waiting.
    """
    try:
        return wait.result(timeout=timedelta(seconds=timeout))
    except TimeoutError:
        raise
    except Exception as e:
        if _is_eviction_error(e):
            raise _EvictedException(str(e))
        raise


def _poll_command_status(client, cluster_id, context_id, command_id, timeout=600):
    """Re-poll an already-submitted command until it finishes. Returns the SDK result.

    Used by 'await' to resume waiting after a previous timeout.
    Raises TimeoutError if still running, _EvictedException if evicted.
    """
    try:
        return client.command_execution.wait_command_status_command_execution_finished_or_error(
            cluster_id=cluster_id,
            command_id=command_id,
            context_id=context_id,
            timeout=timedelta(seconds=timeout),
        )
    except TimeoutError:
        raise
    except Exception as e:
        if _is_eviction_error(e):
            raise _EvictedException(str(e))
        raise


def _execute_command(client, cluster_id, context_id, code, timeout=600):
    """Execute code in the context and block until done. Returns the SDK result object.

    Convenience wrapper around _submit_command + _await_command.
    Raises _EvictedException if the context was evicted.
    """
    wait, _ = _submit_command(client, cluster_id, context_id, code)
    return _await_command(wait, timeout=timeout)


def _is_eviction_error(exc):
    """Check if an exception indicates context eviction."""
    msg = str(exc).lower()
    indicators = [
        "resource does not exist",
        "resourcedoesnotexist",
        "invalid parameter value",
        "invalidparametervalue",
        "no such execution context",
    ]
    return any(ind in msg for ind in indicators)


class _EvictedException(Exception):
    """Raised when the execution context has been evicted."""


# ---------------------------------------------------------------------------
# Eviction recovery
# ---------------------------------------------------------------------------

def _handle_eviction(client, session, paths):
    """Create fresh context, re-inject bootstrap, return eviction response."""
    cluster_id = session["cluster_id"]

    new_context_id = _create_context(client, cluster_id)

    bootstrap_code = _read_bootstrap()
    _execute_command(client, cluster_id, new_context_id, bootstrap_code)

    updated_session = {
        **session,
        "context_id": new_context_id,
        "eviction_count": session.get("eviction_count", 0) + 1,
        "last_eviction_at": _now_iso(),
    }
    _write_json(paths["session_file"], updated_session)

    previous_steps = [
        {
            "step": step["step"],
            "tag": step["tag"],
            "command_file": step["command_file"],
        }
        for step in session.get("steps", [])
    ]

    return {
        "status": "ContextEvicted",
        "message": "Execution context was evicted. Fresh context created. Replay needed.",
        "new_context_id": new_context_id,
        "project_dir": paths["project_dir"],
        "previous_steps": previous_steps,
    }


# ---------------------------------------------------------------------------
# Subcommand: create
# ---------------------------------------------------------------------------

def cmd_create(args):
    """Create a new REPL session."""
    client = _get_workspace_client(args.profile)
    paths = _resolve_paths(args.project_dir)

    existing_steps = []
    if os.path.exists(paths["session_file"]):
        existing = _read_json(paths["session_file"])
        if existing.get("status") != "destroyed":
            _error_exit(
                "SessionExists",
                f"Active session already exists in {paths['project_dir']}. "
                "Destroy it first or use a different --project-dir.",
            )
        existing_steps = existing.get("steps", [])

    context_id = _create_context(client, args.cluster_id)

    bootstrap_code = _read_bootstrap()
    _execute_command(client, args.cluster_id, context_id, bootstrap_code)

    os.makedirs(paths["output_dir"], exist_ok=True)

    starting_step = _highest_existing_step(paths["output_dir"])

    session = {
        "status": "active",
        "cluster_id": args.cluster_id,
        "context_id": context_id,
        "session_name": args.session_name,
        "step_counter": starting_step,
        "created_at": _now_iso(),
        "profile": args.profile,
        "steps": existing_steps,
    }
    _write_json(paths["session_file"], session)

    print(json.dumps({
        "status": "created",
        "project_dir": paths["project_dir"],
        "session_file": paths["session_file"],
        "cluster_id": args.cluster_id,
        "context_id": context_id,
        "output_dir": paths["output_dir"],
    }))


# ---------------------------------------------------------------------------
# Subcommand: exec
# ---------------------------------------------------------------------------

def _build_running_response(cmd_id, command_id, elapsed, timeout, project_dir):
    """Build the structured Running response with actionable tip."""
    return {
        "cmd_id": cmd_id,
        "status": "Running",
        "command_id": command_id,
        "elapsed_seconds": elapsed,
        "message": f"Command still running after {timeout}s client-side timeout.",
        "tip": {
            "await": f"dbx_repl.py await --timeout 600 --project-dir {project_dir}",
            "cancel": f"dbx_repl.py cancel --project-dir {project_dir}",
        },
    }


def _cancel_and_finalize(client, session, paths, command_id,
                          new_step, tag, stdout_file, stderr_file,
                          cmd_file, started_at, start_time):
    """Cancel a remote command, finalize step as Cancelled, and print response."""
    try:
        client.command_execution.cancel(
            cluster_id=session["cluster_id"],
            context_id=session["context_id"],
            command_id=command_id,
        )
    except Exception:
        pass
    _clear_active_command(paths)
    elapsed = round(time.monotonic() - start_time, 1)
    response = _finalize_exec(
        paths, new_step, tag, session["session_name"],
        "Cancelled", stdout_file, stderr_file, "", "",
        cmd_file, started_at, elapsed,
    )
    print(json.dumps({**response, "message": "Command interrupted by user."}))


def _finalize_exec(paths, new_step, tag, session_name, status_str,
                    stdout_file, stderr_file, raw_stdout, raw_stderr,
                    cmd_file, started_at, elapsed):
    """Write output files, record step in session.json, clear active_command.

    Returns the response dict.
    """
    _write_text(stdout_file, raw_stdout)
    _write_text(stderr_file, raw_stderr)

    finished_at = _now_iso()
    stdout_bytes = len(raw_stdout.encode("utf-8"))
    stderr_bytes = len(raw_stderr.encode("utf-8"))

    is_error = status_str.lower() in ("error", "cancelled")

    response = {
        "cmd_id": _step_prefix(new_step, tag),
        "status": status_str,
        "stdout_file": stdout_file,
        "stderr_file": stderr_file,
        "stdout_bytes": stdout_bytes,
        "stderr_bytes": stderr_bytes,
        "elapsed_seconds": elapsed,
    }

    if is_error and stderr_bytes > 0:
        response["stderr_preview"] = _preview(raw_stderr)
    elif stdout_bytes > 0:
        response["stdout_preview"] = _preview(raw_stdout)

    current_session = _read_json(paths["session_file"])
    step_entry = {
        "step": new_step,
        "tag": tag,
        "session_name": session_name,
        "status": status_str,
        "command_file": cmd_file,
        "started_at": started_at,
        "finished_at": finished_at,
        "elapsed_seconds": elapsed,
    }
    cleared = {k: v for k, v in current_session.items() if k != "active_command"}
    updated_session = {
        **cleared,
        "steps": cleared.get("steps", []) + [step_entry],
    }
    _write_json(paths["session_file"], updated_session)

    return response


def cmd_exec(args):
    """Execute Python code in the REPL."""
    paths = _resolve_paths(args.project_dir)
    session = _load_session(paths)

    if session.get("status") == "destroyed":
        _error_exit("NoSession", "Session has been destroyed. Run 'create' first.")

    client = _get_workspace_client(session.get("profile") or args.profile)

    command = args.command
    if command.startswith("@"):
        filepath = command[1:]
        if not os.path.exists(filepath):
            _error_exit("FileNotFound", f"Command file not found: {filepath}")
        with open(filepath) as f:
            command = f.read()

    new_step = session["step_counter"] + 1
    prefix = _step_prefix(new_step, args.tag)
    cmd_file = os.path.join(paths["output_dir"], f"{prefix}.cmd.py")
    stdout_file = os.path.join(paths["output_dir"], f"{prefix}.stdout")
    stderr_file = os.path.join(paths["output_dir"], f"{prefix}.stderr")

    _write_text(cmd_file, command)

    updated_session = {
        **session,
        "step_counter": new_step,
    }
    _write_json(paths["session_file"], updated_session)

    # --- Submit (non-blocking) ---
    started_at = _now_iso()
    start_time = time.monotonic()

    try:
        wait, command_id = _submit_command(
            client,
            session["cluster_id"],
            session["context_id"],
            command,
        )
    except _EvictedException:
        eviction_response = _handle_eviction(client, session, paths)
        print(json.dumps(eviction_response))
        return

    # Persist active_command so cancel can auto-detect it from another terminal
    _set_active_command(paths, {
        "command_id": command_id,
        "step": new_step,
        "tag": args.tag,
        "started_at": started_at,
    })

    # --- Await (blocking) ---
    try:
        result = _await_command(wait, timeout=args.timeout)
    except _EvictedException:
        _clear_active_command(paths)
        eviction_response = _handle_eviction(client, session, paths)
        print(json.dumps(eviction_response))
        return
    except TimeoutError:
        elapsed = round(time.monotonic() - start_time, 1)
        response = _build_running_response(
            _step_prefix(new_step, args.tag), command_id,
            elapsed, args.timeout, paths["project_dir"],
        )
        print(json.dumps(response))
        return
    except KeyboardInterrupt:
        _cancel_and_finalize(
            client, session, paths, command_id,
            new_step, args.tag, stdout_file, stderr_file,
            cmd_file, started_at, start_time,
        )
        return

    raw_stdout = ""
    raw_stderr = ""

    if result.results:
        raw_stdout = result.results.data or ""
        if result.results.cause:
            raw_stderr = result.results.cause

    elapsed = round(time.monotonic() - start_time, 1)
    status_str = str(result.status.value) if result.status else "Unknown"

    response = _finalize_exec(
        paths, new_step, args.tag, session["session_name"],
        status_str, stdout_file, stderr_file, raw_stdout, raw_stderr,
        cmd_file, started_at, elapsed,
    )

    print(json.dumps(response))


# ---------------------------------------------------------------------------
# Subcommand: cancel
# ---------------------------------------------------------------------------

def cmd_cancel(args):
    """Cancel a running command."""
    paths = _resolve_paths(args.project_dir)
    session = _load_session(paths)

    command_id = args.run_id
    if not command_id:
        active = session.get("active_command")
        if not active:
            _error_exit("NothingToCancel", "No active command to cancel.")
        command_id = active["command_id"]

    client = _get_workspace_client(session.get("profile") or args.profile)

    try:
        client.command_execution.cancel(
            cluster_id=session["cluster_id"],
            context_id=session["context_id"],
            command_id=command_id,
        )
    except Exception as e:
        if _is_eviction_error(e):
            _error_exit("ContextEvicted", "Context was evicted. Cancel is no longer possible.")
        raise

    _clear_active_command(paths)

    print(json.dumps({
        "status": "cancelled",
        "command_id": command_id,
    }))


# ---------------------------------------------------------------------------
# Subcommand: await
# ---------------------------------------------------------------------------

def cmd_await(args):
    """Re-poll a running command that previously timed out."""
    paths = _resolve_paths(args.project_dir)
    session = _load_session(paths)

    active = session.get("active_command")
    if not active:
        _error_exit("NothingToAwait", "No active command to await.")

    command_id = active["command_id"]
    new_step = active["step"]
    tag = active["tag"]
    started_at = active["started_at"]

    prefix = _step_prefix(new_step, tag)
    stdout_file = os.path.join(paths["output_dir"], f"{prefix}.stdout")
    stderr_file = os.path.join(paths["output_dir"], f"{prefix}.stderr")
    cmd_file = os.path.join(paths["output_dir"], f"{prefix}.cmd.py")

    client = _get_workspace_client(session.get("profile") or args.profile)

    start_time = time.monotonic()

    try:
        result = _poll_command_status(
            client, session["cluster_id"], session["context_id"],
            command_id, timeout=args.timeout,
        )
    except TimeoutError:
        elapsed = round(time.monotonic() - start_time, 1)
        response = _build_running_response(
            prefix, command_id, elapsed, args.timeout, paths["project_dir"],
        )
        print(json.dumps(response))
        return
    except _EvictedException:
        _clear_active_command(paths)
        eviction_response = _handle_eviction(client, session, paths)
        print(json.dumps(eviction_response))
        return
    except KeyboardInterrupt:
        _cancel_and_finalize(
            client, session, paths, command_id,
            new_step, tag, stdout_file, stderr_file,
            cmd_file, started_at, start_time,
        )
        return

    raw_stdout = ""
    raw_stderr = ""
    if result.results:
        raw_stdout = result.results.data or ""
        if result.results.cause:
            raw_stderr = result.results.cause

    elapsed = round(time.monotonic() - start_time, 1)
    status_str = str(result.status.value) if result.status else "Unknown"

    response = _finalize_exec(
        paths, new_step, tag, session["session_name"],
        status_str, stdout_file, stderr_file, raw_stdout, raw_stderr,
        cmd_file, started_at, elapsed,
    )
    print(json.dumps(response))


# ---------------------------------------------------------------------------
# Subcommand: destroy
# ---------------------------------------------------------------------------

def cmd_destroy(args):
    """Destroy the execution context and finalize the session."""
    paths = _resolve_paths(args.project_dir)
    session = _load_session(paths)

    if session.get("status") == "destroyed":
        _error_exit("NoSession", "Session is already destroyed.")

    client = _get_workspace_client(session.get("profile") or args.profile)

    _destroy_context(client, session["cluster_id"], session["context_id"])

    updated_session = {
        **session,
        "status": "destroyed",
        "destroyed_at": _now_iso(),
    }
    _write_json(paths["session_file"], updated_session)

    steps = session.get("steps", [])

    print(json.dumps({
        "status": "destroyed",
        "steps_completed": len(steps),
        "session_file": paths["session_file"],
    }))


# ---------------------------------------------------------------------------
# CLI argument parser
# ---------------------------------------------------------------------------

def _build_parser():
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="dbx_repl",
        description="Databricks RLM REPL — stateful Python execution on Databricks",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common arguments added to each subparser
    def _add_common(sub):
        sub.add_argument(
            "--project-dir", default=".",
            help="Project root directory (default: cwd)",
        )
        sub.add_argument(
            "--profile", default=None,
            help="Databricks CLI profile name from ~/.databrickscfg",
        )
        sub.add_argument("--debug", action="store_true", help="Print SDK debug info to stderr")

    # create
    p_create = subparsers.add_parser("create", help="Create a new REPL session")
    _add_common(p_create)
    p_create.add_argument("--cluster-id", required=True, help="Databricks cluster ID")
    p_create.add_argument("--session-name", required=True, help="Human-readable session name")
    p_create.set_defaults(func=cmd_create)

    # exec
    p_exec = subparsers.add_parser("exec", help="Execute Python code in the REPL")
    _add_common(p_exec)
    p_exec.add_argument("--command", required=True, help="Python code (inline or @filepath)")
    p_exec.add_argument("--tag", required=True, help="Descriptive label for this step")
    p_exec.add_argument("--timeout", type=int, default=600, help="Max seconds to wait (default: 600)")
    p_exec.set_defaults(func=cmd_exec)

    # cancel
    p_cancel = subparsers.add_parser("cancel", help="Cancel a running command")
    _add_common(p_cancel)
    p_cancel.add_argument("--run-id", default=None, help="Command ID to cancel (auto-detected from active_command if omitted)")
    p_cancel.set_defaults(func=cmd_cancel)

    # await
    p_await = subparsers.add_parser("await", help="Re-poll a running command")
    _add_common(p_await)
    p_await.add_argument("--timeout", type=int, default=600, help="Max seconds to wait (default: 600)")
    p_await.set_defaults(func=cmd_await)

    # destroy
    p_destroy = subparsers.add_parser("destroy", help="Destroy the session")
    _add_common(p_destroy)
    p_destroy.set_defaults(func=cmd_destroy)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = _build_parser()
    args = parser.parse_args()

    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

    try:
        args.func(args)
    except _EvictedException as e:
        _error_exit("ContextEvicted", str(e))
    except KeyboardInterrupt:
        _error_exit("Interrupted", "Command interrupted by user.")
    except Exception as e:
        _error_exit("UnexpectedError", str(e))


if __name__ == "__main__":
    main()
