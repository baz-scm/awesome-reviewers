---
title: Explicit Null Handling
description: Null/undefined safety should prevent crashes *and* preserve correct semantics.
  Don’t hide missing required inputs with optional chaining or weak fallbacks.
repository: mermaid-js/mermaid
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 87952
---

Null/undefined safety should prevent crashes *and* preserve correct semantics. Don’t hide missing required inputs with optional chaining or weak fallbacks.

**Standards**
1. **Validate required dependencies explicitly**: If an object (e.g., `themeVariables`) is expected to exist, check it and emit a warning/error when it’s missing instead of silently continuing.
2. **Use type-correct defaults, not `null` sentinels**: If downstream code expects a color/string/number/boolean, provide a real default of that type—avoid `?? null` unless the API explicitly supports `null`.
3. **Avoid truthiness logic that changes meaning**: Watch for patterns like `value || true` (it always becomes `true`). Compute booleans with correct precedence.
4. **Be intentional about `null` vs `undefined`**: Use `??` when you only want to treat `null/undefined` as “missing”, and add explicit branches when precedence matters.

**Example pattern**
```ts
function getThemeValue<T>(theme: any, key: string, fallback: T): T {
  if (!theme) {
    console.warn(`Missing themeVariables; using fallback for ${key}`);
    return fallback;
  }
  const value = theme[key];
  if (value === undefined || value === null) {
    console.warn(`Missing theme value ${key}; using fallback`);
    return fallback;
  }
  return value as T;
}

const quadrant1Fill = getThemeValue(themeVariables, 'quadrant1Fill', '#000000');

// Boolean example: avoid `anything || true`
const useHtmlLabels = node.useHtmlLabels ?? evaluate(config.htmlLabels ?? undefined) ?? true;
```

Applying these rules makes UI/config failures easier to diagnose, avoids runtime surprises from invalid sentinel values, and keeps boolean/null semantics correct.