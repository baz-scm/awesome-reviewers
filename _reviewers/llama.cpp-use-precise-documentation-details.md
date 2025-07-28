---
title: Use precise documentation details
description: Documentation should provide specific, actionable information rather
  than vague or generic references. This applies to both technical specifications
  and descriptive text.
repository: ggml-org/llama.cpp
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 83559
---

Documentation should provide specific, actionable information rather than vague or generic references. This applies to both technical specifications and descriptive text.

For technical details, use exact package names, commands, or identifiers instead of approximate terms:
```markdown
# Vague - avoid this
- Install curl-dev package

# Precise - do this  
- Debian/Ubuntu: `sudo apt-get install libcurl4-openssl-dev`
- Fedora/RHEL: `sudo dnf install libcurl-devel`
- Arch: `sudo pacman -S curl`
```

For links, use descriptive text or show identifiers rather than generic phrases like "available here" or "click here". This improves accessibility and makes the purpose of the link immediately clear to readers.

```markdown
# Vague - avoid this
More information is [available here](https://github.com/org/repo/pull/4861)

# Precise - do this
More information is available in <https://github.com/org/repo/pull/4861>
```

This approach ensures documentation is immediately useful and reduces ambiguity for users trying to follow instructions or understand references.