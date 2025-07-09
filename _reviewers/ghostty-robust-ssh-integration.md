---
title: Robust SSH integration
description: 'When implementing SSH integration in your application, follow these
  practices to ensure reliability across different systems:


  1. **Preserve user context**: Include user information in SSH target identification,
  as many operations (like terminfo installation) write to user-specific directories.'
repository: ghostty-org/ghostty
label: Networking
language: Other
comments_count: 6
repository_stars: 32864
---

When implementing SSH integration in your application, follow these practices to ensure reliability across different systems:

1. **Preserve user context**: Include user information in SSH target identification, as many operations (like terminfo installation) write to user-specific directories.

```bash
# AVOID: Only capturing hostname
ssh_hostname="$(ssh -G "$@" | grep hostname | cut -d' ' -f2)"

# BETTER: Capture full user@host target
ssh_config=$(ssh -G "$@" 2>/dev/null)
while IFS=' ' read -r key value; do
  case "$key" in
    user) ssh_user="$value" ;;
    hostname) ssh_hostname="$value" ;;
  esac
done < <(ssh -G "$@" 2>/dev/null)
ssh_target="${ssh_user}@${ssh_hostname}"
```

2. **Minimize environment changes**: Avoid modifying the local environment when possible. For environment variable overrides, set them at the command level instead of exporting and restoring:

```bash
# AVOID: Modifying and restoring environment
export TERM="$ssh_term_override"
command ssh "${ssh_opts[@]}" "$@"
export TERM="$original_term"

# BETTER: Override at command level
command TERM="$ssh_term_override" ssh "${ssh_opts[@]}" "$@"
```

3. **Clarify tool locations**: Document clearly which tools must exist locally versus remotely. For SSH operations like terminfo installation, be explicit about requirements:

```bash
# Local check (infocmp needed locally)
if ! command -v infocmp >/dev/null 2>&1; then
  echo "Warning: infocmp command not available locally for terminfo export." >&2
  return 1
fi

# Remote check (tic needed remotely)
if ! ssh "$host" "command -v tic >/dev/null 2>&1"; then
  echo "Warning: tic command not available on remote host for terminfo installation." >&2
  return 1
fi
```

4. **Use minimal commands**: Remove unnecessary operations in remote commands to improve reliability and performance:

```bash
# AVOID: Redundant commands
ssh "$host" 'mkdir -p ~/.terminfo/x 2>/dev/null && tic -x -o ~/.terminfo /dev/stdin'

# BETTER: Let tic handle directory creation
ssh "$host" 'tic -x - 2>/dev/null'
```

5. **Understand SSH options**: Use SSH options like SendEnv and SetEnv appropriately based on their behavior across different server configurations.