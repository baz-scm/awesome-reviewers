---
title: Configuration documentation clarity
description: Ensure configuration documentation clearly distinguishes between deployment
  contexts and uses consistent terminology throughout. When documenting configuration
  procedures, explicitly specify the target deployment type (Langflow Desktop vs OSS)
  and platform (macOS vs Windows) to avoid user confusion.
repository: langflow-ai/langflow
label: Configurations
language: Markdown
comments_count: 17
repository_stars: 111046
---

Ensure configuration documentation clearly distinguishes between deployment contexts and uses consistent terminology throughout. When documenting configuration procedures, explicitly specify the target deployment type (Langflow Desktop vs OSS) and platform (macOS vs Windows) to avoid user confusion.

Key requirements:
- **Deployment Context**: Clearly state whether instructions apply to "Langflow Desktop" or "Langflow OSS" 
- **Platform Specificity**: Provide separate sections or clear indicators for macOS and Windows when procedures differ
- **Consistent Terminology**: Use standardized terms like "Terminal" instead of mixing "command line", "PowerShell", and "cmd"
- **Prerequisites Clarity**: Mark configuration requirements as "Required" or "Optional" consistently
- **File Path Formatting**: Use proper path formatting with tilde notation (`~/.langflow`) for cross-platform clarity

Example of improved configuration documentation:

```markdown
## Set environment variables for Langflow Desktop

### macOS
Langflow Desktop for macOS cannot automatically use variables set in your terminal, such as those in `.zshrc` or `.bash_profile`, when launched from the macOS GUI.

To make environment variables available to GUI apps on macOS, you need to use `launchctl` with a `plist` file:

1. Create the `LaunchAgents` directory if it doesn't exist:
```bash
mkdir -p ~/Library/LaunchAgents
```

### Windows  
Langflow Desktop for Windows cannot automatically use variables set in your terminal, such as those defined with `set` in `cmd` or `$env:VAR=...` in PowerShell, when launched from the Windows GUI.

To make environment variables available to the Langflow Desktop app, you must set them at the user or system level using the **System Properties** interface or the Terminal.
```

This approach prevents user confusion about which instructions apply to their specific setup and ensures consistent experience across different deployment scenarios.