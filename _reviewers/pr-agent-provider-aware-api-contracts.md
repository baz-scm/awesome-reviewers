---
title: Provider-aware API contracts
description: External API calls must be routed and shaped using provider/version-aware
  logic derived from immutable inputs (before any mutation), and idempotency keys
  must use stable identifiers.
repository: the-pr-agent/pr-agent
label: API
language: Python
comments_count: 5
repository_stars: 12523
---

External API calls must be routed and shaped using provider/version-aware logic derived from immutable inputs (before any mutation), and idempotency keys must use stable identifiers.

Apply this standard:
1) Compute provider predicates early and once
- Determine the target provider from the original, unmodified input (e.g., the model string before any rewriting).
- Use the predicate for all downstream decisions (endpoint/base URL, credential forwarding, and special kwargs).

2) Gate provider-specific request parameters
- Only include kwargs/fields that the chosen provider actually supports.
- If you must pass optional provider-specific config, add it conditionally based on the provider predicate.

3) Use stable state/dedup anchors for idempotency
- When an API operation is retried or runs across multiple commits, don’t anchor dedup/state to mutable attributes (e.g., diff `position`). Prefer stable fields (file path + normalized content) and ensure fallback/retry flows do not reapply filtering.

Example (LiteLLM-style guard):
```python
is_databricks = model.startswith("databricks/")
# mutate model only after provider predicate is captured
if self.azure:
    model = "azure/" + model if not is_databricks else model

kwargs = {
    "model": model,
    "deployment_id": deployment_id,
    "messages": messages,
    "temperature": temperature,
    "force_timeout": get_settings().config.ai_timeout,
}
if is_databricks:
    kwargs["api_base"] = os.environ.get("DATABRICKS_API_BASE")

if self.aws_bedrock_client and self.using_bedrock:  # another immutable predicate
    kwargs["aws_bedrock_client"] = self.aws_bedrock_client

response = await acompletion(**kwargs)
```

Example (robust GitHub PR URL parsing):
```python
# Accept both web URLs and enterprise/API-style URLs by extracting repo + PR id via regex.
pattern = r"/repos/([^/]+/[^/]+)/pulls?/?(?:/)?(\d+)"
m = re.search(pattern, pr_url)
if not m:
    raise ValueError("Unrecognized PR URL")
repo_name = m.group(1)
pr_number = int(m.group(2))
```

Result: fewer cross-provider runtime failures (unrecognized params), correct endpoint selection in multi-provider setups, and reliable idempotent behavior across retries and evolving diffs.