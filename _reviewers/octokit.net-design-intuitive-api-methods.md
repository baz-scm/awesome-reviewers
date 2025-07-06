---
title: Design intuitive API methods
description: 'When designing API methods, prioritize intuitive usage patterns and
  backwards compatibility. Follow these guidelines:


  1. Order parameters from required to optional, maintaining consistency across overloads:'
repository: octokit/octokit.net
label: API
language: C#
comments_count: 5
repository_stars: 2793
---

When designing API methods, prioritize intuitive usage patterns and backwards compatibility. Follow these guidelines:

1. Order parameters from required to optional, maintaining consistency across overloads:
```csharp
// Good - consistent parameter order
public Task<RepositoryContent> GetAllContents(string owner, string name, string reference);
public Task<RepositoryContent> GetAllContents(string owner, string name, string reference, string path);

// Bad - inconsistent parameter order
public Task<RepositoryContent> GetAllContents(string owner, string name, string path, string reference);
```

2. Use clear, singular property names for sub-clients:
```csharp
// Good
public IObservableTeamDiscussionsClient Discussion { get; }

// Bad 
public IObservableTeamDiscussionsClient TeamDiscussion { get; }
```

3. When adding new parameters or changing existing ones:
- Add new overloads rather than modifying existing method signatures
- Keep existing methods for backwards compatibility
- Mark deprecated methods with [Obsolete] attribute and direct users to new methods

4. Include clear XML documentation describing parameter usage and any authentication requirements

This approach ensures APIs remain intuitive to use while maintaining compatibility for existing consumers.