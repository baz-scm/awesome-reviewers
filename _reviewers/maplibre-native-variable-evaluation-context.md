---
title: Variable evaluation context
description: Be mindful of when and where environment variables and configuration
  values are evaluated in shell scripts, especially when working across different
  execution contexts (like host vs. container environments). Improper quoting can
  cause variables to be evaluated in the wrong context, leading to unexpected behavior.
repository: maplibre/maplibre-native
label: Configurations
language: Shell
comments_count: 2
repository_stars: 1411
---

Be mindful of when and where environment variables and configuration values are evaluated in shell scripts, especially when working across different execution contexts (like host vs. container environments). Improper quoting can cause variables to be evaluated in the wrong context, leading to unexpected behavior.

For example, when providing instructions for command execution in output messages:

```bash
# INCORRECT - $PWD would evaluate inside the container
echo "  docker run --rm -it -v \"$PWD:/app/\" -v \"$PWD/docker/.cache:/home/$USERNAME/.cache\" maplibre-native-image"

# CORRECT - Using single quotes to preserve $PWD for host evaluation
echo '  docker run --rm -it -v "$PWD:/app/" -v "$PWD/docker/.cache:/home/'"$USERNAME"'/.cache" maplibre-native-image'
```

Similarly, when referencing configuration files in scripts, use variables consistently to avoid hardcoded references:

```bash
# Use variables for file paths
echo "::error::Invalid version '$version' in $(realpath "$version_file")"
```

This approach makes scripts more robust, maintainable, and less prone to configuration errors across different environments.