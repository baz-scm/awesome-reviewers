---
title: Secure CI/CD pipelines
description: 'Implement strict security controls in continuous integration and deployment
  workflows:


  1. Pin external GitHub Actions to immutable commit hashes rather than mutable tags:'
repository: openai/codex
label: Security
language: Yaml
comments_count: 2
repository_stars: 31275
---

Implement strict security controls in continuous integration and deployment workflows:

1. Pin external GitHub Actions to immutable commit hashes rather than mutable tags:
   ```yaml
   # Instead of this (vulnerable to supply chain attacks):
   - uses: codespell-project/codespell-problem-matcher@v1
   
   # Use this (pinned to specific commit):
   - uses: codespell-project/codespell-problem-matcher@e8fc5c5c5e6c5c5c5c5c5c5c5c5c5c5c5c5c5c5c
   ```

2. Isolate workflows requiring elevated permissions into separate files for clearer security boundaries:
   ```yaml
   # Separate high-privilege workflows (e.g., update-nix-hash.yml) from regular CI workflows
   permissions:
     contents: write  # Clearly visible elevated permission
   ```

3. Apply the principle of least privilege by:
   - Only granting write permissions where strictly necessary
   - Using conditional execution to limit when privileged jobs run (e.g., `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`)
   
4. Thoroughly review scripts running with elevated permissions to protect against:
   - Secret leakage
   - Unintended commits or changes
   - Input injection vulnerabilities

Implementing these practices prevents supply chain attacks and reduces the risk of compromised workflows affecting your repository.