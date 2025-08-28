---
title: Document configuration requirements
description: Always document configuration requirements, environment variables, and
  version specifications to ensure consistent development environments and proper
  system setup. This includes documenting environment variables that enhance workflow,
  specifying exact versions in configuration files, and providing clear setup instructions.
repository: kilo-org/kilocode
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 7302
---

Always document configuration requirements, environment variables, and version specifications to ensure consistent development environments and proper system setup. This includes documenting environment variables that enhance workflow, specifying exact versions in configuration files, and providing clear setup instructions.

For environment variables, document their purpose and usage:
```bash
# Terminal sessions now automatically include a $WORKSPACE_ROOT environment variable 
# that points to your current workspace root directory
cd $WORKSPACE_ROOT
```

For development dependencies, reference version specification files and provide setup guidance:
```markdown
## Prerequisites
1. **Node.js** (LTS version recommended) - see `.nvmrc` for exact version
2. **nvm** - recommended for Node.js version management
```

This ensures developers can reliably reproduce environments and understand how configuration affects system behavior.