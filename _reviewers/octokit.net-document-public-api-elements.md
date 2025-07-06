---
title: Document public API elements
description: Every public API element (classes, methods, properties, constructors)
  must have XML documentation comments that clearly describe its purpose and usage.
  This improves developer experience through IntelliSense and ensures the API is well-documented.
repository: octokit/octokit.net
label: Documentation
language: C#
comments_count: 8
repository_stars: 2793
---

Every public API element (classes, methods, properties, constructors) must have XML documentation comments that clearly describe its purpose and usage. This improves developer experience through IntelliSense and ensures the API is well-documented.

For implementation classes that implement interfaces:
- Use `<inheritdoc />` at the class level to inherit documentation from interfaces
- Don't duplicate documentation in both places to avoid maintenance issues

For method parameters and properties:
- Place important contextual information in `<param>` descriptions rather than `<remarks>` for better IntelliSense visibility
- Use the format: `<param name="paramName">Description (additional context)</param>`

Example:
```csharp
/// <summary>
/// Creates a new repository transfer description.
/// </summary>
/// <param name="newOwner">The new owner of the repository after the transfer.</param>
/// <param name="teamId">A list of team Ids to add to the repository (only applies to Organization owned repositories).</param>
public RepositoryTransfer(string newOwner, IReadOnlyList<int> teamId)
{
    Ensure.ArgumentNotNullOrEmptyString(newOwner, nameof(newOwner));
    Ensure.ArgumentNotNullOrEmptyEnumerable(teamId, nameof(teamId));
    
    NewOwner = newOwner;
    TeamId = teamId;
}
```

Maintain consistency across similar members - if one method overload has documentation, all overloads should be documented with the same level of detail.