---
title: Simplify complex expressions
description: 'Extract repeated expressions and complex conditional logic into clear,
  readable variables to improve code maintainability and reduce cognitive load.


  **Key practices:**'
repository: ant-design/ant-design
label: Code Style
language: TSX
comments_count: 5
repository_stars: 95882
---

Extract repeated expressions and complex conditional logic into clear, readable variables to improve code maintainability and reduce cognitive load.

**Key practices:**
- Extract repeated expressions (like `Date.now()`, `type === 'countdown'`) into descriptive variables
- Replace nested ternary operators with if-else statements wrapped in `useMemo` for complex logic
- Use destructuring instead of repeated optional chaining (`?.`)
- Simplify conditional expressions by extracting boolean conditions into named variables

**Example:**
```tsx
// ❌ Avoid: Complex nested ternary and repeated expressions
const closePosition = props.closable === false 
  ? undefined 
  : props.closable === undefined || props.closable === true || props.closable?.position === undefined || props.closable?.position === 'start'
    ? 'start' 
    : 'end';

// ❌ Avoid: Repeated expressions and optional chaining
if (down && timestamp < Date.now()) {
  const timeDiff = !down ? Date.now() - timestamp : timestamp - Date.now();
  customCheckboxProps?.onChange?.(e);
}

// ✅ Prefer: Clear variables and structured logic
const closePosition = useMemo(() => {
  const { closable } = props;
  
  if (closable === false) return undefined;
  if (closable === true || closable === undefined) return 'start';
  if (typeof closable === 'object') {
    return closable.position === 'end' ? 'end' : 'start';
  }
  return 'start';
}, [props.closable]);

// ✅ Prefer: Extract repeated expressions and destructure
const now = Date.now();
const isCountdown = type === 'countdown';
const { onChange } = customCheckboxProps || {};

if (isCountdown && timestamp < now) {
  const timeDiff = !isCountdown ? now - timestamp : timestamp - now;
  onChange?.(e);
}
```

This approach makes code more readable, easier to debug, and reduces the likelihood of errors from repeated complex expressions.