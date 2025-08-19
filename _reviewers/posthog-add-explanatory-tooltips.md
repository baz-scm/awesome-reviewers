---
title: Add explanatory tooltips
description: When UI elements have unclear functionality or purpose, add tooltips
  to provide immediate context and explanation. This is especially important for icons,
  checkboxes, and interactive elements where the behavior or consequences aren't immediately
  obvious to users.
repository: PostHog/posthog
label: Documentation
language: TSX
comments_count: 3
repository_stars: 28460
---

When UI elements have unclear functionality or purpose, add tooltips to provide immediate context and explanation. This is especially important for icons, checkboxes, and interactive elements where the behavior or consequences aren't immediately obvious to users.

Tooltips should:
- Explain what the element does in clear, user-friendly language
- Describe any non-obvious consequences or behaviors
- Use terminology consistent with the rest of the UI
- Link to documentation when appropriate (though some tooltip implementations only support strings)

Example from the discussions:
```tsx
<LemonCheckbox
    checked={!!filter.optionalInFunnel}
    onChange={(checked) => {
        updateFilterOptional({
            ...filter,
            optionalInFunnel: checked,
            index,
        })
    }}
    label="Optional step"
    tooltip="When checked, this step won't cause users to drop out of the funnel if they skip it"
/>
```

This practice improves user experience by providing inline documentation that helps users understand functionality without needing to consult external documentation or guess at behavior.