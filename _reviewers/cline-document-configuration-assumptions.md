---
title: Document configuration assumptions
description: When documenting configuration settings, environment setup, or system
  requirements, explicitly state assumptions about the target environment and provide
  accurate default values. Avoid making implicit assumptions that may not apply to
  all users or deployment scenarios.
repository: cline/cline
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 48299
---

When documenting configuration settings, environment setup, or system requirements, explicitly state assumptions about the target environment and provide accurate default values. Avoid making implicit assumptions that may not apply to all users or deployment scenarios.

For configuration settings, ensure documented default values match the actual implementation:

```markdown
- `cline.editor.skipDiffAnimation`: Disable the animated diff view when Cline makes changes to files. This can significantly speed up file modifications, especially when working with remote repositories. Default: `false`
```

For environment-specific instructions, acknowledge the target system and note alternatives:

```markdown
**Linux-specific Setup (Debian/Ubuntu)**
If you're developing on Debian-based Linux distributions, you'll need to install additional system libraries:
```bash
sudo apt update
sudo apt install -y libatk1.0-0 libatk-bridge2.0-0 ...
```
Note: For RHEL, Arch, or Alpine systems, equivalent packages will have different names and installation methods.
```

This practice prevents confusion, reduces support burden, and ensures users can adapt instructions to their specific environments.