---
title: Configuration precedence rules
description: Whenever a setting can come from multiple sources (explicit per-call
  config, provider-level overrides, suite/global env, specific env vars, or built-in
  defaults), the precedence order must be explicit, documented, and verified end-to-end
  — never silently dropped or confused with a built-in default.
repository: promptfoo/promptfoo
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 26565
---

Whenever a setting can come from multiple sources (explicit per-call config, provider-level overrides, suite/global env, specific env vars, or built-in defaults), the precedence order must be explicit, documented, and verified end-to-end — never silently dropped or confused with a built-in default.

Key practices:
- Distinguish an explicitly supplied value from an injected default. Refactors that change how a default is applied must not discard a user-set env var or config value just because some other branch condition (e.g., an unrecognized model alias) is taken. For example, when `OPENAI_MAX_TOKENS=73` is set, a provider must still forward `73` even if it falls into a "modern model" branch that normally omits the field for defaults — only the synthetic default should be omitted, not a user-supplied value.
- Define and keep a single, consistent precedence order among layers (e.g., explicit constructor/provider config > provider-level env override > suite-level env > ambient/process env > built-in default). Don't let a merge step (such as suite `env` folded into `providerOptions.env`) accidentally rank below a layer that is supposed to be lower priority.
- When both a convenience/shorthand setting and a fully-specified nested config can set the same value (e.g., a top-level `numberOfResults` convenience field vs. a complete `retrieveAndGenerateConfiguration`), the more specific/explicit configuration must win, and this must be documented in code comments and user docs.
- Apply caller-supplied overrides last, so they can actually override internal defaults (not vice versa) unless there's a clearly documented reason (e.g., a required internal flag) why an internal value must win.
- Prefer deferring to an authoritative external source (e.g., AWS region/model availability) over hardcoding allowlists that can drift and go stale, unless local validation is explicitly required.
- Add regression tests that exercise the *full* resolution path (e.g., through loader functions like `loadApiProvider`, not just a direct constructor call) so that merge/precedence behavior is verified the way it will actually run in production.
- When changing behavior around env vars or defaults, describe it accurately in the PR/changelog — call out whether it's a compatibility change or a behavior-preserving fix, so consumers relying on old defaults aren't surprised.

Example of the problem to avoid:
```ts
// BAD: drops an explicit user-set env var together with the injected default
maxTokens: assumeModernModel ? undefined : maxTokensDefault,

// GOOD: only omit the synthetic default; keep an explicitly configured value
maxTokens: assumeModernModel
  ? getEnvInt('OPENAI_MAX_TOKENS') // explicit override still respected
  : maxTokensDefault,
```