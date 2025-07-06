---
title: Consistent naming patterns
description: 'Follow consistent naming conventions throughout the codebase to improve
  readability and maintainability:


  1. **Client property names should be singular**, not plural:'
repository: octokit/octokit.net
label: Naming Conventions
language: C#
comments_count: 14
repository_stars: 2793
---

Follow consistent naming conventions throughout the codebase to improve readability and maintainability:

1. **Client property names should be singular**, not plural:
```csharp
// Good
IObservableOrganizationHooksClient Hook { get; }
// Not
IObservableOrganizationHooksClient Hooks { get; }
```

2. **Method names should include appropriate verbs** and be concise:
```csharp
// Good
Task<string> GetSha1(string owner, string name, string reference);
// Not
Task<string> Sha1(string owner, string name, string reference);
```

3. **Always use nameof() for parameter validation** instead of string literals:
```csharp
// Good
Ensure.ArgumentNotNull(client, nameof(client));
// Not
Ensure.ArgumentNotNull(client, "client");
```

4. **Use descriptive parameter names** that clearly communicate purpose:
```csharp
// Good - clear distinction between concepts
IObservable<Unit> Delete(string owner, string name, int number, int reactionId);
// Not - ambiguous
IObservable<Unit> Delete(string owner, string name, int number, int reaction);

// Good - clearly identifies repository ID
Task<Repository> Transfer(long repositoryId, RepositoryTransfer transfer);
// Not - too generic
Task<Repository> Transfer(long id, RepositoryTransfer transfer);
```

5. **For pull request operations, use 'number'** instead of 'id' to avoid confusion with the internal ID:
```csharp
// Good
IObservable<PullRequest> Get(string owner, string name, int number);
// Not
IObservable<PullRequest> Get(string owner, string name, int pullRequestId);
```

These conventions help maintain a consistent codebase, reduce confusion, and make the API more intuitive for consumers.