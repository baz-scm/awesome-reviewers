---
title: Structure CI/CD scripts
description: Improve CI/CD shell scripts' readability and maintainability by using
  appropriate shell script patterns. Use heredocs for multiline output generation
  (especially for YAML configurations) and extract repetitive operations into functions.
  This approach reduces duplication, makes scripts easier to understand, and simplifies
  future updates.
repository: chef/chef
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 7860
---

Improve CI/CD shell scripts' readability and maintainability by using appropriate shell script patterns. Use heredocs for multiline output generation (especially for YAML configurations) and extract repetitive operations into functions. This approach reduces duplication, makes scripts easier to understand, and simplifies future updates.

Example 1 - Using heredocs for multiline output:
```bash
# Instead of multiple echo statements:
echo "- label: \":hammer_and_wrench::docker: $platform\""
echo "  retry:"
echo "    automatic:"
# ...many more echo statements...

# Use heredoc syntax:
cat <<- YAML_CONFIG
- label: ":hammer_and_wrench::docker: $platform"
  retry:
    automatic:
      limit: 1
  key: build-$platform
  # ...rest of configuration...
YAML_CONFIG
```

Example 2 - Extracting repetitive operations into functions:
```bash
# Instead of repeating similar commands:
docker manifest create "chef/chef:${CHANNEL}" \
  --amend "chef/chef:${VERSION}-amd64" \
  --amend "chef/chef:${VERSION}-arm64"
docker manifest push "chef/chef:${CHANNEL}"

# Extract into a reusable function:
function create_and_push_manifest() {
  echo "--- Creating manifest for $2"
  docker manifest create "$1:$2" \
    --amend "$1:${EXPEDITOR_VERSION}-amd64" \
    --amend "$1:${EXPEDITOR_VERSION}-arm64"
  
  echo "--- Pushing manifest for $2"
  docker manifest push "$1:$2"
}

# Then call it multiple times:
create_and_push_manifest "chef/chef" "${EXPEDITOR_TARGET_CHANNEL}"
```
