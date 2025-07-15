---
title: Consistent component API patterns
description: Design component APIs with consistent patterns that promote extensibility
  and clear usage. Prefer generic prop structures like `slotProps` over specific props
  (such as `InputProps`, `InputLabelProps`) for better maintainability and consistency
  across components.
repository: mui/material-ui
label: API
language: JavaScript
comments_count: 3
repository_stars: 96063
---

Design component APIs with consistent patterns that promote extensibility and clear usage. Prefer generic prop structures like `slotProps` over specific props (such as `InputProps`, `InputLabelProps`) for better maintainability and consistency across components.

When evolving APIs, provide clear migration paths and documentation to minimize breaking changes. Consider backward compatibility by supporting both old and new patterns during transition periods:

```jsx
// When migrating from specific props to slotProps pattern
// Support both patterns temporarily
{% raw %}
<Autocomplete
    renderInput={(params) => (
        <TextField
            {...params}
            // New pattern
            slotProps={{
                input: {...params.slotProps.input, ref},
            }}
            // Legacy pattern (deprecated but supported)
            InputProps={{...params.InputProps, ref}}
        />
    )}
/>
{% endraw %}
```

For function parameters in component APIs, ensure they match their intended use and are properly typed. Use dedicated comparison functions rather than repurposing other APIs:

```jsx
// Prefer this
isOptionEqualToValue(option, value)

// Over repurposing other functions
getOptionLabel(option) === getOptionLabel(value)
```

When organizing component APIs across packages, establish clear patterns for importing and extension points that allow for customization without causing namespace collisions or duplicating functionality.