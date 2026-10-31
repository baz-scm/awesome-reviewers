---
title: Environment-driven config resolution
description: When behavior depends on environment variables or config files (e.g.
  git's `core.hooksPath`, `GIT_DIR`, `GIT_CONFIG*`), never assume an in-process reimplementation
  of the resolution rules is complete. Config can be layered and overridden through
  many sources — env vars, `~`/`%(prefix)%` expansion, system/global/local config,
  `-c` flags, wrapper scripts —...
repository: can1357/oh-my-pi
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 37317
---

When behavior depends on environment variables or config files (e.g. git's `core.hooksPath`, `GIT_DIR`, `GIT_CONFIG*`), never assume an in-process reimplementation of the resolution rules is complete. Config can be layered and overridden through many sources — env vars, `~`/`%(prefix)%` expansion, system/global/local config, `-c` flags, wrapper scripts — and a native reimplementation will silently diverge from the real tool on edge cases.

Apply these rules:
1. Always use the exact environment explicitly supplied by the caller, not ambient `process.env`. Callers may filter environment (e.g. stripping `GIT_DIR`-family vars) before passing it down, so accept and thread an explicit `env` parameter through every subprocess/config lookup.
2. Detect when the environment or config injects overrides your in-process logic doesn't understand (e.g. `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_GLOBAL`), and in those cases delegate to the authoritative external tool (spawn the real binary) instead of guessing, rather than only partially supporting such overrides.
3. Treat the external tool as the source of truth whenever it is available and capable (correct version, starts successfully); fall back to the in-process resolution only when the tool can't run, and report that distinctly (e.g. "no-git"/"old-git") instead of treating a found resource as missing.
4. Validate and sanitize anything the authoritative tool reports before trusting it (e.g. reject MSYS-style `/c/...` paths on Windows, but accept legitimate UNC paths like `//server/share/...`).
5. Cover these cases with tests that exercise real config edge cases: tilde/prefix expansion, environment-variable overrides, old/missing tool versions, and platform-specific path formats (UNC vs MSYS) — verifying against the actual external tool's reported behavior, not just the reimplementation's assumptions.

Example pattern:
```js
async function resolveConfigPath(cwd, env, signal) {
  if (hasUnsupportedOverrides(env)) {
    // Defer to the authoritative tool when env/config overrides exceed in-process support.
    return await askRealTool(cwd, env, signal);
  }
  return inProcessResolve(cwd, env);
}
```