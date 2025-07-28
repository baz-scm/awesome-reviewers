---
title: maintain API compatibility
description: When implementing or extending APIs, preserve compatibility with existing
  standards and expected behaviors. APIs should maintain the same contracts, interfaces,
  and behavioral patterns as the systems they emulate or replace.
repository: evanw/esbuild
label: API
language: Go
comments_count: 5
repository_stars: 39161
---

When implementing or extending APIs, preserve compatibility with existing standards and expected behaviors. APIs should maintain the same contracts, interfaces, and behavioral patterns as the systems they emulate or replace.

Key principles:
- Return results to callers rather than performing side effects directly (like file writing)
- Implement complete feature sets rather than partial implementations that break compatibility
- Use proper abstraction layers to maintain platform independence
- Respect fallback behaviors and edge cases from reference implementations
- Consider cross-platform and cross-browser compatibility when adding features

Example from bundler API design:
```go
// Bad: Bundler writes files directly, breaking API contract
defer ioutil.WriteFile(path.Join(targetFolder, url), []byte(source.Contents), 0644)

// Good: Return files to caller, preserving API contract
// Contents should be stashed on parseResult/ast and returned as BundleResult entry
```

This approach ensures APIs remain testable, predictable, and compatible with existing toolchains and workflows.