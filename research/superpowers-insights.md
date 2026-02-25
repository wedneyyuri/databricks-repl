# Superpowers Framework: Deep Research & Insights

**Repository:** https://github.com/obra/superpowers
**Author:** Jesse Vincent (@obra)
**Stars:** ~55K+ (as of Feb 2026)
**License:** MIT
**Version:** 4.3.1

---

## 1. What Problem Does Superpowers Solve?

Superpowers addresses the fundamental weakness of AI coding agents: **they rush to write code
without adequate planning, testing, or verification.** Left to their defaults, agents produce
code that looks plausible but is often poorly architected, untested, and fragile.

Superpowers transforms an AI agent from a code-generating autocomplete into a **methodical
software engineer** that:

- Plans before coding (brainstorming, design documents, implementation plans)
- Tests before implementing (strict TDD with RED-GREEN-REFACTOR)
- Verifies before claiming completion (evidence-based verification gates)
- Reviews its own work (two-stage code review: spec compliance + quality)
- Follows systematic debugging instead of guess-and-check

The core insight: **methodology beats raw intelligence.** A disciplined process produces
consistently better results than an undirected powerful model.

---

## 2. Architecture & Repository Structure

```
superpowers/
  .claude-plugin/        # Claude Code plugin manifest (plugin.json, marketplace.json)
  .cursor-plugin/        # Cursor plugin manifest
  .codex/                # Codex installation instructions
  .opencode/             # OpenCode installation instructions
  agents/                # Agent persona definitions
    code-reviewer.md     # Senior code reviewer agent definition
  commands/              # Slash command definitions
    brainstorm.md        # /brainstorm command
    write-plan.md        # /write-plan command
    execute-plan.md      # /execute-plan command
  hooks/                 # Session lifecycle hooks
    hooks.json           # Hook configuration (triggers on startup/resume/clear/compact)
    run-hook.cmd          # Cross-platform hook runner
    session-start        # Injects using-superpowers skill into every session
  lib/
    skills-core.js       # Core library: skill discovery, frontmatter parsing, shadowing
  skills/                # 14 composable skill definitions (each has SKILL.md)
    brainstorming/
    dispatching-parallel-agents/
    executing-plans/
    finishing-a-development-branch/
    receiving-code-review/
    requesting-code-review/
    subagent-driven-development/
    systematic-debugging/
    test-driven-development/
    using-git-worktrees/
    using-superpowers/
    verification-before-completion/
    writing-plans/
    writing-skills/
  tests/                 # Skill behavior validation tests
  docs/                  # Additional documentation
```

### Key Architectural Decisions

1. **Skills are markdown files (SKILL.md), not code.** Each skill is a natural-language
   document that teaches the agent a methodology. This is brilliant because it leverages
   the LLM's natural ability to follow instructions rather than requiring programmatic
   orchestration.

2. **Flat directory structure.** Each skill lives in its own directory with a required
   `SKILL.md` file. Supporting reference files can live alongside it, but the primary
   skill is always one markdown document.

3. **Session-start injection.** The `using-superpowers` skill is automatically loaded into
   every session via a hook. This acts as the "bootstrap" that teaches the agent to check
   for applicable skills before every response.

4. **Plugin manifest for distribution.** The `.claude-plugin/plugin.json` declares paths
   to skills/, agents/, commands/, and hooks/, enabling clean installation via
   `/plugin install`.

5. **Personal skill shadowing.** The `skills-core.js` library supports personal skills
   overriding superpowers skills (unless explicitly prefixed with `superpowers:`). This
   enables customization without forking.

6. **Commands are thin wrappers.** Each command (`/brainstorm`, `/write-plan`,
   `/execute-plan`) simply invokes the corresponding skill. The command files contain
   a one-line instruction: "Invoke the superpowers:X skill and follow it exactly."
   They also set `disable-model-invocation: true` to prevent the model from
   short-circuiting the skill.

---

## 3. How It Structures Prompts/Instructions for AI Agents

This is where Superpowers is most instructive. The prompting patterns are highly refined.

### 3.1 The "Iron Law" Pattern

