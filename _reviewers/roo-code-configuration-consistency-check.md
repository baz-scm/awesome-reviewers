---
title: Configuration consistency check
description: 'Ensure that configuration files and settings are consistent with their
  intended functionality and maintain portability across different environments. '
repository: RooCodeInc/Roo-Code
label: Configurations
language: Other
comments_count: 4
repository_stars: 17288
---

Ensure that configuration files and settings are consistent with their intended functionality and maintain portability across different environments. 

Key aspects to verify:
1. **Avoid hardcoded paths** - Use relative paths, environment variables, or configuration variables instead of absolute paths
2. **Align permissions with functionality** - Make sure that permissions or access groups in configurations match the tools and capabilities referenced in descriptions
3. **Properly configure special files** - Use appropriate attributes and settings for files that require special handling

Example of improving path configuration:
```javascript
// Problematic - hardcoded absolute path
const templatePath = 'C:\\Users\\orphe\\Downloads\\playwright-mcp.yaml';

// Better - relative path using Node.js path module
const templatePath = path.join(__dirname, 'playwright-mcp.yaml');
```

Example of aligning permissions with functionality:
```yaml
# Problematic - empty groups but roleDefinition mentions using tools
roleDefinition: |-
  You can use the `new_task` tool...
groups: []

# Better - groups include all necessary permissions
roleDefinition: |-
  You can use the `new_task` tool...
groups:
  - read
  - edit
  - command
  - new_task
```