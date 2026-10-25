---
title: Explicit Null Semantics
description: 'When inputs/settings are optional (undefined/nullable) treat null/undefined
  as part of the product logic: distinguish “absent” from “explicit empty”, prefer
  explicit reset values, and gate behavior so missing context can’t silently pick
  the wrong fallback or misclassify errors.'
repository: ClInE/cLiNe
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70838
---

When inputs/settings are optional (undefined/nullable) treat null/undefined as part of the product logic: distinguish “absent” from “explicit empty”, prefer explicit reset values, and gate behavior so missing context can’t silently pick the wrong fallback or misclassify errors.

Practical rules:
- Distinguish absent vs empty
  - If omitted should mean “use previous”, use `??`/length checks; don’t treat `[]` the same as “not provided”.
  - Pattern:
    ```ts
    // If the caller omits images, keep retry’s images.
    const effectiveImages = images?.length ? images : retry.images
    await initTask(retry.prompt, effectiveImages, files)
    ```
- Use explicit resets/markers instead of relying on leftovers
  - If clearing must happen, send an explicit reset (e.g., `null`/cleared auth fields) through the correct contract so old values can’t win by precedence.
  - Pattern:
    ```ts
    // Only override when caller actually supplied a key.
    const apiKey = typeof args?.api_key === 'string' ? args.api_key : undefined
    if (apiKey?.trim() && update.auth === undefined) {
      update.auth = { accessToken: "", refreshToken: "" } // explicit clear/reset intent
    }
    ```
- Gate mode-dependent behavior on required fields/context
  - If a mode requires additional data (cloud needs repo; provider errors require matching auth), don’t fall through to the “other” mode or generic error.
  - Pattern:
    ```ts
    const canSendCloud =
      cloudSessionsEnabled && cloudTaskTarget?.target === "cloud" && !!cloudTaskTarget.repoUrl
    if (!canSendCloud) return // or disable send until repoUrl exists
    ```
- Encode configuration precedence in one place
  - For config like frontmatter where multiple keys can exist, implement deterministic precedence with explicit null/undefined handling.

Checklist for PRs:
- For every `?.`/`??`/nullable field, write down the intended semantics: absent vs empty vs reset.
- Ensure “missing optional context” can’t silently route to an incorrect fallback (mode switch, wrong error, skipped capability check).
- If a value must be cleared, prefer an explicit reset through the relevant API/contract rather than leaving ambiguity that lets old state win.