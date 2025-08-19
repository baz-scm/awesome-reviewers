---
title: Use descriptive names
description: Choose names that clearly communicate purpose and accurately represent
  what they describe. Avoid ambiguous or misleading names that require additional
  context to understand.
repository: PostHog/posthog
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 28460
---

Choose names that clearly communicate purpose and accurately represent what they describe. Avoid ambiguous or misleading names that require additional context to understand.

Key principles:
- **Be specific**: Use precise terms that indicate the actual purpose or content
- **Avoid generic terms**: Replace vague names with descriptive alternatives
- **Match semantic meaning**: Ensure names accurately reflect what they represent

Examples of improvements:
```python
# Too generic/ambiguous
property_type: str  # What kind of property type?
closure: bool       # What does this boolean represent?
key = name or "default"  # Key for what? Too generic

# More descriptive
property_type: PropertyTypeEnum  # Use enum for type safety
is_factory: bool                 # Clearly indicates factory pattern
registration_key = f"{module_name}#{function_name}"  # Specific and unique

# Misleading names
class FeatureFlagToolkit:  # Actually handles surveys
    pass

class OriginProduct:       # Not all values are products
    pass

# Accurate names  
class SurveyToolkit:       # Accurately describes purpose
    pass

class Origin:              # Broader, more accurate term
    pass
```

When naming is unclear, consider: "Would a new developer understand this name without additional context?" If not, choose a more descriptive alternative.