---
title: Actions workflow best practices
description: 'Use GitHub Actions native features and follow best practices to create
  maintainable, secure, and reliable CI workflows:


  1. **Use working-directory instead of manual cd commands**'
repository: Homebrew/brew
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 44168
---

Use GitHub Actions native features and follow best practices to create maintainable, secure, and reliable CI workflows:

1. **Use working-directory instead of manual cd commands**
   ```yaml
   # DO THIS
   - name: Run command in specific directory
     working-directory: ${{ steps.set-up-homebrew.outputs.repository-path }}
     run: |
       command1
       command2

   # INSTEAD OF THIS
   - name: Run command in specific directory
     run: |
       cd "${{ steps.set-up-homebrew.outputs.repository-path }}"
       command1
       command2
   ```

2. **Pin specific SHA commits for third-party actions**
   ```yaml
   # DO THIS
   - uses: codecov/test-results-action@9739113ad922ea0a9abb4b2c0f8bf6a4aa8ef820 # v1.0.1

   # INSTEAD OF THIS
   - uses: codecov/test-results-action@v1
   ```

3. **Handle all possible job states in conditional logic**
   ```yaml
   update-existing: ${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') || contains(needs.*.result, 'skipped') }}
   ```

4. **Scope permissions to the minimum required level**
   ```yaml
   # DO THIS - scope permissions per job
   jobs:
     build:
       permissions:
         contents: read
         attestations: write
         id-token: write

   # INSTEAD OF THIS - overly broad permissions
   permissions:
     contents: read
     attestations: write
     id-token: write
   ```

These practices improve workflow reliability, security, and maintainability while making troubleshooting easier.