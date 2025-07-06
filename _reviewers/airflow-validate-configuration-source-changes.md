---
title: Validate configuration source changes
description: When switching between different configuration sources (like APIs or
  configuration values), ensure data structure compatibility and consistent behavior.
  Configuration endpoints may return different data structures that require proper
  transformation.
repository: apache/airflow
label: Configurations
language: TSX
comments_count: 2
repository_stars: 40858
---

When switching between different configuration sources (like APIs or configuration values), ensure data structure compatibility and consistent behavior. Configuration endpoints may return different data structures that require proper transformation.

For example, instead of this direct replacement:

```typescript
- const { data } = usePluginServiceGetPlugins();
+ const { data } = useConfig("plugins_extra_menu_items");
```

Ensure proper data transformation:

```typescript
- const { data } = usePluginServiceGetPlugins();
+ const menuPluginsData = useConfig("plugins_extra_menu_items");
+ const menuPlugins = menuPluginsData ? transformConfigToPluginFormat(menuPluginsData) : [];
```

Always test your changes with multiple configuration scenarios, and consider backward compatibility when configuration structures are in transition. Verify UI behavior remains consistent across all possible configuration states.