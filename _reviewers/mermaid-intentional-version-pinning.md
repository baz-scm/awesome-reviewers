---
title: Intentional Version Pinning
description: When managing configuration via `package.json`/`tsconfig.json`, treat
  version and target specifiers as compatibility controls—not defaults. Choose constraints
  based on the dependency/toolchain’s real compatibility behavior, and wire compatibility
  between packages explicitly.
repository: mermaid-js/mermaid
label: Configurations
language: Json
comments_count: 6
repository_stars: 87952
---

When managing configuration via `package.json`/`tsconfig.json`, treat version and target specifiers as compatibility controls—not defaults. Choose constraints based on the dependency/toolchain’s real compatibility behavior, and wire compatibility between packages explicitly.

Apply these rules:
- **Non-semver or signature-risk dependencies:** avoid `^`; use `~x.y.z` or a **fixed** version (and document the exception).
- **Compatibility-coupled packages:** if you bump one package (e.g., a runtime), verify whether related packages (e.g., `@types/*`) are fixed/unchangeable and don’t assume compatible upgrades.
- **Version range choice:**
  - Use `^` only when the dependency truly follows semver and you’re OK with patch/minor updates.
  - Use `~` when you only want patch updates.
  - Use a fixed version when you need deterministic behavior.
- **Package boundary & opt-in behavior:** if functionality is meant to be added during initialization, don’t hard-bundle those packages as workspace deps; prefer documented opt-in wiring.
- **Cross-package compatibility:** add **peerDependencies** when the library/external package version pairing matters so mismatches produce clear warnings.
- **Config file targets:** ensure `tsconfig` module/target settings match current TypeScript semantics (e.g., prefer `Node16/Node18` settings over ambiguous `NodeNext` if TS changed behavior).

Example:
```json
{
  "dependencies": {
    "langium": "1.2.0",        // non-semver: pin
    "chokidar": "^3.6.0",    // semver: allow compatible updates
    "@iconify/utils": "3.0.1" // pinned to known-good version
  },
  "peerDependencies": {
    "mermaid": "~11.7.0"     // compatible minor/patch range
  }
}
```

And for `tsconfig.json`, keep `module`/`moduleResolution` consistent with the TS version you run (e.g., `Node16`/`Node16` or `Node18`/`Node16`), rather than blindly using `NodeNext`.