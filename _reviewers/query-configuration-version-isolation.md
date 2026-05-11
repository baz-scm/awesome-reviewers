---
title: Configuration Version Isolation
description: When changing package/tooling configuration (peer deps, TS/ESLint parser
  versions, tsup/esbuild settings, or feature/behavior flags), make version and behavior
  control explicit and isolated so CI/build/tests don’t break unexpectedly.
repository: tanstack/query
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 49380
---

When changing package/tooling configuration (peer deps, TS/ESLint parser versions, tsup/esbuild settings, or feature/behavior flags), make version and behavior control explicit and isolated so CI/build/tests don’t break unexpectedly.

Apply these rules:
1) **Pin or resolve the exact toolchain versions needed per package** (don’t rely on repo-root defaults). If a test/build requires a newer TS feature set, resolve the parser/tooling in the package config.
2) **Isolate build config overrides**: if parent-level build plugins/settings cause failures, import the config you need and re-apply only the safe settings locally.
3) **Gate experimental runtime behavior behind a config/option** (or provide an experimental hook) rather than enabling it unconditionally.
4) **Centralize derived configuration**: decisions like `enabled`/`skipToken` interactions should be handled in one config derivation function (e.g., `defaultQueryOptions`) rather than scattered condition checks.
5) **Document the “why”** (e.g., “TS 4.9+ required for satisfies”, “peer dep bump needed for $derived override support”) and verify tests after dependency/version changes.

Example (package-local tool resolution):
```ts
const ruleTester = new ESLintUtils.RuleTester({
  // Use the package-resolved parser so TS-feature tests are consistent
  parser: require.resolve('@typescript-eslint/parser') as any,
});
```

Example (experimental gating):
```ts
export function useBaseQuery(/*...*/){
  if (!isServer && experimental_autoprefetch) {
    // allow prefetch during render only when explicitly enabled
  }
}
```