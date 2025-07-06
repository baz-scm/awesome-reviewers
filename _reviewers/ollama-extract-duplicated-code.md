---
title: Extract duplicated code
description: Identify repeated code segments and extract them into reusable functions
  or variables. This improves maintainability, reduces the risk of inconsistencies,
  and makes the code more concise.
repository: ollama/ollama
label: Code Style
language: Other
comments_count: 2
repository_stars: 145705
---

Identify repeated code segments and extract them into reusable functions or variables. This improves maintainability, reduces the risk of inconsistencies, and makes the code more concise.

Example from shader code:
```
// Before
float theta_base = (float) pos[i2];
// Code that uses theta_base
// ...
// Later in the code, theta_base is calculated again
float theta_base = (float) pos[i2];

// After
float calculate_theta_base(device const int32_t* pos, int i2) {
    return (float) pos[i2];
}
// ...
float theta_base = calculate_theta_base(pos, i2);
// ...
// Later in the code
float theta_base = calculate_theta_base(pos, i2);
```

Even for small code segments, applying the DRY (Don't Repeat Yourself) principle leads to more maintainable code. When you see the same calculation, transformation, or logic repeated, consider extracting it into a function or storing it in a well-named variable. This also makes code more resistant to bugs when changes are needed, as you'll only need to update the logic in one place.