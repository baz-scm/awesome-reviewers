---
title: Explicit over implicit
description: When designing APIs, prioritize explicit parameter identification over
  implicit context. APIs with clear, unambiguous parameters improve implementation,
  maintenance, and usage. Whenever a function could operate on multiple resources
  or have ambiguous behavior, include explicit parameters to clarify the intent.
repository: zed-industries/zed
label: API
language: Other
comments_count: 2
repository_stars: 62119
---

When designing APIs, prioritize explicit parameter identification over implicit context. APIs with clear, unambiguous parameters improve implementation, maintenance, and usage. Whenever a function could operate on multiple resources or have ambiguous behavior, include explicit parameters to clarify the intent.

Example of problematic API:
```
func language-server-workspace-configuration(language-server-id: string, worktree: borrow<worktree>) -> result<option<string>, string>;

// Ambiguous - which language server will receive this configuration?
func additional-language-server-workspace-configuration(language-server-id: string, worktree: borrow<worktree>) -> result<option<string>, string>;
```

Improved API:
```
func language-server-workspace-configuration(language-server-id: string, worktree: borrow<worktree>) -> result<option<string>, string>;

// Explicit - clearly identifies both the source and target language servers
func additional-language-server-workspace-configuration(
    source-language-server-id: string, 
    target-language-server-id: string,
    worktree: borrow<worktree>
) -> result<option<string>, string>;
```

Similarly, when designing RPC calls, ensure parameters are placed on the appropriate side of the interface. Parameters that can only be reasonably handled by the client (like UI focus control or selection) should not be included in server-side RPC parameters but should instead be handled in client-side logic or returned as part of the response.