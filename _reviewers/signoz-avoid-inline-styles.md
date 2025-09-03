---
title: Avoid inline styles
description: Move all inline styles to dedicated CSS/SCSS files to improve maintainability,
  consistency, and separation of concerns. Inline styles make components harder to
  maintain, reduce reusability, and violate the principle of separating presentation
  from logic.
repository: SigNoz/signoz
label: Code Style
language: TSX
comments_count: 4
repository_stars: 23369
---

Move all inline styles to dedicated CSS/SCSS files to improve maintainability, consistency, and separation of concerns. Inline styles make components harder to maintain, reduce reusability, and violate the principle of separating presentation from logic.

Instead of using inline styles:
```tsx
// ❌ Avoid
<div style={{ 
  display: 'flex', 
  alignItems: 'center', 
  gap: '8px' 
}}>
  <span style={{ color: 'white', fontSize: '14px' }}>
    Status
  </span>
</div>

// ❌ Avoid
<Typography.Paragraph
  style={{
    color: 'var(--text-vanilla-300)',
    fontStyle: 'italic'
  }}
>
```

Create proper CSS classes:
```scss
// ✅ Preferred
.status-container {
  display: flex;
  align-items: center;
  gap: 8px;
  
  .status-text {
    color: white;
    font-size: 14px;
  }
}

.login-prompt {
  color: var(--text-vanilla-300);
  font-style: italic;
}
```

```tsx
// ✅ Preferred
<div className="status-container">
  <span className="status-text">Status</span>
</div>

<Typography.Paragraph className="login-prompt">
```

This approach enables better theming, easier maintenance, improved performance through CSS caching, and cleaner component code that focuses on logic rather than presentation details.