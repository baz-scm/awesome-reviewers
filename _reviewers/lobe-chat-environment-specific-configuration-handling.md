---
title: Environment-specific configuration handling
description: When writing configuration scripts, ensure they handle environment-specific
  differences properly by using predefined path variables and adapting commands for
  different operating systems. Use consistent variable naming for paths that may vary
  between environments, and implement OS detection when commands have different syntax
  across platforms.
repository: lobehub/lobe-chat
label: Configurations
language: Shell
comments_count: 2
repository_stars: 65138
---

When writing configuration scripts, ensure they handle environment-specific differences properly by using predefined path variables and adapting commands for different operating systems. Use consistent variable naming for paths that may vary between environments, and implement OS detection when commands have different syntax across platforms.

For path management, always use predefined variables when referencing configuration files:
```bash
SUB_DIR="docker-compose/local"
FILES=(
    "$SUB_DIR/docker-compose.yml"
    "$SUB_DIR/init_data.json"
    "$SUB_DIR/searxng-settings.yml"
)
```

For cross-platform compatibility, detect the operating system and adapt commands accordingly:
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SED_COMMAND="sed -i ''"
else
    SED_COMMAND="sed -i"
fi
```

This approach ensures configuration scripts work reliably across different environments while maintaining consistency in path handling and command execution.