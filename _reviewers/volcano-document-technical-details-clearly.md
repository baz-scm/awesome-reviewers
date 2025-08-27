---
title: Document technical details clearly
description: Ensure all technical documentation provides clear explanations and follows
  proper formatting conventions. Technical parameters, configuration options, and
  complex concepts should include explanatory comments or descriptions to make them
  accessible to users and maintainers.
repository: volcano-sh/volcano
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 4899
---

Ensure all technical documentation provides clear explanations and follows proper formatting conventions. Technical parameters, configuration options, and complex concepts should include explanatory comments or descriptions to make them accessible to users and maintainers.

Key practices:
- Add explanatory comments for configuration parameters and technical arguments
- Follow established formatting conventions (e.g., proper author name formatting in citations)
- Keep documentation focused on its intended scope (design docs should focus on concepts, not implementation details)
- Provide context and meaning for technical settings rather than just listing them

Example from configuration documentation:
```yaml
- name: deviceshare
  arguments:
    deviceshare.VGPUEnable: true # Enable virtual GPU support for workloads
    deviceshare.KnowGeometriesCMName: volcano-vgpu-device-config # ConfigMap containing GPU geometry definitions
```

This approach ensures documentation serves its primary purpose: helping users understand and correctly use the system.