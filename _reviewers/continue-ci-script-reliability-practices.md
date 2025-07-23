---
title: CI script reliability practices
description: 'Ensure CI/CD workflows maintain reliability by following these practices:


  1. **Use explicit script paths** - Always use explicit paths when invoking scripts
  (e.g., `./build.ps1` for PowerShell or `./build.sh` for bash) rather than relying
  on implicit path resolution. This ensures the runner can locate and execute scripts
  regardless of the current working...'
repository: continuedev/continue
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 27819
---

Ensure CI/CD workflows maintain reliability by following these practices:

1. **Use explicit script paths** - Always use explicit paths when invoking scripts (e.g., `./build.ps1` for PowerShell or `./build.sh` for bash) rather than relying on implicit path resolution. This ensures the runner can locate and execute scripts regardless of the current working directory.

2. **Verify script existence** - Confirm that all referenced script files and directories exist in the repository before merging workflow changes:
   ```yaml
   # Before merging, verify that these paths exist:
   - name: Build packages (Windows)
     run: ./scripts/build-packages.ps1
     
   - name: Build packages (Unix)
     run: ./scripts/build-packages.sh
   ```

3. **Set execute permissions** - Include a step to set execute permissions for shell scripts on Unix systems:
   ```yaml
   - name: Set permissions
     run: chmod +x ./build.sh
     
   - name: Build
     run: ./build.sh
   ```

4. **Handle secrets securely** - Add conditional guards when using repository secrets to accommodate PRs from forks where secrets aren't available:
   ```yaml
   - name: Run tests requiring API keys
     if: ${{ github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository }}
     run: npm test
     env:
       API_KEY: ${{ secrets.API_KEY }}
   ```

These practices will prevent common CI/CD failures and improve workflow reliability across different environments and contributor scenarios.