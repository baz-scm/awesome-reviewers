---
title: Defensive workflow triggers
description: 'Write CI/CD workflow conditions, triggers, and inputs defensively to
  avoid unintended or unsafe executions. Specifically:

  - For manual/dispatch inputs that control risky actions (e.g., publish tag), avoid
  pre-selecting a default; require the operator to explicitly choose a value.'
repository: facebook/react#b18
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 251889
---

Write CI/CD workflow conditions, triggers, and inputs defensively to avoid unintended or unsafe executions. Specifically:
- For manual/dispatch inputs that control risky actions (e.g., publish tag), avoid pre-selecting a default; require the operator to explicitly choose a value.
- When matching comment/text bodies to trigger commands (e.g., `/land`), use exact or anchored matching (`startsWith`, equality) instead of `contains`, since substrings can appear incidentally (e.g., in a URL) and trigger the job unintentionally.
- Choose event triggers that map precisely to the condition you care about (e.g., use the `labeled` event instead of `pull_request: opened` plus a label check) to avoid races between workflows and unreliable behavior.
- When embedding shell commands inside echoed strings or error messages, escape special characters properly (e.g., backticks) so they are rendered literally instead of being executed by the shell:
```yaml
run: |
  git diff --exit-code || (echo "Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false)
```
- Avoid duplicating checks already performed by the underlying tool (e.g., re-checking if a package version exists before `npm publish`, which already fails safely on duplicates) to keep workflows simple and maintainable.

Following these practices prevents accidental publishes, unintended job triggers, race conditions, and shell-injection-like bugs in CI/CD pipelines.