---
title: Manage side effects properly
description: Avoid performing side effects directly in component render functions.
  Use useEffect for side effects like API calls, DOM manipulations, or state changes
  that should occur after render. Wrap functions with useCallback when they need to
  be optimized or used as dependencies, and use async/await for proper asynchronous
  handling.
repository: langgenius/dify
label: React
language: TSX
comments_count: 2
repository_stars: 114231
---

Avoid performing side effects directly in component render functions. Use useEffect for side effects like API calls, DOM manipulations, or state changes that should occur after render. Wrap functions with useCallback when they need to be optimized or used as dependencies, and use async/await for proper asynchronous handling.

Example of incorrect usage:
```tsx
const I18n: FC<II18nProps> = ({ locale, children }) => {
  // ❌ Side effect in render
  locale && changeLanguage(locale)
  
  return <I18NContext.Provider>...</I18NContext.Provider>
}
```

Example of correct usage:
```tsx
const I18n: FC<II18nProps> = ({ locale, children }) => {
  // ✅ Side effect in useEffect
  useEffect(() => {
    locale && changeLanguage(locale)
  }, [locale])

  // ✅ Function wrapped with useCallback and async/await
  const handleRender = useCallback(async () => {
    await renderFlowchart(code)
  }, [code])
  
  return <I18NContext.Provider>...</I18NContext.Provider>
}
```

This ensures predictable component behavior, prevents unnecessary re-renders, and maintains React's rendering principles.