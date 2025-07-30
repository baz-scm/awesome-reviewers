---
title: Document configuration clarity
description: Ensure all configuration options and setup instructions are clearly documented
  with their intended purposes, use cases, and the most accessible implementation
  paths. When introducing new configuration classes or setup steps, include contextual
  descriptions that help users understand when and why to use each option.
repository: SWE-agent/SWE-agent
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 16839
---

Ensure all configuration options and setup instructions are clearly documented with their intended purposes, use cases, and the most accessible implementation paths. When introducing new configuration classes or setup steps, include contextual descriptions that help users understand when and why to use each option.

For configuration classes, provide clear descriptions of their functionality:
```markdown
Currently, there are three main agent classes:

* `DefaultAgentConfig`: This is the default agent.
* `RetryAgentConfig`: A "meta agent" that instantiates multiple agents for multiple attempts and then picks the best solution.
* `ShellAgentConfig`: An agent that provides shell-based interaction capabilities for experimental mode and quick interactive workflows.
```

For setup instructions, prioritize user-friendly approaches and link to simpler alternatives when available:
```markdown
3. [Install Miniconda](https://docs.anaconda.com/free/miniconda/#quick-command-line-install), then create the `swe-agent` environment with `conda env create -f environment.yml`
```

This approach helps developers quickly understand available configuration options and reduces setup friction, leading to better adoption and fewer configuration-related issues.