Each discipline-enforcing skill has an absolute rule stated upfront in bold:
- TDD: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- Debugging: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
- Verification: "Evidence before claims, always"

These are non-negotiable, no-exceptions directives. They establish a bright line that the
agent cannot rationalize past.

### 3.2 The "Rationalization Table" Anti-Pattern Defense

This is perhaps the most innovative pattern. Skills explicitly list the internal
rationalizations an agent might generate to skip the process, then debunk each one:

| Rationalization | Counter |
|---|---|
| "This is just a simple question" | Tasks always warrant skill checks |
| "I need more context first" | Skills precede clarification |
| "The skill is overkill" | You cannot judge before invoking |
| "I'll test later" | Delete work and restart with TDD |
| "Tests after prove the same thing" | Tests-after prove nothing |

This is powerful because LLMs generate plausible-sounding excuses to skip steps.
By pre-listing and debunking them, the skill closes escape hatches.

### 3.3 The "Red Flag" Pattern

Skills list specific phrases that signal the agent is about to violate the process:
- "should work" / "probably passes" / "seems correct" (verification violations)
- "quick fix for now" / "probably X, let me fix that" (debugging violations)
- "Great!" / "Done!" before running tests (premature completion)

These act as tripwires in the agent's own reasoning.

### 3.4 The "Flowchart/Decision Tree" Pattern

Complex skills include explicit decision trees for the agent:
- "If tasks are tightly coupled -> use executing-plans, else -> use subagent-driven"
- "If worktree directory exists -> use it, else -> check CLAUDE.md, else -> ask user"

This prevents the agent from making arbitrary choices.

### 3.5 The "Checklist Gate" Pattern

Before marking work complete, skills require explicit checklists:
- Every new function has a test
- Each test failed for expected reasons before implementation
- Minimal code passes tests
- All tests pass cleanly
- Edge cases are covered

### 3.6 The "Rigid vs. Flexible" Classification

Skills self-declare their flexibility level:
- **Rigid skills** (TDD, debugging): Must follow exactly, no shortcuts
- **Flexible skills** (patterns): Allow contextual adaptation

This prevents agents from treating all guidance as optional.

### 3.7 The "Announce Before Acting" Pattern

Every skill requires the agent to announce its activation: "I'm using the
executing-plans skill to implement this plan." This makes the process transparent
to the user and creates accountability.

---

## 4. Context Management Patterns

### 4.1 Fresh Context via Subagents

The most significant context management strategy is **dispatching fresh subagents
per task.** Each implementation task gets a new agent with:
- The complete task description from the plan
- Full project context (via the codebase)
- No accumulated confusion from prior tasks

This solves the "context pollution" problem where agents accumulate wrong assumptions
over long sessions.

### 4.2 Session-Start Bootstrap

The hooks system ensures the `using-superpowers` skill is injected at session start,
resume, clear, and compact events. This means the agent always has the core "check
skills first" instruction in context, even after context resets.

### 4.3 Plans as External Memory

Implementation plans are saved to `docs/plans/YYYY-MM-DD-<feature-name>.md`. These
serve as persistent context that survives across sessions. A new session can pick up
where the previous one left off by loading the plan file.

### 4.4 Git Worktrees for Isolation

Each development task gets its own git worktree, providing:
- Clean test baselines (tests must pass before implementation starts)
- Isolation from other in-progress work
- Easy rollback (just delete the worktree)

### 4.5 Two-Stage Review with Separate Reviewers

After implementation, two separate review subagents are dispatched:
1. **Spec compliance reviewer** - checks against the plan
2. **Code quality reviewer** - evaluates engineering standards

Using separate agents prevents "rubber stamp" reviews where the same agent reviews
its own work.

---

## 5. Tool Orchestration Patterns

### 5.1 Skill Invocation via the Skill Tool

The core mechanism: the agent calls a `Skill` tool to load a skill definition. The
using-superpowers bootstrap instructs the agent to invoke skills "even if there's only
a 1% chance of applicability." This aggressive triggering ensures skills are never
accidentally bypassed.

### 5.2 Subagent Dispatch via the Task Tool

