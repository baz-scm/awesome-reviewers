---
title: Optimize workflow resources
description: 'When designing CI/CD workflows, optimize resource usage while maintaining
  appropriate test coverage. Consider these guidelines:


  1. **Avoid duplicate testing configurations** unless explicitly needed'
repository: pytorch/pytorch
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 91169
---

When designing CI/CD workflows, optimize resource usage while maintaining appropriate test coverage. Consider these guidelines:

1. **Avoid duplicate testing configurations** unless explicitly needed
   ```yaml
   # DO: Select one configuration when appropriate
   - name: linux-test-freezing
     if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'
     # Only run one configuration to save resources

   # DON'T: Run redundant configurations that increase resource usage
   - name: linux-test-default
     if: github.event.schedule == '0 7 * * *'
   - name: linux-test-freezing
     if: github.event.schedule == '0 7 * * *'
   ```

2. **Don't over-specify compute resources** unless required for the specific job
   ```yaml
   # DO: Use default runners when sufficient
   jobs:
     build-job:
       runs-on: ubuntu-latest
       # No specific size requirements

   # DON'T: Specify large instances unnecessarily
   jobs:
     build-job:
       runs-on: "linux.12xlarge"  # Only specify if truly needed
   ```

3. **Separate workflow changes logically** to improve review efficiency and maintainability
   - Split CI test changes from dashboard/visualization changes
   - Make smaller, focused PRs that address one concern at a time

This practice ensures cost-effective use of CI/CD resources, faster build times, and more maintainable workflow definitions.
