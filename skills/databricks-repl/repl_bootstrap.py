"""
Bootstrap helpers injected into the Databricks REPL on session start.

All functions are available in every command — no imports needed.
"""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed


def sub_llm(prompt, endpoint="default-llm-endpoint", max_tokens=1024,
            system="", temperature=0.0):
    """Single recursive LM call via a Databricks serving endpoint.

    Pure text-in/text-out, no tools, no retry logic.
    """
    import urllib.request
    import urllib.error

    token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()  # pyright: ignore[reportUndefinedVariable] # noqa: F821
    host = spark.conf.get("spark.databricks.workspaceUrl")  # pyright: ignore[reportUndefinedVariable] # noqa: F821

    url = f"https://{host}/serving-endpoints/{endpoint}/invocations"

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    return body["choices"][0]["message"]["content"]


def sub_llm_batch(prompts, endpoint="default-llm-endpoint", max_tokens=1024,
                  system="", temperature=0.0, max_workers=8):
    """Parallel recursive LM calls using a thread pool.

    Returns results in the same order as the input prompts.
    """
    def _call(index, prompt):
        return index, sub_llm(
            prompt,
            endpoint=endpoint,
            max_tokens=max_tokens,
            system=system,
            temperature=temperature,
        )

    collected = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [
            pool.submit(_call, i, p) for i, p in enumerate(prompts)
        ]
        for future in as_completed(futures):
            idx, result = future.result()
            collected[idx] = result

    return [collected[i] for i in range(len(prompts))]
