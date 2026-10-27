---
title: Escape backticks in shells
description: When writing CI/workflow `run` commands (bash/sh) that include code snippets
  in log messages or error text, escape shell metacharacters—especially backticks—so
  they are not interpreted as command substitution.
repository: facebook/react#b4
label: Security
language: Yaml
comments_count: 1
repository_stars: 251885
---

When writing CI/workflow `run` commands (bash/sh) that include code snippets in log messages or error text, escape shell metacharacters—especially backticks—so they are not interpreted as command substitution.

How to apply:
- In shell strings that will be interpreted by bash, use `\`` (or single quotes where appropriate) around any inline command text you want to display.
- Avoid unescaped backticks inside `echo`/`printf` strings in scripts executed by CI.

Example:
```sh
# Bad: backticks may trigger command substitution
echo "Run `yarn generate-inline-fizz-runtime` and check in the result."

# Good: escape backticks so they render as text
echo "Run \`yarn generate-inline-fizz-runtime\` and check in the result."
```