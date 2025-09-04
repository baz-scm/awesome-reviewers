---
title: CSS utility usage
description: Use CSS utility functions and avoid complex inline calculations for better
  maintainability and readability. Prefer `cx()` from useStyles for combining CSS
  classes instead of template literals, and use `css` from antd-style for simple styles
  without design tokens.
repository: lobehub/lobe-chat
label: Code Style
language: TSX
comments_count: 4
repository_stars: 65138
---

Use CSS utility functions and avoid complex inline calculations for better maintainability and readability. Prefer `cx()` from useStyles for combining CSS classes instead of template literals, and use `css` from antd-style for simple styles without design tokens.

**Recommended patterns:**

{% raw %}
```ts
// ✅ Good: Use cx() for combining classes
const { styles, cx } = useStyles();
<div className={cx(styles.promptBox, styles.animatedContainer)} />

// ❌ Avoid: Template literal concatenation
<div className={`${styles.promptBox} ${styles.animatedContainer}`} />

// ✅ Good: Simple CSS without tokens
import { css, cx } from 'antd-style';
const extraTitle = css`
  font-weight: 300;
  white-space: nowrap;
`;
<div className={cx(extraTitle)} style={{ fontSize: extraSize }} />

// ❌ Avoid: Complex CSS calculations that are fragile
style={{ maxHeight: `calc(75vh - 56px - 13px - ${gap}px)` }}
```
{% endraw %}

Avoid overly complex CSS calculations that depend on magic numbers, as they become fragile when layouts change. Consider using CSS inheritance properties or more robust layout solutions instead.
