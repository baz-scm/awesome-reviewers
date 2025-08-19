---
title: Validate before configuration generation
description: Always validate system capabilities and existing configuration state
  before generating new configuration entries or profiles. This prevents unnecessary
  configuration generation, improves startup performance, and avoids presenting unusable
  options to users.
repository: microsoft/terminal
label: Configurations
language: C++
comments_count: 4
repository_stars: 99242
---

Always validate system capabilities and existing configuration state before generating new configuration entries or profiles. This prevents unnecessary configuration generation, improves startup performance, and avoids presenting unusable options to users.

Check system prerequisites, existing installations, and user capabilities before creating configuration entries. For example, when generating profile installers, verify if the target software is already installed or if the installation mechanism is available.

Example from PowerShell profile generation:
```cpp
PowershellCoreProfileGenerator powerShellGenerator{};
_executeGenerator(powerShellGenerator);

const auto isPowerShellInstalled = !powerShellGenerator.GetPowerShellInstances().empty();
if (!isPowerShellInstalled)
{
    // Only generate the installer stub profile if PowerShell isn't installed.
    PowershellInstallationProfileGenerator pwshInstallationGenerator{};
    _executeGenerator(pwshInstallationGenerator);
}
```

This approach prevents generating configuration that would be immediately marked for deletion, reduces UI clutter by hiding irrelevant options, and avoids potential startup performance impacts from unnecessary configuration processing. Always consider whether configuration generation should be conditional based on system state rather than generating everything and cleaning up afterward.