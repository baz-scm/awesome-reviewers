---
title: Avoid unintentional defaults
description: When designing configuration interfaces, be intentional about default
  values and consider their impact on user behavior and data quality. Avoid defaults
  that users might unconsciously accept without proper consideration, especially for
  critical settings.
repository: hyprwm/Hyprland
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 28863
---

When designing configuration interfaces, be intentional about default values and consider their impact on user behavior and data quality. Avoid defaults that users might unconsciously accept without proper consideration, especially for critical settings.

For form configurations, consider forcing explicit user choices rather than providing convenient defaults that might be ignored. Users often have "attention problems and just ignore" default selections, leading to poor data quality where values are not "hand picked and relevant."

Example approaches:
- Use `multiple: true` in dropdowns to prevent default selection and force explicit choice
- Clearly communicate when configuration values are required vs optional, as changing these requirements can have broader system implications
- Consider the downstream impact of configuration changes before relaxing or tightening requirements

This principle helps ensure that configuration values reflect deliberate user decisions rather than oversight or convenience.