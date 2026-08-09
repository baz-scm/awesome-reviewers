---
title: Copy-Paste Safe Docs
description: 'Ensure documentation command examples and command reference sections
  are accurate and safe to copy/paste.


  Apply these rules:

  - Code fences: use a `bash` (or relevant shell) code fence for blocks that contain
  only shell commands.'
repository: apple/container
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 48787
---

Ensure documentation command examples and command reference sections are accurate and safe to copy/paste.

Apply these rules:
- Code fences: use a `bash` (or relevant shell) code fence for blocks that contain only shell commands.
- Copy/paste safety: do not include inline explanatory comments inside a command block (especially trailing `# ...`). If explanation is needed, put it outside the code fence.
- Consistency checks: the command reference must match implementation—usage, “Options”, defaults, and supported flags must agree (no contradictions like “No options” when `--debug` is shown).
- Prune unsupported options/variants: only document flags/options that actually apply to that command.
- Keep help/flag text formatting consistent with existing precedent (e.g., where environment override info appears relative to default/format details).

Example (copy/paste safe):
```bash
# Good: no inline trailing comments inside the runnable block
container build -t builder .
container system property set image.builder builder:latest
container rm -f buildkit
```

And ensure “Usage” and “Options” sections agree (e.g., if usage shows `[--debug]`, the command’s options documentation must include `--debug`, or usage must be corrected).