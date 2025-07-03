---
title: Prevent null references
description: "Use defensive coding practices to prevent null reference exceptions\
  \ by properly handling potentially null values throughout your code. \n\n1. **Properly\
  \ initialize objects** instead of using default values when instantiation is needed:"
repository: dotnet/runtime
label: Null Handling
language: C#
comments_count: 5
repository_stars: 16578
---

Use defensive coding practices to prevent null reference exceptions by properly handling potentially null values throughout your code. 

1. **Properly initialize objects** instead of using default values when instantiation is needed:
```csharp
// AVOID: Using default without initialization
ArrayBuilder<ProcessInfo> processes = default; // Could cause NullReferenceException when adding items

// PREFER: Proper instantiation
ArrayBuilder<ProcessInfo> processes = new ArrayBuilder<ProcessInfo>();
```

2. **Capture and check results** of methods that might return null before using them:
```csharp
// AVOID: Potential NullReferenceException if ReadLine() returns null
while (!remoteHandle.Process.StandardOutput.ReadLine().EndsWith(message))
{
    Thread.Sleep(20);
}

// PREFER: Capture and check for null
string? line;
while ((line = remoteHandle.Process.StandardOutput.ReadLine()) != null && 
       !line.EndsWith(message))
{
    Thread.Sleep(20);
}
```

3. **Map null values** to appropriate empty structures to maintain consistent behavior:
```csharp
// AVOID: Will throw if context is null
return SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), new ReadOnlySpan<byte>(context));

// PREFER: Properly handle null context
return SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), 
    context == null ? ReadOnlySpan<byte>.Empty : new ReadOnlySpan<byte>(context));
```

4. **Use pattern matching** for more readable and concise null checks:
```csharp
// AVOID: Traditional null check with equality operator
if (setMethod == null || !setMethod.IsPublic)

// PREFER: Modern pattern matching
if (setMethod is null || !setMethod.IsPublic)
```

5. **Combine conditions** using pattern matching for cleaner code:
```csharp
// AVOID: Multiple conditions checked separately
if (changeToken is not null && changeToken is not NullChangeToken)

// PREFER: Combine related checks
if (changeToken is not (null or NullChangeToken))
```

When adding validation in public APIs, favor the built-in helpers like `ArgumentNullException.ThrowIfNull()` over custom throw helpers for better readability and standardization.
