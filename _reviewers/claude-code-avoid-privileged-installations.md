---
title: Avoid privileged installations
description: Always recommend user-level package installations rather than using administrative/root
  privileges. Installing packages with elevated permissions can compromise system
  security and stability. Documentation and scripts should explicitly guide users
  toward safer installation practices.
repository: anthropics/claude-code
label: Security
language: Markdown
comments_count: 1
repository_stars: 25432
---

Always recommend user-level package installations rather than using administrative/root privileges. Installing packages with elevated permissions can compromise system security and stability. Documentation and scripts should explicitly guide users toward safer installation practices.

Example:
```markdown
# Installation

## User-level installation (recommended)
```sh
mkdir -p ~/.local/share/npm-packages
npm config set prefix ~/.local/share/npm-packages
export PATH=~/.local/share/npm-packages/bin:$PATH
npm install -g my-package
```

We recommend installing this package as a regular user, not as an administrative user like root. Installing as a regular user helps maintain your system's security and stability.
```