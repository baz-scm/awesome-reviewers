---
title: Explicit Environment Contracts
description: When code depends on runtime configuration (tooling paths, IDE/CLI context,
  feature flags), treat environment variables as an explicit contract and don’t rely
  on implicit process state.
repository: awslabs/aidlc-workflows
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 3849
---

When code depends on runtime configuration (tooling paths, IDE/CLI context, feature flags), treat environment variables as an explicit contract and don’t rely on implicit process state.

Apply these rules:
1) Prefer documented env inputs over assumed I/O
- If a component states that stdin is unusable or context is delivered via an env var (e.g., `USER_PROMPT`), read from that env var, parse the expected JSON shape, and fail fast (or fail-open only if the contract requires).

2) When spawning subprocesses, make the child’s environment deterministic
- Don’t assume the child can find `bun`/other binaries via inherited `PATH`.
- Either:
  - pass an explicit `env` (including a known-good `PATH` or required tool locations), and/or
  - invoke the exact executable via an absolute path (e.g., `process.execPath`) so the child doesn’t depend on PATH.

Code example (env-safe spawn):
```ts
function runCore(hookFile: string, input: Record<string, unknown>) {
  const childExe = process.execPath; // don’t depend on PATH
  return Bun.spawnSync([childExe, join(HOOKS_DIR, hookFile)], {
    stdin: "pipe",
    env: process.env, // or explicitly set PATH/bun dir if needed
    encoding: "utf-8",
    // ...forward other required options
  });
}
```

Checklist for reviews:
- Are required runtime inputs sourced from explicit env/config (not assumed stdin/PATH)?
- Does every subprocess receive the environment it needs (or use an absolute executable path)?
- If behavior differs in IDE vs CLI, is that controlled by explicit config/contracts rather than incidental process state?