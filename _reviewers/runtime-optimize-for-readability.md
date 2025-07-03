---
title: Optimize for readability
description: 'Write code that clearly communicates intent by using appropriate naming
  and formatting techniques. Improve readability by:


  1. Replacing magic numbers and string literals with named constants:'
repository: dotnet/runtime
label: Code Style
language: C#
comments_count: 11
repository_stars: 16578
---

Write code that clearly communicates intent by using appropriate naming and formatting techniques. Improve readability by:

1. Replacing magic numbers and string literals with named constants:
```csharp
// Instead of:
if (valueType.Module == SystemModule && valueType.Name.StartsWith("ValueTuple`", StringComparison.OrdinalIgnoreCase))

// Prefer:
private const string ValueTuplePrefix = "ValueTuple`";
if (valueType.Module == SystemModule && valueType.Name.StartsWith(ValueTuplePrefix, StringComparison.OrdinalIgnoreCase))
```

2. Using explicit types instead of `var` when the type isn't obvious:
```csharp
// Instead of:
var relativePathToSpec = GetFilteredFileSpecs(fileSpecs);

// Prefer:
Dictionary<string, FileSpec> relativePathToSpec = GetFilteredFileSpecs(fileSpecs);
```

3. Using standard language patterns like `Array.Empty<byte>()` over raw literals:
```csharp
// Instead of:
SHA256.Create().ComputeHash([])

// Prefer:
SHA256.Create().ComputeHash(Array.Empty<byte>())
```

4. Using pattern matching for null checks:
```csharp
// Instead of:
if (m_getterMethod != null && m_getterMethod.IsVirtual)

// Prefer:
if (m_getterMethod is not null && m_getterMethod.IsVirtual)
```

5. Adding parentheses to clarify operator precedence in complex conditionals:
```csharp
// Instead of:
bool taken = (opcode is ILOpcode.brtrue or ILOpcode.brtrue_s && val.Value != 0)
    || (opcode is ILOpcode.brfalse or ILOpcode.brfalse_s && val.Value == 0);

// Prefer:
bool taken = ((opcode is ILOpcode.brtrue or ILOpcode.brtrue_s) && val.Value != 0)
    || ((opcode is ILOpcode.brfalse or ILOpcode.brfalse_s) && val.Value == 0);
```

6. Using operators for more concise code when available:
```csharp
// Instead of:
Vector256<int> result = Vector256.And(Vector256.LoadUnsafe(ref left, i), Vector256.LoadUnsafe(ref right, i));

// Prefer:
Vector256<int> result = Vector256.LoadUnsafe(ref left, i) & Vector256.LoadUnsafe(ref right, i);
```
