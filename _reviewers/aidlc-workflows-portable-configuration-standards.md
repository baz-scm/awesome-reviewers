---
title: Portable Configuration Standards
description: 'All configuration-driven setup and workflow behavior must be (a) convention-based
  and unambiguous, and (b) portable across environments.


  Apply this standard:'
repository: awslabs/aidlc-workflows
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 3849
---

All configuration-driven setup and workflow behavior must be (a) convention-based and unambiguous, and (b) portable across environments.

Apply this standard:
1) Environment variables: document required env vars with directory-structure-aware guidance and OS-specific commands.
   - Example (Linux/macOS):
     ```bash
     export AIDLC_WORKFLOWS=~/dev/aidlc-workflows
     ```
   - Include an equivalent Windows path/command (CMD and/or PowerShell depending on your support policy) and clarify how to set it for the user’s actual directory layout.

2) Config file loading conventions: define deterministic pairing and loading rules.
   - For extensions: when scanning `extensions/`, load only `*.opt-in.md` at startup; derive the corresponding rules file by convention (strip `.opt-in.md`).
   - Clarify that a directory may contain both opt-in (`*.opt-in.md`) extensions and always-enforced extensions (no opt-in file), and that both behaviors can coexist.

3) OS-compatible automation: if you prescribe commands for config-dependent behavior (e.g., writing audit timestamps), always provide a Windows CMD variant when PowerShell may be unavailable.
   - Keep output in the canonical format required by the spec (e.g., ISO 8601). Example PowerShell timestamp (if allowed):
     ```powershell
     Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
     ```
   - Provide a CMD equivalent when PowerShell access is not guaranteed.

This prevents “works on my machine” failures and ensures the workflow’s configuration behavior is predictable and consistent.