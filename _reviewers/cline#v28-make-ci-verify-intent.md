---
title: Make CI Verify Intent
description: CI/CD standards should ensure (a) builds are deterministic for the code
  under review and (b) the test commands developers add are actually executed in CI.
repository: cline/cline#v28
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70893
---

CI/CD standards should ensure (a) builds are deterministic for the code under review and (b) the test commands developers add are actually executed in CI.

1) Pin what you verify
- For packages using caret ranges, rely on a committed lockfile with CI installing via frozen lockfile.
- When bumping dependency ranges, keep the lockfile update aligned to versions you have actually verified; don’t broaden the lockfile to newer patch versions “just because” they’re allowed by the range.

2) Wire tests into CI
- Any new test script added to `package.json` (e.g., a Vitest command) should be connected to the CI workflow in the same PR or explicitly justified.
- Periodically audit CI to ensure all relevant toolchains run their tests (e.g., Node tests AND Rust `cargo test` if the repo includes Rust).

Example (dependency + CI-friendly install approach)
```json
// package.json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
Then ensure CI uses a frozen lockfile install so the committed lock pins the verified version.

Example (test script wired to CI)
```json
// package.json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Ensure your CI workflow calls `bun run test:desktop-client` (or an equivalent command) and also runs `cargo test` where applicable.