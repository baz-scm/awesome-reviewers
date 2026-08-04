---
title: Self-Documenting Calls & Models
description: 'When reviewing code, enforce two style rules:


  1) **Make complex calls self-documenting**: prefer **named arguments** over positional
  parameters, and pass **intent variables** instead of literals when the value is
  logically derived.'
repository: Azure/azure-powershell
label: Code Style
language: C#
comments_count: 3
repository_stars: 4762
---

When reviewing code, enforce two style rules:

1) **Make complex calls self-documenting**: prefer **named arguments** over positional parameters, and pass **intent variables** instead of literals when the value is logically derived.

```csharp
await acquirer.StampPolicyTokenAsync(
    request,
    shouldAcquire: shouldAcquire,
    changeReference: changeReference,
    isWhatIf: false,
    debugMessages: null,
    tokenHttpClient: null,
    cancellationToken: cancelToken);
```

2) **Keep models reusable and organized**: don’t re-define model types that already exist elsewhere (especially when used by stacks/SDKs). Maintain clean structure by placing **each class in its own file**.

These changes improve readability, reduce breakage from signature changes, prevent duplication, and make the codebase easier to navigate and maintain.