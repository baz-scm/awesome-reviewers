---
title: Specify security requirements
description: Always explicitly declare security requirements and provide clear security
  guidance in both configuration files and user-facing content. When operations require
  elevated privileges, specify the security context to ensure proper UAC prompting.
  When features have security implications, include explanatory text to help users
  make informed decisions.
repository: microsoft/terminal
label: Security
language: Other
comments_count: 2
repository_stars: 99242
---

Always explicitly declare security requirements and provide clear security guidance in both configuration files and user-facing content. When operations require elevated privileges, specify the security context to ensure proper UAC prompting. When features have security implications, include explanatory text to help users make informed decisions.

For configuration files requiring elevation:
```yaml
- resource: Microsoft.Windows.Developer/DeveloperMode
  directives:
    description: Enable Developer Mode
    allowPrerelease: true
    securityContext: elevated  # Required for UAC prompting
```

For user-facing security features, provide context about the security implications:
```xml
<data name="Globals_WarnAboutMultiLinePaste.HelpText" xml:space="preserve">
  <value>If your shell does not support "bracketed paste" mode, we recommend setting this to "Always" for security reasons.</value>
</data>
```

This practice ensures that security requirements are transparent to both the system (for proper privilege handling) and users (for informed decision-making), reducing the risk of security misconfigurations or unintended security bypasses.