---
title: API parameter semantics
description: Ensure API parameters have clear semantic meaning and avoid sending null
  values for optional fields. When designing API endpoints, use parameter names that
  accurately reflect their purpose and data type. For optional fields, omit them entirely
  from the payload rather than setting them to null, as this creates cleaner API contracts
  and prevents confusion...
repository: PostHog/posthog
label: API
language: TSX
comments_count: 2
repository_stars: 28460
---

Ensure API parameters have clear semantic meaning and avoid sending null values for optional fields. When designing API endpoints, use parameter names that accurately reflect their purpose and data type. For optional fields, omit them entirely from the payload rather than setting them to null, as this creates cleaner API contracts and prevents confusion about field requirements.

Example of what to avoid:
```javascript
// Bad: sending null values for optional fields
setSurveyValue('conditions', {
    ...survey.conditions,
    linkedFlagVariant: null,  // Don't send null for optional fields
});
```

Example of proper approach:
```javascript
// Good: omit optional fields entirely
const { linkedFlagVariant, ...conditions } = survey.conditions;
setSurveyValue('conditions', {
    ...conditions,  // Only include non-null values
});
```

Additionally, ensure parameter names match their expected data types. For example, use `email` parameter when expecting email addresses rather than overloading `distinct_id` with email values, as this maintains semantic clarity and prevents data attribution issues.