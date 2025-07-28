---
title: Use example configuration files
description: When providing team configuration files that developers might want to
  customize, use `.example` suffixes and implement automatic copying mechanisms to
  avoid conflicts with personal settings.
repository: prettier/prettier
label: Configurations
language: Json
comments_count: 2
repository_stars: 50772
---

When providing team configuration files that developers might want to customize, use `.example` suffixes and implement automatic copying mechanisms to avoid conflicts with personal settings.

This approach prevents team configuration files from overriding individual developer preferences while ensuring new team members get sensible defaults. The pattern works by:

1. Committing configuration files with `.example` extensions (e.g., `settings.example.json`)
2. Adding the actual config file to `.gitignore` 
3. Implementing automatic copying via package scripts when the target file doesn't exist

Example implementation:
```json
// package.json
{
  "scripts": {
    "postinstall": "node -e \"try{fs.existsSync('.vscode/settings.json')||fs.writeFileSync('.vscode/settings.json',fs.readFileSync('.vscode/settings.example.json'))}catch(_){}\""
  }
}
```

This pattern is particularly valuable for IDE settings, environment configurations, and any config files that developers commonly customize. It balances team consistency with individual developer workflow preferences.