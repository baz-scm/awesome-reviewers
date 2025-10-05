---
title: Choose meaningful identifiers
description: All identifiers including parameters, files, functions, and categories
  should clearly communicate their purpose and role. Avoid generic or ambiguous names
  that require additional context to understand.
repository: facebook/yoga
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 18255
---

All identifiers including parameters, files, functions, and categories should clearly communicate their purpose and role. Avoid generic or ambiguous names that require additional context to understand.

For parameters, use descriptive names that indicate what the parameter represents:
```objc
// Poor: generic parameter name
void YGLogAlign(YGLogLevel logLevel, const char * param, YGAlign value)

// Better: descriptive parameter name  
void YGLogAlign(YGLogLevel logLevel, const char * propertyName, YGAlign value)
```

Maintain consistency between related components - if a file is named `YGEnumsPrint.h`, the functions should use `Print` terminology rather than mixing `Print` and `Log`.

For categories and interfaces, ensure the name accurately reflects the current functionality. If an interface evolves beyond being "Private" to include public properties needed by tests, update the name accordingly:
```objc
// When functionality changes, update the name to match
@interface YGLayout ()  // No longer just private
```

This approach improves code readability and reduces the cognitive load for developers trying to understand the codebase.