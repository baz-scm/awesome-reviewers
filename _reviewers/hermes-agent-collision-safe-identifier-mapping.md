---
title: Collision-Safe Identifier Mapping
description: 'Treat every identifier (tool name, command name, provider slug, theme
  name, thread key) as a runtime contract: you must generate, transform, and resolve
  it consistently, and preserve an unambiguous mapping between any emitted/sanitized
  UI value and the backend identity.'
repository: nousresearch/hermes-agent
label: Naming Conventions
language: Python
comments_count: 11
repository_stars: 221948
---

Treat every identifier (tool name, command name, provider slug, theme name, thread key) as a runtime contract: you must generate, transform, and resolve it consistently, and preserve an unambiguous mapping between any emitted/sanitized UI value and the backend identity.

Apply these rules:
1) Use a single source-of-truth canonical form for comparisons/dispatch.
   - Prefer canonical slugs/known naming contracts over raw display strings.
   - Don’t apply broad “starts with” naming exemptions that change meaning unless scoped to the exact contract (e.g., require `custom:`).
2) Keep “display/sanitized” values separate from “dispatch” values.
   - If you must truncate or sanitize for UI limits, store an opaque token as the dispatched value and map it back to the full canonical name.
3) Enforce collision safety at registration/dispatch time.
   - Reject name collisions across different “kinds” (e.g., frontend tool vs real backend tool vs state-writer tool).
   - Allow redeclarations only when they’re the same kind and validated for that run.
4) Transform identifiers narrowly and deterministically.
   - Strip only the intended suffix (avoid double-suffix derivations).
   - After truncation/capping, re-validate identifier constraints (e.g., branch ref formatting).

Example pattern (opaque UI token → canonical dispatch):
```python
# UI: show truncated label, dispatch uses stable token
items = {token: canonical_name}

# When rendering select options
for token, canonical in list(items.items())[:24]:
    select_option = discord.SelectOption(
        label=canonical[:100],  # display-only truncation
        value=token,            # dispatched identity
    )

# On selection
token = interaction.data["values"][0]
canonical = items[token]
await dispatch(f"/{canonical}")
```

Follow the same separation for Telegram menus, tool registries, and provider/theme resolution: emitted names/values must be mapped back to the exact canonical identifier used for backend resolution, and collisions must be rejected early rather than “best-effort” resolved later.