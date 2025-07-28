---
title: optimize workflow triggers
description: Design CI/CD workflows with intentional triggers and conditions to avoid
  unnecessary executions, rate limiting, and contextually inappropriate behavior.
  Use specific event triggers and conditional statements to ensure workflow steps
  run only when needed and appropriate.
repository: hyprwm/Hyprland
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 28863
---

Design CI/CD workflows with intentional triggers and conditions to avoid unnecessary executions, rate limiting, and contextually inappropriate behavior. Use specific event triggers and conditional statements to ensure workflow steps run only when needed and appropriate.

Avoid overly broad automation like daily cron jobs that can cause rate limiting issues as your project scales. Instead, rely on event-driven triggers and manual execution when needed.

For steps that should only run in specific contexts, use conditional execution:

```yaml
- name: clang-format apply
  if: failure() && github.event_name == 'pull_request'
  run: ninja -C build clang-format

- name: Comment patch  
  if: failure() && github.event_name == 'pull_request'
  uses: mshick/add-pr-comment@v2
```

Consider separating workflows by purpose rather than adding complex conditions to a single workflow. This improves maintainability and reduces the risk of unintended executions.