---
title: Use nullable for optionals
description: When a property or parameter represents an optional value that might
  be absent in requests or responses, use nullable types rather than non-nullable
  types with default values. This clearly distinguishes between "not set" and an explicit
  value, prevents sending unintended defaults in API requests, and properly handles
  missing values in API responses.
repository: octokit/octokit.net
label: Null Handling
language: C#
comments_count: 6
repository_stars: 2793
---

When a property or parameter represents an optional value that might be absent in requests or responses, use nullable types rather than non-nullable types with default values. This clearly distinguishes between "not set" and an explicit value, prevents sending unintended defaults in API requests, and properly handles missing values in API responses.

For boolean flags that are optional in API requests:
```csharp
// INCORRECT: Will always send a value (false by default)
public bool MaintainerCanModify { get; set; }

// CORRECT: Only sent when explicitly set by the user
public bool? MaintainerCanModify { get; set; }
```

For enum-like values that might be absent in API responses:
```csharp
// INCORRECT: Will cause issues when API returns null
public StringEnum<EmailVisibility> Visibility { get; protected set; }

// CORRECT: Properly handles missing values in responses
public StringEnum<EmailVisibility>? Visibility { get; protected set; }
```

This pattern also applies to optional fields in database models, DTOs, and any other context where a value might legitimately be absent. Using nullable types communicates intent clearly and prevents subtle bugs from default values being interpreted as explicit choices.