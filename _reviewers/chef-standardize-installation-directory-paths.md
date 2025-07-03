---
title: Standardize installation directory paths
description: Maintain consistent and separate installation paths for different build
  types to prevent conflicts and improve system organization. Use `/hab` directory
  for Habitat builds and `/opt/chef` for Omnibus installations.
repository: chef/chef
label: Configurations
language: Other
comments_count: 4
repository_stars: 7860
---

Maintain consistent and separate installation paths for different build types to prevent conflicts and improve system organization. Use `/hab` directory for Habitat builds and `/opt/chef` for Omnibus installations.

Key guidelines:
- Place Habitat-built components under `/hab/` directory
- Keep Omnibus installations under `/opt/chef/`
- Use distinct directories for migration tools (e.g., `/hab/migration/`)
- Avoid mixing paths between build types

Example directory structure:
```
# Habitat builds
/hab/
  ├── chef/
  │   └── bin/
  └── migration/
      ├── bin/
      └── bundle/

# Omnibus installations
/opt/chef/
  ├── bin/
  └── bundle/
```

This separation enables:
- Clear distinction between installation types
- Easier cookbook checks and compatibility verification
- Simplified upgrade paths
- Prevention of file conflicts between different versions
