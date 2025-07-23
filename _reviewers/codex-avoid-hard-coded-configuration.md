---
title: Avoid hard-coded configuration
description: 'Make scripts and applications flexible by avoiding hard-coded configuration
  values. Instead, allow users to provide configuration through command-line flags,
  environment variables, or configuration files. When updating scripts to use configurable
  parameters:'
repository: openai/codex
label: Configurations
language: Shell
comments_count: 4
repository_stars: 31275
---

Make scripts and applications flexible by avoiding hard-coded configuration values. Instead, allow users to provide configuration through command-line flags, environment variables, or configuration files. When updating scripts to use configurable parameters:

1. Prefer explicit flag-based interfaces over positional arguments
2. Use descriptive names for flags, especially those with security implications (e.g., `--dangerously-allow-network-outbound`)
3. Validate configuration values before use to prevent errors
4. Maintain backward compatibility when possible
5. Include helpful usage documentation

Example:
```bash
#!/usr/bin/env bash
# Parse optional flags with descriptive names
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dangerously-allow-network-outbound)
      ALLOW_OUTBOUND=true
      shift
      ;;
    --work_dir)
      if [ -z "$2" ]; then
        echo "Error: --work_dir flag provided but no directory specified."
        exit 1
      fi
      WORK_DIR="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $(basename "$0") [--dangerously-allow-network-outbound] [--work_dir directory]"
      exit 0
      ;;
    *)
      # Handle other arguments or commands
      break
      ;;
  esac
done

# Validate environment variables before use
if [ -z "$ALLOWED_DOMAINS" ]; then
  echo "Error: ALLOWED_DOMAINS is empty."
  exit 1
fi
```