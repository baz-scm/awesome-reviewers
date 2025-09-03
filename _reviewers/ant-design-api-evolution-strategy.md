---
title: API evolution strategy
description: When evolving APIs, design for extensibility and provide clear migration
  paths to maintain backward compatibility while improving developer experience.
repository: ant-design/ant-design
label: API
language: Markdown
comments_count: 7
repository_stars: 95882
---

When evolving APIs, design for extensibility and provide clear migration paths to maintain backward compatibility while improving developer experience.

**Key principles:**

1. **Design for future extensibility**: Wrap parameters in objects rather than using simple types when future expansion is likely. For example, prefer `(info: { props }) => Result` over `(props) => Result` to allow adding additional context later without breaking changes.

2. **Provide clear deprecation paths**: When replacing APIs, mark old ones as deprecated with clear migration instructions and warnings. Use strikethrough formatting in documentation: `~~oldAPI~~` with replacement guidance.

3. **Avoid temporary APIs**: Don't introduce new APIs that will be deprecated soon. If a better design is coming in the next major version, wait for it rather than creating intermediate APIs that add confusion.

4. **Standardize naming across components**: When introducing new patterns, apply them consistently. For example, unifying `destroyTooltipOnHide`, `destroyPopupOnHide`, and `destroyOnClose` to a single `destroyOnHidden` pattern across all components.

**Example of good API evolution:**
```typescript
// Before: Simple parameter
filterOption: (inputValue, option): boolean

// After: Extensible object wrapper  
filterOption: (inputValue, option, direction: 'left' | 'right'): boolean

// Documentation shows both with clear migration path
| ~~vertical~~ | 排列方向，与 `orientation` 同时存在，以 `orientation` 优先 | boolean | `false` | 5.21.0 |
| orientation | 排列方向 | `horizontal` \| `vertical` | `horizontal` |  |
```

This approach ensures APIs can evolve gracefully while giving developers clear guidance on migration paths and preventing confusion from temporary or inconsistent naming patterns.