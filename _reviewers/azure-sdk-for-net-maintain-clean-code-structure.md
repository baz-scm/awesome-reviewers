---
title: Maintain clean code structure
description: "Keep code clean and well-organized by:\n1. Removing unnecessary elements:\n\
  \   - Delete commented-out code that is no longer needed\n   - Remove unused using\
  \ directives"
repository: Azure/azure-sdk-for-net
label: Code Style
language: C#
comments_count: 5
repository_stars: 5809
---

Keep code clean and well-organized by:
1. Removing unnecessary elements:
   - Delete commented-out code that is no longer needed
   - Remove unused using directives
   - Avoid redundant code blocks

2. Organizing imports properly:
   - Group using directives consistently (System namespaces first)
   - Use clean imports instead of fully qualified names
   - Keep imports ordered alphabetically

Example - Before:
```csharp
using Azure.Core;
using System.Threading;
using System.Linq.Enumerable;
// Old implementation
// public void OldMethod() {
//    // ...
// }
using System;

public class MyClass 
{
    public void ProcessItems()
    {
        if (System.Linq.Enumerable.Any(items)) // Verbose qualification
        {
            // ...
        }
    }
}
```

After:
```csharp
using System;
using System.Linq;
using System.Threading;
using Azure.Core;

public class MyClass
{
    public void ProcessItems() 
    {
        if (items.Any()) // Clean syntax with proper imports
        {
            // ...
        }
    }
}
```
