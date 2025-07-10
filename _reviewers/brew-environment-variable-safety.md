---
title: Environment variable safety
description: 'When configuring environment variables, especially those related to
  paths, implement these safety practices:


  1. Validate path accessibility before use to ensure the environment is properly
  configured'
repository: Homebrew/brew
label: Configurations
language: Shell
comments_count: 3
repository_stars: 44168
---

When configuring environment variables, especially those related to paths, implement these safety practices:

1. Validate path accessibility before use to ensure the environment is properly configured
2. Use dynamic evaluation in shell configurations instead of static values
3. Always add directories (not executables) to PATH variables
4. Consider shell compatibility issues for different environments

```sh
# Validate paths before setting environment variables
if [[ -r "/var/tmp" && -w "/var/tmp" ]]
then
  TEMP_DIR="/var/tmp"
else
  TEMP_DIR="/tmp"
fi

# Use dynamic evaluation in shell config files
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bashrc
# NOT: /opt/homebrew/bin/brew shellenv >> ~/.bashrc

# Add directories (not executables) to PATH
export PATH="/opt/homebrew/bin:$PATH"  # Correct
# NOT: export PATH="/opt/homebrew/bin/brew:$PATH"  # Incorrect

# Handle unset variables in strict mode shells
export PATH="${HOMEBREW_PREFIX}/bin:${HOMEBREW_PREFIX}/sbin${PATH+:$PATH}";
```