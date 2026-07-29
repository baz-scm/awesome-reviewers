---
title: Validate Configuration Contracts
description: 'Configuration docs/examples and runtime behavior must stay aligned,
  and configuration must be explicit and validated.


  Apply two rules:

  1) **No silent no-ops:** If a config field is accepted by schema/docs, it must actually
  affect runtime behavior—or be removed from examples and clearly documented as unused/ignored.
  Add validation/tests that cover example...'
repository: QwenLM/qwen-code
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 26407
---

Configuration docs/examples and runtime behavior must stay aligned, and configuration must be explicit and validated.

Apply two rules:
1) **No silent no-ops:** If a config field is accepted by schema/docs, it must actually affect runtime behavior—or be removed from examples and clearly documented as unused/ignored. Add validation/tests that cover example payloads to prevent “looks supported but isn’t” failures.
2) **No ambiguous defaults:** For critical targets derived from environment/remotes (repo selection, workspace selection, endpoints), do not guess from generic names like `origin`. Require explicit config/flags (e.g., `--repo owner/name`) and validate structure (e.g., the remote URL must match the intended `owner/repo`). If missing/ambiguous, fail fast with a clear error or ask rather than continuing.

Example pattern:
```ts
// Ensure only the actually-used field controls behavior
const timeoutMs = config.autoRecall?.timeoutMs; // not config.timeoutMs
assertNumber(timeoutMs, 'autoRecall.timeoutMs is required');

// Ensure repo selection is explicit and validated
function pickRepo(requiredOwnerRepo: string, remotes: Record<string, string>) {
  if (!requiredOwnerRepo) throw new Error('Provide --repo owner/name');
  for (const url of Object.values(remotes)) {
    if (urlIncludesOwnerRepo(url, requiredOwnerRepo)) return requiredOwnerRepo;
  }
  throw new Error('No remote matches the intended --repo owner/name');
}
```

Result: admins/users get predictable configuration behavior, and tooling won’t act on the wrong repo or silently ignore intended settings.