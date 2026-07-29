---
title: Publish-safe dependency ranges
description: When CI/CD builds and release automation publish or test packages from
  a monorepo, inter-workspace dependency specs and lockfile contents must stay publish-safe
  and CI-consistent.
repository: QwenLM/qwen-code
label: CI/CD
language: Json
comments_count: 4
repository_stars: 26407
---

When CI/CD builds and release automation publish or test packages from a monorepo, inter-workspace dependency specs and lockfile contents must stay publish-safe and CI-consistent.

**Standards**
1) **No unresolvable workspace paths in published deps**
   - Avoid `"file:../..."` specifiers in `package.json` of packages intended for registry publication; they can break `npm i` for consumers.

2) **Use publish-time-resolved specs**
   - For channel-to-base (and similar) workspace dependencies, prefer `workspace:*` so the dependency resolves to the correct concrete version at publish time.
   - If you must use semver ranges, ensure your release/version automation rewrites dependency specifiers across workspaces after version bumps and handles pre-releases/nightlies.

3) **Keep lockfile aligned with manifests**
   - Any change to `package.json` dependencies must be followed by lockfile reconciliation; stale/phantom entries in `package-lock.json` can cause unexpected CI lock-diff failures.

4) **If CI starts running new workspaces, ensure reporting is wired**
   - Adding workspaces to default CI scripts can make tests run but produce no JUnit/coverage artifacts due to reporter/glob config differences—verify artifact collection so regressions don’t fail “silently.”

**Example (recommended inter-workspace dependency style)**
```json
{
  "dependencies": {
    "@qwen-code/channel-base": "workspace:*"
  }
}
```

**Operational checklist for PRs affecting release/CI**
- Confirm cross-workspace deps are publish-resolvable (no `file:` in published package manifests).
- Prefer `workspace:*` or ensure your versioning/release scripts rewrite dependency ranges.
- Update `package-lock.json` after dependency changes.
- If CI workspaces changed, confirm JUnit/coverage collection still covers them.