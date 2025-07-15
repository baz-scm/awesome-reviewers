---
title: Leverage framework defaults
description: Avoid redundant or unnecessary configuration by understanding and utilizing
  default behaviors provided by frameworks and tools. Remove explicit configuration
  when the underlying framework already handles it automatically, which reduces maintenance
  overhead and prevents configuration drift.
repository: shadcn-ui/ui
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 90568
---

Avoid redundant or unnecessary configuration by understanding and utilizing default behaviors provided by frameworks and tools. Remove explicit configuration when the underlying framework already handles it automatically, which reduces maintenance overhead and prevents configuration drift.

For example, when using Storybook with NextJS, you can simplify your configuration by removing redundant settings:

```diff
// .storybook/main.ts
const config: StorybookConfig = {
  stories: ["../stories/**/*.stories.@(js|jsx|ts|tsx|mdx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
-    {
-      name: "@storybook/addon-styling",
-      options: {
-        postCss: true,
-      },
-    },
  ],
}
```

Similarly, when writing utility functions for configuration, prefer simple, direct implementations:

```typescript
// Instead of complex nested conditionals
export function resolveProjectDir(appDir: boolean, srcDir: boolean) {
  if (appDir && srcDir) return "src/app"
  if (appDir) return "app"
  if (srcDir) return "src"
  return ""
}
```

Always research framework capabilities before adding custom configuration to avoid duplicating functionality that's already built-in.