---
title: Deprecated API documentation
description: When documenting deprecated APIs, follow consistent practices to provide
  clear guidance to developers while maintaining usability. Use strikethrough formatting
  (~~propertyName~~) to visually indicate deprecation without completely removing
  the documentation. Always include replacement guidance using phrases like "请使用 `xxx`
  替换" or "Please use `xxx` instead"...
repository: ant-design/ant-design
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 95882
---

When documenting deprecated APIs, follow consistent practices to provide clear guidance to developers while maintaining usability. Use strikethrough formatting (~~propertyName~~) to visually indicate deprecation without completely removing the documentation. Always include replacement guidance using phrases like "请使用 `xxx` 替换" or "Please use `xxx` instead" to help developers migrate. For version-specific deprecations, include version constraints such as "版本 >= 5.25.0 时请使用 Statistic.Timer 作为替代方案" to prevent confusion for users on different versions.

Example:
```markdown
| ~~iconPosition~~ | 设置按钮图标组件的位置，请使用 `xxx` 替换 | `start` \| `end` | `start` | 5.17.0 |
```

For major component deprecations, consider using warning blocks with badges:
```markdown
:::warning{title=已废弃}
版本 >= 5.25.0 时请使用 Statistic.Timer 作为替代方案。
:::
```

This approach ensures deprecated APIs remain discoverable for existing users while clearly guiding them toward current alternatives, preventing confusion and supporting smooth migration paths.