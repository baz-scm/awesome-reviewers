---
title: Use proper configuration tooling
description: When working with configuration files and values, prefer dedicated tools
  and canonical sources over manual text manipulation or secondary configuration files.
  Use language-specific tools for modifications (e.g., `go mod edit -go=1.23` instead
  of `sed` commands on go.mod) and extract configuration values from their primary
  sources rather than derived files.
repository: prometheus/prometheus
label: Configurations
language: Shell
comments_count: 2
repository_stars: 59616
---

When working with configuration files and values, prefer dedicated tools and canonical sources over manual text manipulation or secondary configuration files. Use language-specific tools for modifications (e.g., `go mod edit -go=1.23` instead of `sed` commands on go.mod) and extract configuration values from their primary sources rather than derived files.

For example, instead of:
```bash
# Avoid manual text manipulation
sed -i.bak -E "s/^go [0-9]+\.[0-9]+\.[0-9]+$/go ${NEW_VERSION}.0/" go.mod

# Avoid secondary sources
REQUIRED_GO_VERSION=$(grep 'version:' .promu.yml | awk '{print $2}')
```

Prefer:
```bash
# Use proper tooling
go mod edit -go=${NEW_VERSION}.0

# Use canonical sources
MIN_GO_VERSION=$(awk '/^go / {print $2}' go.mod)
```

This approach reduces fragility, improves maintainability, and ensures configuration changes are handled through proper validation and formatting provided by the dedicated tools.