For parallel and delegated work, superpowers uses the `Task` tool to dispatch subagents.
Each subagent receives:
- Complete task context from the plan
- Which skills to follow (TDD, verification)
- Specific commit hashes for review scope

### 5.3 TodoWrite for Progress Tracking

Plans are tracked via `TodoWrite`, creating a persistent task list that the orchestrating
agent uses to manage multi-step execution.

### 5.4 Commands as Entry Points

Three slash commands (`/brainstorm`, `/write-plan`, `/execute-plan`) provide ergonomic
entry points for users. Each command is a thin wrapper that invokes the corresponding
skill, keeping the architecture clean.

### 5.5 Hook-Based Session Management

The hooks.json configuration triggers the session-start script on startup, resume,
clear, and compact events. The script reads the using-superpowers SKILL.md, escapes
it for JSON, and injects it as additional context. This ensures the bootstrap
instruction survives context management events.

---

## 6. Why It Gained Traction (55K+ Stars)

### 6.1 Solves a Real, Painful Problem
Every Claude Code / AI agent user has experienced: agents writing untested code,
skipping edge cases, rushing to implement without understanding requirements. Superpowers
directly addresses this universal pain point.

### 6.2 Zero Configuration Required
`/plugin install superpowers@superpowers-marketplace` -- one command, immediate value.
No Node.js dependency, no configuration files to edit, no environment variables.

### 6.3 Composable, Not Monolithic
Users can adopt individual skills incrementally. Use just TDD, or just brainstorming,
or the full workflow. Skills compose naturally because they reference each other by name.

### 6.4 Works Across Platforms
Supports Claude Code (native plugin), Cursor (plugin), Codex (symlinks), and OpenCode
(symlinks). This broad compatibility expanded the addressable user base significantly.

### 6.5 Dramatically Better Results
The structured methodology produces noticeably higher-quality code. Users report fewer
bugs, better test coverage, and more maintainable architectures. The improvement is
obvious enough to drive word-of-mouth adoption.

### 6.6 Transparent Process
The "announce before acting" pattern means users can see exactly what methodology the
agent is following. This builds trust and enables users to learn the methodology
themselves.

### 6.7 Community Extensibility
The `writing-skills` meta-skill teaches users how to create their own skills using the
same TDD-for-documentation approach. Personal skills can shadow framework skills. This
creates a virtuous cycle of community contribution.

### 6.8 Timing
Released as AI coding agents (Claude Code, Codex, Cursor) reached mainstream adoption.
Users were discovering the limitations of unstructured AI coding exactly when Superpowers
offered a solution.

---

## 7. Positioning vs. Built-in AI Features

Superpowers does not replace built-in AI features -- it **layers methodology on top**:

| Aspect | Built-in AI Agent | + Superpowers |
|---|---|---|
| Planning | Jumps to code | Brainstorm -> Design -> Plan -> Execute |
| Testing | Tests after (maybe) | Strict TDD: failing test first, always |
| Debugging | Guess and patch | 4-phase root cause analysis |
| Verification | "Should work" | Evidence-based: run command, read output |
| Review | None | Two-stage: spec compliance + quality |
| Context | Accumulates confusion | Fresh subagents per task |
| Parallelism | Sequential | Dispatch parallel agents per domain |

The key insight: **Superpowers enhances the agent's decision-making process, not its
capabilities.** The agent already has the tools (read files, write code, run tests).
Superpowers teaches it *when* and *how* to use them effectively.

---

## 8. Actionable Insights for the Databricks REPL Skill Project

Based on this research, here are specific patterns to apply to a Claude Code skill for
executing Python on Databricks clusters:

### 8.1 Skill Structure

Follow the SKILL.md convention:
- YAML frontmatter with `name` and `description` (description states triggering
  conditions, not process summary)
- Maximum 1024 characters for frontmatter
- Inline patterns and principles; externalize heavy reference material

```yaml
---
name: databricks-repl
description: "Use when executing Python code on remote Databricks clusters, running
notebooks, querying data, or managing cluster state."
---
```

### 8.2 Apply the "Iron Law" Pattern

