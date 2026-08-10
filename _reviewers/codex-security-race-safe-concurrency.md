---
title: Race-safe concurrency
description: When multiple workflow runs mutate or publish to the same shared external
  resource (labels, registries, “latest”), make synchronization explicit and resource-scoped,
  and handle conflicts by re-verifying state before proceeding.
repository: openai/codex-security
label: Concurrency
language: Yaml
comments_count: 2
repository_stars: 9394
---
{% raw %}
When multiple workflow runs mutate or publish to the same shared external resource (labels, registries, “latest”), make synchronization explicit and resource-scoped, and handle conflicts by re-verifying state before proceeding.

Apply this standard:
1) Use a concurrency group that matches the shared resource scope, not the triggering ref. If different refs can publish the same artifact (e.g., main run vs version tag), they must share the same concurrency key.
2) For create-and-apply operations, treat “already exists/duplicate create” as a race: re-fetch the resource and confirm the expected end state before continuing. Only fail closed for genuine errors.
3) Add regression coverage for the race path (mock duplicate-create / conflicting publish) to ensure the workflow still converges correctly.

Example pattern (resource-creation race, fail-closed with verification):
```bash
set -euo pipefail

resource_id="$1"

# Try create
if gh api --method POST ".../resources" -f id="$resource_id" --silent 2>/dev/null; then
  created=true
else
  created=false
fi

# Always verify current state before proceeding
current="$(gh api ".../resources/$resource_id" --jq '.id' 2>/dev/null || true)"
if [[ "$current" != "$resource_id" ]]; then
  echo "Failed to ensure resource exists; failing closed" >&2
  exit 1
fi

# Now safe to apply dependent steps
# ... apply label / proceed with publish ...
```

Concrete CI action: if your workflow uses something like `concurrency.group: <event ref>`, update it to something stable and shared for the published artifact (e.g., `container-publish-${{ github.repository }}-${{ matrix.image }}`) so overlapping publishes are serialized rather than merely “per ref”.
{% endraw %}
