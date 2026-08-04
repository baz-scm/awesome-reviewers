---
title: API versioning and client methods
description: 'When changing API clients, keep API versioning and HTTP operation semantics
  explicit and isolated.


  **Do**

  - **Scope ApiVersion changes** to only the new operation(s). If a shared client
  is used by many cmdlets, either (a) split the client, (b) wrap the new operation
  in a dedicated client/operation class, or (c) prove all affected cmdlets are covered.'
repository: Azure/azure-powershell
label: API
language: C#
comments_count: 5
repository_stars: 4762
---

When changing API clients, keep API versioning and HTTP operation semantics explicit and isolated.

**Do**
- **Scope ApiVersion changes** to only the new operation(s). If a shared client is used by many cmdlets, either (a) split the client, (b) wrap the new operation in a dedicated client/operation class, or (c) prove all affected cmdlets are covered.
- **Validate availability by cloud/sovereign environment** (and confirm scenario/recording targets) before switching preview ApiVersions broadly.
- **Expose explicit SDK methods per operation/verb**. Don’t add “GET method + flag that triggers POST” patterns; create separate methods (e.g., `GetWhatIfResult(...)` vs `PostWhatIfResult(...)`).
- **Split SDKs by resource family when it reduces regression risk** (e.g., separate “stacks what-if” SDK/client) so changes don’t unintentionally affect other resource types.
- **Add tests for request/response semantics** whenever you change payload models or request verbs (GET/POST/PUT/PATCH), especially for update flows.

**Don’t**
- Don’t change a shared client’s ApiVersion for unrelated cmdlets without regenerated regression coverage and cross-environment validation.
- Don’t rely on flags to switch HTTP verbs or operation behavior inside a single “GET” method.

**Example (separate methods instead of verb flags)**
```csharp
// Bad: GET method with a flag that sometimes POSTs
public PSDeploymentStackWhatIfResult GetDeploymentStackWhatIfResult(string rg, string name, bool withPropertyChanges)
{
    // if (withPropertyChanges) POST...
}

// Good: explicit methods
public PSDeploymentStackWhatIfResult GetDeploymentStackWhatIfResult(string rg, string name)
{
    // GET only
}

public PSDeploymentStackWhatIfResult PostDeploymentStackWhatIfResult(string rg, string name)
{
    // POST only
}
```

Use this standard for any API-related PR that touches: (1) ApiVersion, (2) endpoint/verb selection, or (3) SDK client method boundaries.