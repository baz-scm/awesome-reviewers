---
title: Pinned Releases For CI
description: 'Ensure release and versioning behavior is deterministic and pipeline-owned.


  - For CI/CD workflows/rules: if it’s experimental, tracking the “head” is acceptable;
  for anything users rely on in production, pin to an explicit release (tag/zip/release
  branch) rather than “always latest” via submodule auto-update.'
repository: awslabs/aidlc-workflows
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 3849
---

Ensure release and versioning behavior is deterministic and pipeline-owned.

- For CI/CD workflows/rules: if it’s experimental, tracking the “head” is acceptable; for anything users rely on in production, pin to an explicit release (tag/zip/release branch) rather than “always latest” via submodule auto-update.
- For app version/changelog/release artifacts: do not rely on AI-driven blanket edits across heterogeneous build systems. Instead, delegate version bumps to the project’s existing build/release scripts in CI (one canonical mechanism per project).
- Keep the AI workflow generic and tools-agnostic: never try to “future-proof” by enumerating Maven/Gradle/NPM/etc. inside the workflow logic.

Example (CI-owned version bump step, rather than AI editing multiple build files):

```yaml
# Example sketch: CI invokes the project’s release/version script
steps:
  - name: Bump version
    run: |
      # Use the repository’s canonical release tooling
      # (e.g., ./gradlew release, mvn versions:set, npm version, etc.)
      ./ci/release/bump-version.sh "$RELEASE_VERSION"
  - name: Generate changelog/artifacts
    run: ./ci/release/build-release-artifacts.sh "$RELEASE_VERSION"
```

Apply this policy by: pinning the workflow/rules source for stable usage, and centralizing version/release updates in CI scripts already appropriate for your build tooling.