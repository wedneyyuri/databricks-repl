# Bootstrap Helpers

Functions injected into the Databricks REPL on session start via the bootstrap module. These are available in every command — no imports needed.

## Table of Contents

- [sub_llm()](#sub_llm) — Single recursive LM call
- [sub_llm_batch()](#sub_llm_batch) — Parallel recursive LM calls

---

## sub_llm()

Single recursive LM call via a Databricks serving endpoint. This is the RLM depth=1 pattern: pure text-in/text-out, no tools, no retry logic.

```python
sub_llm(
    prompt: str,
    endpoint: str = "default-llm-endpoint",
    max_tokens: int = 1024,
    system: str = "",
    temperature: float = 0.0
) -> str
```

**Example — summarization:**

```python
summary = sub_llm(
    f"Summarize the key findings:\n\n{report_text}",
    max_tokens=512
)
print(summary)
```

**Example — classification:**

```python
label = sub_llm(
    f"Classify this text as 'positive', 'negative', or 'neutral'. "
    f"Reply with only the label.\n\n{text}",
    temperature=0.0
)
```

**Notes:**
- Calls stay inside the Databricks cluster (serving endpoint)
- Blocking — the REPL waits for the response
- No tools attached to the sub-LM — pure text completion
- Use `sub_llm_batch()` for parallel calls over multiple inputs

---

## sub_llm_batch()

Parallel recursive LM calls using a thread pool. For map operations over partitioned data.

```python
sub_llm_batch(
    prompts: list[str],
    endpoint: str = "default-llm-endpoint",
    max_tokens: int = 1024,
    system: str = "",
    temperature: float = 0.0,
    max_workers: int = 8
) -> list[str]
```

**Example — partition + map pattern:**

```python
chunks = [rows[i:i+500] for i in range(0, len(rows), 500)]
prompts = [
    f"Classify each row as 'entity', 'description', or 'other'.\n\n{chunk}"
    for chunk in chunks
]
results = sub_llm_batch(prompts, max_workers=4)
```

**Example — map/reduce summarization:**

```python
# Map: summarize each partition
partition_summaries = sub_llm_batch([
    f"Summarize this data partition:\n\n{p}" for p in partitions
])

# Reduce: combine summaries
final_summary = sub_llm(
    f"Combine these summaries into a final report:\n\n"
    + "\n---\n".join(partition_summaries)
)
```

**Notes:**
- Returns results in the same order as the input prompts
- `max_workers` controls thread pool size — tune based on endpoint rate limits
- Each call is independent — failures in one don't affect others
