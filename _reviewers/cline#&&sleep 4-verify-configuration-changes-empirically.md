---
title: Verify configuration changes empirically
description: Treat configuration artifacts (generated files, feature-flag/setting
  keys, ignore/exclude lists) as derived from an authoritative source or tool, and
  verify any change against that source or the actual tool behavior instead of hand-editing
  or assuming correctness.
repository: cline/cline#&&sleep 4
label: Configurations
language: Other
comments_count: 3
repository_stars: 70980
---

Treat configuration artifacts (generated files, feature-flag/setting keys, ignore/exclude lists) as derived from an authoritative source or tool, and verify any change against that source or the actual tool behavior instead of hand-editing or assuming correctness.

- For generated config/proto files, never hand-edit the output. Re-run the generator against its source of truth (e.g. `node scripts/generate-state-proto.mjs` driven by `state-keys.ts`) and confirm it produces no unexpected diff, then validate with `npm run protos` / `npm run check-types`.
- For settings or feature flags that vary by build/environment (e.g. nightly vs stable, legacy vs next rollout), make sure the key derivation explicitly accounts for every variant. Don't assume a single shared prefix or default will work across all environments—trace how the key is actually computed (e.g. `gen-manifest.mjs`'s `nextPkg.name === "cline-nightly" ? "cline-nightly" : "cline"` prefix) and name/document each variant explicitly.
- For packaging/ignore configuration (e.g. `.vscodeignore`), don't add or remove entries based on assumption. Test the actual packaging tool's behavior (e.g. `vsce ls` with and without the entry) to confirm whether a rule is redundant with built-in defaults or genuinely required before changing it.

In short: before committing a configuration change, reproduce the generation step or exercise the actual tool/environment the config feeds into, and use that evidence—not assumption—to justify the change.</description>
</invoke>
