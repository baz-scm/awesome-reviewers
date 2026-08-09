---
title: Config Resolution Discipline
description: When adding/updating configuration handling, resolve configuration once
  into a single immutable runtime context, and make precedence/fallback behavior explicit.
repository: apple/container
label: Configurations
language: Swift
comments_count: 5
repository_stars: 48787
---

When adding/updating configuration handling, resolve configuration once into a single immutable runtime context, and make precedence/fallback behavior explicit.

**Rules**
1. **Never use `try!` for config loading.** Prefer `throws` at the boundary and fail fast with a clear error message.
2. **Avoid threading raw config through long call chains.** Instead, resolve a final config once (including user overrides) and inject it at module boundaries as an immutable context.
3. **Define precedence explicitly** (document it in code): e.g. `environment variables -> user overrides file -> system config`.
   - If env values may change during process lifetime, either (a) read env only once when resolving the immutable config, or (b) explicitly implement re-resolution/hot reload—don’t accidentally mix both.
4. **Don’t couple unrelated utilities to system config.** If a helper doesn’t conceptually need system config, refactor it to accept only the minimal parameters it truly requires.
5. **Keep models OS-agnostic.** Move OS/Linux-specific settings into runtime/OS-specific payloads (encoded/decoded via runtime configuration), not into generic cross-platform configuration types.
6. **Respect explicit user intent for derived behavior.** Only set derived environment variables/forwarding behavior when the corresponding flag/config input was explicitly provided; otherwise define clear fallback behavior (and only when input is absent).

**Sketch**
```swift
struct RuntimeConfigContext: Sendable {
    let finalConfig: ContainerSystemConfig
}

enum ConfigError: Error {
    case loadFailed(String)
}

func resolveRuntimeConfig() throws -> RuntimeConfigContext {
    do {
        let system = try SystemRuntimeOptions.loadConfig() // throws, no try!

        // precedence: env -> user file -> system
        let userOverrides = try loadUserOverrides() // throws
        let envOverrides = loadEnvOverrides() // evaluate now

        let merged = merge(system: system, user: userOverrides, env: envOverrides)
        return RuntimeConfigContext(finalConfig: merged)
    } catch {
        throw ConfigError.loadFailed("Failed to resolve runtime config: \(error)")
    }
}

// Inject at boundaries
let ctx = try resolveRuntimeConfig()
startServices(with: ctx) // services/utilities can use ctx.finalConfig without plumb-through
```

Apply these rules to new config flows and refactors: they prevent unsafe initialization, reduce coupling, make override behavior predictable, and keep platform-specific concerns contained.