---
title: Use Supported Config Surfaces
description: When code behavior depends on environment variables or OS/platform UI
  integrations, make it deterministic and aligned with what the platform actually
  supports.
repository: cline/cline#v8
label: Configurations
language: Rust
comments_count: 2
repository_stars: 70867
---

When code behavior depends on environment variables or OS/platform UI integrations, make it deterministic and aligned with what the platform actually supports.

Apply these rules:
- Discover configuration/executables using the same environment the user’s session uses (e.g., invoke an interactive login shell so .zshrc/.bashrc PATH is honored) and add regression tests for those shell-specific setups.
- Avoid “best-effort” assumptions about installed command layouts/paths; probe/validate via the runtime/CLI when possible, and surface discovery failures instead of silently falling back to secondary installs.
- For platform integrations (icons, UI, settings), use the supported integration surface. If a runtime override is not reliable across Windows configurations, remove it and update only the parts the platform guarantees.
- Make subprocess behavior explicit with environment flags to prevent unintended side effects.

Example (deterministic subprocess execution during discovery):
```rust
fn bounded_output(command: &mut std::process::Command) -> Option<String> {
    command
        .stdin(std::process::Stdio::null())
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::null())
        // Explicit config to keep behavior deterministic
        .env("CLINE_NO_AUTO_UPDATE", "1")
        .env_remove("BUN_BE_BUN");
    super::hide_console_window(command);

    let mut child = command.spawn().ok()?;
    // ... bounded wait/timeout ...
    let output = child.wait_with_output().ok()?;
    Some(String::from_utf8_lossy(&output.stdout).into_owned())
}
```

Checklist for PRs:
- Does this change assume PATH/.zshrc/.bashrc/session variables? If yes, update discovery to use the correct shell and add a regression test.
- Does this change rely on an OS runtime override that may be configuration-dependent? If yes, verify the supported surface and remove unreliable overrides.
- Are errors actionable (no silent fallbacks)?
- Are subprocess/environment behaviors explicit and documented via env vars/flags?