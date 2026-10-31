---
title: Validate and scope configuration changes
description: Configuration values from settings, CLI flags, YAML, or environment variables
  are untrusted input and must be validated/normalized at the point of use, not just
  cast through a schema. Loosely-typed arrays or fields (e.g. a model-id list) can
  still receive non-string or malformed entries from `config set` or hand-edited YAML;
  guard every element with a...
repository: can1357/oh-my-pi
label: Configurations
language: TypeScript
comments_count: 9
repository_stars: 37317
---

Configuration values from settings, CLI flags, YAML, or environment variables are untrusted input and must be validated/normalized at the point of use, not just cast through a schema. Loosely-typed arrays or fields (e.g. a model-id list) can still receive non-string or malformed entries from `config set` or hand-edited YAML; guard every element with a runtime type check, drop or coerce invalid entries instead of throwing, enforce any protocol/wire limits (e.g. a provider's max fallback count) by slicing with a warning log rather than failing the request, and cover this with a regression test using deliberately malformed input.

Settings must also be resolved consistently everywhere they apply: when a setting has an override (a table name, a path alias, a backend selector), route every consumer through the same resolver helper instead of re-implementing resolution ad hoc, so a script, CLI path, and runtime path never disagree on what a setting means. If a setting only takes effect in a subset of contexts (e.g. a task-only override), either reject it explicitly elsewhere or document the scoping clearly — never let it silently fall back to a different behavior.

Finally, treat any change to a default value, or any new default-enabled behavior, as a user-visible contract change: call it out explicitly, keep it in its own PR separate from unrelated fixes, and get explicit maintainer sign-off before merging, especially when it diverges from a previously agreed-upon default.

Example of defensive validation for a config-supplied list:
```ts
const serverSideFallbackModels = serverSideFallbackEnabled
  ? settings
      .get("providers.anthropic.serverSideFallbackModels")
      .filter((id): id is string => typeof id === "string" && id.trim().length > 0)
      .slice(0, ANTHROPIC_MAX_FALLBACK_MODELS) // enforce wire limit, warn if truncated
  : [];
```