---
title: Generic security configuration naming
description: When implementing security-related configuration options, use generic,
  implementation-agnostic naming conventions rather than tying them to specific tools
  or runtimes. This approach ensures flexibility as the underlying technology stack
  evolves and prevents vendor lock-in in security configurations.
repository: google-gemini/gemini-cli
label: Security
language: Markdown
comments_count: 1
repository_stars: 65062
---

When implementing security-related configuration options, use generic, implementation-agnostic naming conventions rather than tying them to specific tools or runtimes. This approach ensures flexibility as the underlying technology stack evolves and prevents vendor lock-in in security configurations.

For example, when adding container security flags, prefer generic names like `SANDBOX_FLAGS` over tool-specific names like `DOCKER_RUN_FLAGS`. This allows the same configuration to work across different container runtimes (Docker, Podman, etc.) without requiring changes to user configurations.

**Example:**
```bash
# Good: Generic naming that works across container runtimes
export SANDBOX_FLAGS="--security-opt label=disable"

# Avoid: Tool-specific naming that limits flexibility  
export DOCKER_RUN_FLAGS="--security-opt label=disable"
```

This principle is especially important for security configurations because:
- Security policies should remain consistent regardless of the underlying implementation
- Teams may need to switch between different tools for security or compliance reasons
- Generic naming makes security configurations more maintainable and self-documenting

When reviewing security-related configuration code, ensure that environment variables, configuration keys, and API parameters use descriptive, generic names that reflect their security purpose rather than the specific tool being configured.