Define a non-negotiable rule for the Databricks REPL skill:
- "NEVER execute destructive operations (DROP, DELETE, TRUNCATE) without explicit user
  confirmation"
- "ALWAYS verify cluster state before submitting jobs"
- "ALWAYS capture and display full error output, never summarize"

### 8.3 Apply the "Rationalization Table" Pattern

Pre-list and debunk agent rationalizations:

| Rationalization | Counter |
|---|---|
| "I'll just run this query directly" | Check cluster state first |
| "The error is probably a timeout" | Read the full error message |
| "I can fix this by retrying" | Diagnose the root cause |
| "The cluster is probably running" | Verify with an API call |

### 8.4 Apply the "Checklist Gate" Pattern

Before reporting results to the user:
- Verify the execution completed (check job status)
- Verify the output is complete (not truncated)
- Verify no errors were suppressed
- Present results with execution metadata (cluster, runtime, rows returned)

### 8.5 Apply the "Announce Before Acting" Pattern

The skill should instruct the agent to announce: "I'm using the databricks-repl
skill to execute this on cluster X" before any execution. This creates transparency.

### 8.6 Context Management for Long-Running Jobs

Borrow the "plans as external memory" pattern:
- For long-running jobs, write status to a tracking file
- For multi-step workflows, maintain a plan document
- Use TodoWrite to track multi-step data pipeline executions

### 8.7 Error Handling Inspired by Systematic Debugging

Apply the 4-phase debugging model to Databricks errors:
1. Read the full error (not just the last line)
2. Check cluster state, library versions, permissions
3. Form a hypothesis about root cause
4. Fix with minimal change, verify with re-execution

### 8.8 Fresh Context for Complex Workflows

For multi-step Databricks workflows (ETL pipelines, ML training), consider the
subagent pattern: dispatch a fresh agent per pipeline step with explicit context
about what was produced by the prior step.

### 8.9 Verification Before Completion

Apply the verification-before-completion pattern:
- Never say "query completed successfully" without showing actual results
- Never say "cluster is ready" without checking cluster state
- Never say "data was written" without a count/confirmation query

### 8.10 Plugin Manifest Structure

Follow the proven plugin.json structure:

```json
{
  "name": "databricks-repl",
  "description": "Execute Python on Databricks clusters with safety, verification, and result presentation",
  "version": "1.0.0",
  "skills": "./skills/",
  "commands": "./commands/",
  "hooks": "./hooks/hooks.json"
}
```

### 8.11 Command Design

Create thin command wrappers following the superpowers pattern:
- `/databricks-run` -- Invoke the execution skill
- `/databricks-status` -- Check cluster and job state
- `/databricks-connect` -- Establish cluster connection

Each command: one line invoking the skill, `disable-model-invocation: true`.

### 8.12 Session-Start Hook

Inject the Databricks REPL skill context at session start so the agent always knows
about Databricks capabilities. Include:
- Current cluster configuration
- Available databases/catalogs
- Connection state

---

## 9. Key Takeaways

1. **Skills are markdown, not code.** Natural language instructions leveraging LLM
   comprehension are more powerful than programmatic orchestration for guiding agent
   behavior.

2. **Close the rationalization loopholes.** LLMs are excellent at generating plausible
   reasons to skip steps. Explicitly listing and debunking these is the single most
   impactful prompting technique in the framework.

3. **Process before capability.** The agent already has tools. Teaching it *when* to use
   them matters more than giving it new tools.

4. **Fresh context beats accumulated context.** Subagent dispatch per task produces
   better results than a single long session.

5. **Verification is non-negotiable.** Every claim must be backed by evidence from an
   actual command execution.

6. **Composability over monoliths.** 14 small, focused skills that reference each other
   beat one massive instruction document.

7. **The bootstrap pattern is essential.** A session-start hook that injects the
   "always check for skills" instruction ensures the system works without user
   intervention.

8. **Distribution matters.** One-command installation via plugin marketplace drove
   adoption. Make installation frictionless.

---

*Research conducted: 2026-02-25*
*Sources: GitHub repository analysis, release notes, community coverage, skill definitions*
