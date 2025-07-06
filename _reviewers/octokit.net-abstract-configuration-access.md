---
title: Abstract configuration access
description: Use abstraction layers to access configuration settings rather than accessing
  environment variables, feature flags, or other configuration sources directly. This
  improves maintainability by centralizing configuration logic, enabling validation,
  and simplifying testing.
repository: octokit/octokit.net
label: Configurations
language: C#
comments_count: 3
repository_stars: 2793
---

Use abstraction layers to access configuration settings rather than accessing environment variables, feature flags, or other configuration sources directly. This improves maintainability by centralizing configuration logic, enabling validation, and simplifying testing.

**Why it matters:**
- Centralizes configuration management in a single location
- Enables validation of configuration values
- Makes it easier to mock configuration in tests
- Provides a clean API for configuration consumers

**Implementation:**

Instead of:
```csharp
var organization = Environment.GetEnvironmentVariable("OCTOKIT_GITHUBORGANIZATION");
```

Prefer:
```csharp
var organization = Helper.Organization; // Abstracted access to environment variable
```

For environment-specific code, use consistent preprocessor directives and centralize format strings:
```csharp
var format = 
#if !HAS_ENVIRONMENT
    "{0} ({1}; {2}; {3}; Octokit {4})";
#else
    "{0} ({1} {2}; {3}; {4}; Octokit {5})";
#endif

// Use format variable instead of duplicating the format string
```

When creating clients that require specific configuration constraints:
```csharp
public EnterpriseSpecificClient(IApiConnection apiConnection)
{
    // Validate configuration constraints early
    if (!IsEnterpriseUrl(apiConnection.Connection.BaseUrl))
    {
        throw new InvalidOperationException(
            "This client only works with GitHub Enterprise URLs.");
    }
    
    // Rest of constructor...
}
```