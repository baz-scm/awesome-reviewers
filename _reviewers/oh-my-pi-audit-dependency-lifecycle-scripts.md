---
title: Audit dependency lifecycle scripts
description: When restricting which dependencies may run lifecycle (install/postinstall)
  scripts, explicitly maintain and audit the `trustedDependencies` list, and verify
  that your CI pipeline actually enforces the intended security behavior rather than
  silently succeeding. Package managers like Bun will skip untrusted lifecycle scripts
  by default and still report a...
repository: can1357/oh-my-pi
label: Security
language: Json
comments_count: 1
repository_stars: 37317
---

When restricting which dependencies may run lifecycle (install/postinstall) scripts, explicitly maintain and audit the `trustedDependencies` list, and verify that your CI pipeline actually enforces the intended security behavior rather than silently succeeding. Package managers like Bun will skip untrusted lifecycle scripts by default and still report a successful install, so a CI step that only checks the install command's exit code gives a false sense of safety — a new dependency requiring a script for correct operation can pass CI and break (or silently miss security-relevant setup) at runtime. Make sure: (1) any claim in documentation or PR descriptions about "install failing on untrusted scripts" matches actual tool behavior — correct or remove such claims if the tool only warns/skips; (2) CI explicitly checks for skipped/untrusted lifecycle scripts (e.g., via `bun pm untrusted` or equivalent) and fails the build if unexpected packages require scripts, rather than relying solely on the install exit code; and (3) every dependency added to `trustedDependencies` is deliberately reviewed, since lifecycle scripts are a known supply-chain attack vector and blanket or accidental trust can expose the build/runtime environment to malicious code execution.</description>
</invoke>
