---
title: File-Based Command Safety
description: When invoking CLI/shell or external tools, treat all generated/ingested
  content (LLM output, web research, imported facts) as untrusted and never embed
  it directly into command-line strings.
repository: bmad-code-org/bmad-method
label: Security
language: Toml
comments_count: 1
repository_stars: 51859
---

When invoking CLI/shell or external tools, treat all generated/ingested content (LLM output, web research, imported facts) as untrusted and never embed it directly into command-line strings.

Instead, use a file-based contract:
- Write untrusted text to a skill-controlled file in a fixed workspace directory.
- Pass only a trusted, system-generated file path (e.g., `{brief_file}`) into the invoke command/template.
- Ensure the brief text itself never becomes part of shell/CLI arguments, where characters like quotes/backticks/`$()` could be interpreted.

Example pattern:
```toml
# Untrusted brief content is written to disk by the skill.
# The engine invocation receives only a file path.
[[workflow.engines]]
code = "agy"
kind = "cli"
invoke = 'agy -p "{brief_file}" --dangerously-skip-permissions'
```

Apply this rule consistently across:
- CLI invocation templates
- Any orchestration layer that currently interpolates text into commands
- Any “delegate engine”/external-tool integration where prompts, claims, or citations might contain shell metacharacters

Goal: prevent command/argument injection driven by indirect prompt injection while improving reliability by keeping inputs structured and escaping-free.