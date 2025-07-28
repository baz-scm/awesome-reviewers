---
title: leverage native configuration features
description: When configuring applications in containerized environments, prefer using
  the application's built-in configuration mechanisms over extensive external configuration
  like multiple volume mounts or environment variable overrides. This approach reduces
  complexity, improves maintainability, and leverages the application's intended configuration
  patterns.
repository: comfyanonymous/ComfyUI
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 83726
---

When configuring applications in containerized environments, prefer using the application's built-in configuration mechanisms over extensive external configuration like multiple volume mounts or environment variable overrides. This approach reduces complexity, improves maintainability, and leverages the application's intended configuration patterns.

For example, instead of mounting multiple individual directories:
```yaml
volumes:
  - "./models:/app/models"
  - "./input:/app/input" 
  - "./temp:/app/output/temp"
  - "./output:/app/output"
  - "./user:/app/user"
  - "./custom_venv:/app/custom_venv"
  - "./custom_nodes:/app/custom_nodes"
```

Use the application's native configuration support with a single base directory and let the application manage its internal structure:
```yaml
volumes:
  - "./data:/home/comfyui/data"
command: ["--base-directory", "/home/comfyui/data"]
```

This pattern applies broadly - look for CLI arguments, configuration files, or environment variables that allow applications to self-organize their directory structure and file locations rather than imposing external mounting schemes. Additionally, avoid mixing conflicting configuration options (like `image` + `build` in Docker Compose) that can lead to unexpected behavior.