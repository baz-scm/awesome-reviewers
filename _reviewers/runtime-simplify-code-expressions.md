---
title: Simplify code expressions
description: Strive for clarity by simplifying code expressions and reducing unnecessary
  complexity. Complex or verbose expressions decrease readability and increase the
  chance of errors during maintenance.
repository: dotnet/runtime
label: Code Style
language: C++
comments_count: 7
repository_stars: 16578
---

Strive for clarity by simplifying code expressions and reducing unnecessary complexity. Complex or verbose expressions decrease readability and increase the chance of errors during maintenance.

Key simplification practices:

1. **Simplify verbose expressions** - Use the most direct syntax possible:
```cpp
// Overly verbose:
PrecodeMachineDescriptor::Init(&(&g_cdacPlatformMetadata)->precode);

// Simplified:
PrecodeMachineDescriptor::Init(&g_cdacPlatformMetadata.precode);
```

2. **Use appropriate types** - Prefer language-native types for internal details:
```cpp
// Less appropriate for internal usage:
Volatile<BOOL> g_GCBridgeActive = FALSE;

// Better:
Volatile<bool> g_GCBridgeActive = false;
```

3. **Reduce nesting** - Flatten nested conditions and blocks when possible:
```cpp
// Highly nested and harder to follow:
if (g_interpModule != NULL)
{
    if (methodInfo->scope == g_interpModule)
        doInterpret = true;
    else
        doInterpret = false;
}

// Flattened and clearer:
bool doInterpret = false;
if ((g_interpModule != NULL) && (methodInfo->scope == g_interpModule))
    doInterpret = true;
```

4. **Use parentheses in logical expressions** per coding guidelines:
```cpp
// Incorrect:
if (ins == INS_rcl_N || ins == INS_rcr_N || ins == INS_rol_N || ins == INS_ror_N)

// Correct:
if ((ins == INS_rcl_N) || (ins == INS_rcr_N) || (ins == INS_rol_N) || (ins == INS_ror_N))
```

5. **Extract helper methods** for repeated patterns:
```cpp
// Repeated pattern:
if (attr == EA_4BYTE)
{
    GetEmitter()->emitIns_R_R_I(INS_addiw, attr, retReg, op1->GetRegNum(), 0);
}
else
{
    GetEmitter()->emitIns_R_R(INS_mov, attr, retReg, op1->GetRegNum());
}

// Extract to helper:
emitMoveIfZeroImmediate(retReg, op1->GetRegNum(), attr);
```

6. **Collapse related conditionals** into helper functions:
```cpp
// Verbose:
if (IsAVXVNNIInstruction(ins) || IsAVXVNNIINT8Instruction(ins) || IsAVXVNNIINT16Instruction(ins))

// Better:
if (IsAvxVnniFamilyInstruction(ins))
```

Simpler code is easier to read, test, and maintain.
