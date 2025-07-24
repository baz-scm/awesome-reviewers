---
title: Prevent silent failures
description: Ensure that user actions and validations provide clear feedback rather
  than failing silently. When operations cannot be performed, disable UI elements
  or provide explicit error messages to inform users of the system state.
repository: argoproj/argo-cd
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 20149
---

Ensure that user actions and validations provide clear feedback rather than failing silently. When operations cannot be performed, disable UI elements or provide explicit error messages to inform users of the system state.

For UI interactions, disable buttons or controls when the underlying operation cannot be executed:
```ts
{
    iconClassName: classNames('fa fa-redo', {'status-icon--spin': !!refreshing}),
    title: <ActionMenuItem actionLabel='Invalidate Cache' />,
    disabled: !!refreshing, // Prevent silent ignoring of clicks
    action: () => {
        if (!refreshing) {
            // perform action
        }
    }
}
```

For validation scenarios, implement comprehensive validation that returns specific error messages for each field:
```ts
validate: vals => {
    return (action.params || []).reduce((acc, param) => {
        acc[param.name] = vals[param.name] && vals[param.name].match(param.type) ?
            undefined : `required format: ${param.type}`;
        return acc;
    }, {});
}
```

This approach prevents user confusion and ensures that all failure scenarios are communicated clearly rather than being silently ignored.