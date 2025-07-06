---
title: Use async/await pattern
description: When designing or documenting API clients, always use the async/await
  pattern rather than blocking calls. Replace code that uses `.GetAwaiter().GetResult()`
  with proper async/await syntax to prevent potential deadlocks and improve application
  responsiveness.
repository: octokit/octokit.net
label: API
language: Markdown
comments_count: 4
repository_stars: 2793
---

When designing or documenting API clients, always use the async/await pattern rather than blocking calls. Replace code that uses `.GetAwaiter().GetResult()` with proper async/await syntax to prevent potential deadlocks and improve application responsiveness.

Example:
```csharp
// Instead of this:
Repository octokitRepo = ghClient.Repository.Get("octokit", "ocktokit.net").GetAwaiter().GetResult();

// Use this:
var octokitRepo = await ghClient.Repository.Get("octokit", "ocktokit.net");
```

Additionally, ensure method names clearly describe their API operation (e.g., 'CreatePullRequestFromFork' instead of 'CreatePR') to improve code readability and API usability.