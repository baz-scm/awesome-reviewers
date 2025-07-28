---
title: Structure documentation comprehensively
description: Documentation should provide complete, practical information while maintaining
  logical organization and information hierarchy. Ensure sections include all necessary
  details for users to successfully implement or understand the feature, and organize
  content to flow logically from basic to advanced concepts.
repository: comfyanonymous/ComfyUI
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 83726
---

Documentation should provide complete, practical information while maintaining logical organization and information hierarchy. Ensure sections include all necessary details for users to successfully implement or understand the feature, and organize content to flow logically from basic to advanced concepts.

When adding new documentation sections:
1. Include complete practical information (not just basic examples)
2. Place sections in logical order based on user journey
3. Group related content together (user-focused vs. developer-focused)

For example, when documenting Docker usage:
```shell
# Complete example with practical details
docker run -it --rm \
  -v /path/to/models:/app/models \
  -v /path/to/output:/app/output \
  -p 8188:8188 \
  -e COMFYUI_PORT=8188 \
  ghcr.io/comfyanonymous/comfyui:latest-cu124
```

Rather than just:
```shell
# Incomplete - only shows how to pull
docker pull ghcr.io/comfyanonymous/comfyui:latest-cu124
```

Organize sections to follow user progression: Introduction → Getting Started → Features → Advanced Topics → Development/Release Information.