---
title: Choose appropriate error mechanisms
description: 'Use the right error handling mechanism for each scenario: exceptions
  for recoverable situations, assertions only for true programming bugs, and consistent
  error codes for API boundaries. Don''t assert unreachable for scenarios that could
  legitimately occur, such as in this example:'
repository: dotnet/runtime
label: Error Handling
language: C++
comments_count: 4
repository_stars: 16578
---

Use the right error handling mechanism for each scenario: exceptions for recoverable situations, assertions only for true programming bugs, and consistent error codes for API boundaries. Don't assert unreachable for scenarios that could legitimately occur, such as in this example:

```cpp
// Instead of this:
if (!BlockRange().TryGetUse(mask, &use))
{
    unreached(); // Bad: this could legitimately occur
}

// Do this:
if (BlockRange().TryGetUse(mask, &use))
{
    use.ReplaceWith(node);
}
else 
{
    node->SetUnusedValue(); // Gracefully handle the case
}
```

Always validate input values to prevent runtime errors like division-by-zero:

```cpp
DWORD cacheSize = CLRConfig::GetConfigValue(CLRConfig::UNSUPPORTED_NativeToILOffsetCacheSize);
if (cacheSize < 1)
{
    cacheSize = 1; // Ensure cache size is at least 1 to prevent division-by-zero
}
```

For API design, use standard error reporting mechanisms rather than boolean out parameters. When throwing exceptions, select appropriate exception types that reflect the nature of the error, such as `PlatformNotSupportedException` for unsupported hardware features instead of failing fast with generic errors.


[
  {
    "discussion_id": "2180071388",
    "pr_number": 116852,
    "pr_file": "src/coreclr/jit/lowerarmarch.cpp",
    "created_at": "2025-07-02T13:28:12+00:00",
    "commented_code": "ContainCheckNode(mod);\n}\n\n//------------------------------------------------------------------------\n// LowerCnsMask: Lower GT_CNS_MSK. Ensure the mask matches a known pattern.\n//               If not then lower to a constant vector.\n//\n// Arguments:\n//    mask - the node to lower\n//\nGenTree* Lowering::LowerCnsMask(GenTreeMskCon* mask)\n{\n    // Try every type until a match is found\n\n    if (mask->IsZero())\n    {\n        return mask->gtNext;\n    }\n\n    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_BYTE, mask->gtSimdMaskVal) != SveMaskPatternNone)\n    {\n        return mask->gtNext;\n    }\n\n    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_SHORT, mask->gtSimdMaskVal) != SveMaskPatternNone)\n    {\n        return mask->gtNext;\n    }\n\n    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_INT, mask->gtSimdMaskVal) != SveMaskPatternNone)\n    {\n        return mask->gtNext;\n    }\n\n    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_LONG, mask->gtSimdMaskVal) != SveMaskPatternNone)\n    {\n        return mask->gtNext;\n    }\n\n    // Not a valid pattern, so cannot be created using ptrue/pfalse. Instead the mask will require\n    // loading from memory. There is no way to load to a predicate from memory using a PC relative\n    // address, so instead use a constant vector plus conversion to mask.\n\n    LABELEDDISPTREERANGE(\"lowering cns mask to cns vector (before)\", BlockRange(), mask);\n\n    LIR::Use use;\n    if (!BlockRange().TryGetUse(mask, &use))\n    {\n        unreached();\n    }",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2180071388",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116852,
        "pr_file": "src/coreclr/jit/lowerarmarch.cpp",
        "discussion_id": "2180071388",
        "commented_code": "@@ -1134,6 +1134,78 @@ void Lowering::LowerModPow2(GenTree* node)\n     ContainCheckNode(mod);\n }\n \n+//------------------------------------------------------------------------\n+// LowerCnsMask: Lower GT_CNS_MSK. Ensure the mask matches a known pattern.\n+//               If not then lower to a constant vector.\n+//\n+// Arguments:\n+//    mask - the node to lower\n+//\n+GenTree* Lowering::LowerCnsMask(GenTreeMskCon* mask)\n+{\n+    // Try every type until a match is found\n+\n+    if (mask->IsZero())\n+    {\n+        return mask->gtNext;\n+    }\n+\n+    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_BYTE, mask->gtSimdMaskVal) != SveMaskPatternNone)\n+    {\n+        return mask->gtNext;\n+    }\n+\n+    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_SHORT, mask->gtSimdMaskVal) != SveMaskPatternNone)\n+    {\n+        return mask->gtNext;\n+    }\n+\n+    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_INT, mask->gtSimdMaskVal) != SveMaskPatternNone)\n+    {\n+        return mask->gtNext;\n+    }\n+\n+    if (EvaluateSimdMaskToPattern<simd16_t>(TYP_LONG, mask->gtSimdMaskVal) != SveMaskPatternNone)\n+    {\n+        return mask->gtNext;\n+    }\n+\n+    // Not a valid pattern, so cannot be created using ptrue/pfalse. Instead the mask will require\n+    // loading from memory. There is no way to load to a predicate from memory using a PC relative\n+    // address, so instead use a constant vector plus conversion to mask.\n+\n+    LABELEDDISPTREERANGE(\"lowering cns mask to cns vector (before)\", BlockRange(), mask);\n+\n+    LIR::Use use;\n+    if (!BlockRange().TryGetUse(mask, &use))\n+    {\n+        unreached();\n+    }",
        "comment_created_at": "2025-07-02T13:28:12+00:00",
        "comment_author": "tannergooding",
        "comment_body": "We shouldn't assert unreached here. There are always scenarios where unused values get preserved, such as min-opts, and so we should prefer the typical pattern of `if (foundUse) { use.ReplaceWith(node); } else { node->SetUnusedValue(); }`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2178499801",
    "pr_number": 117218,
    "pr_file": "src/coreclr/vm/debugdebugger.cpp",
    "created_at": "2025-07-01T20:56:22+00:00",
    "commented_code": "}\n\n#ifndef DACCESS_COMPILE\n// This is an implementation of a cache of the Native->IL offset mappings used by managed stack traces. It exists for the following reasons:\n// 1. When a large server experiences a large number of exceptions due to some other system failing, it can cause a tremendous number of stack traces to be generated, if customers are attempting to log.\n// 2. The native->IL offset mapping is somewhat expensive to compute, and it is not necessary to compute it repeatedly for the same IP.\n// 3. Often when these mappings are needed, the system is under stress, and throwing on MANY different threads with similar callstacks, so the cost of having locking around the cache may be significant.\n//\n// The cache is implemented as a simple hash table, where the key is the IP + fAdjustOffset\n// flag, and the value is the IL offset. We use a version number to indicate when the cache\n// is being updated, and to indicate that a found value is valid, and we use a simple linear\n// probing algorithm to find the entry in the cache.\n//\n// The replacement policy is randomized, and there are s_stackWalkCacheWalk(8) possible buckets to check before giving up.\n//\n// Since the cache entries are greater than a single pointer, we use a simple version locking scheme to protect readers.\n\nstruct StackWalkNativeToILCacheEntry\n{\n    void* ip = NULL; // The IP of the native code\n    uint32_t ilOffset = 0; // The IL offset, with the adjust offset flag set if the native offset was adjusted by STACKWALK_CONTROLPC_ADJUST_OFFSET\n};\n\nstatic LONG s_stackWalkNativeToILCacheVersion = 0;\nstatic DWORD s_stackWalkCacheSize = 0; // This is the total size of the cache (We use a pointer+4 bytes for each entry, so on 64bit platforms 12KB of memory)\nconst DWORD s_stackWalkCacheWalk = 8; // Walk up to this many entries in the cache before giving up\nconst DWORD s_stackWalkCacheAdjustOffsetFlag = 0x80000000; // 2^31, put into the IL offset portion of the cache entry to check if the native offset was adjusted by STACKWALK_CONTROLPC_ADJUST_OFFSET\nstatic StackWalkNativeToILCacheEntry* s_stackWalkCache = NULL;\n\nbool CheckNativeToILCacheCore(void* ip, bool fAdjustOffset, uint32_t* pILOffset)\n{\n    // Check the cache for the IP\n    int hashCode = MixPointerIntoHash(ip);\n    StackWalkNativeToILCacheEntry* cacheTable = VolatileLoad(&s_stackWalkCache);\n    \n    if (cacheTable == NULL)\n    {\n        // Cache is not initialized\n        return false;\n    }\n    DWORD cacheSize = VolatileLoadWithoutBarrier(&s_stackWalkCacheSize);\n    int index = hashCode % cacheSize;\n\n    DWORD count = 0;\n    do\n    {\n        if (VolatileLoadWithoutBarrier(&cacheTable[index].ip) == ip)\n        {\n            // Cache hit\n            uint32_t dwILOffset = VolatileLoad(&cacheTable[index].ilOffset); // It is IMPORTANT that this load have a barrier after it, so that the version check in the containing funciton is safe.\n            if (fAdjustOffset != ((dwILOffset & s_stackWalkCacheAdjustOffsetFlag) == s_stackWalkCacheAdjustOffsetFlag))\n            {\n                continue; // The cache entry did not match on the adjust offset flag, so move to the next entry.\n            }\n\n            dwILOffset &= ~s_stackWalkCacheAdjustOffsetFlag; // Clear the adjust offset flag\n            *pILOffset = dwILOffset;\n            return true;\n        }\n    } while (index = (index + 1) % cacheSize, count++ < s_stackWalkCacheWalk);\n\n    return false; // Not found in cache\n}\n\nbool CheckNativeToILCache(void* ip, bool fAdjustOffset, uint32_t* pILOffset)\n{\n    LIMITED_METHOD_CONTRACT;\n\n    LONG versionStart = VolatileLoad(&s_stackWalkNativeToILCacheVersion);\n\n    if ((versionStart & 1) == 1)\n    {\n        // Cache is being updated, so we cannot use it\n        return false;\n    }\n\n    if (CheckNativeToILCacheCore(ip, fAdjustOffset, pILOffset))\n    {\n        // When looking in the cache, the last load from the cache is a VolatileLoad, which allows a load here to check the version in the cache\n        LONG versionEnd = VolatileLoadWithoutBarrier(&s_stackWalkNativeToILCacheVersion);\n        if (versionEnd == versionStart)\n        {\n            // Cache was not updated while we were checking it, so we can use it\n            return true;\n        }\n    }\n\n    return false;\n}\n\nvoid InsertIntoNativeToILCache(void* ip, bool fAdjustOffset, uint32_t dwILOffset)\n{\n    CONTRACTL\n    {\n        THROWS;\n    }\n    CONTRACTL_END;\n\n    uint32_t dwILOffsetCheck;\n    if (CheckNativeToILCache(ip, fAdjustOffset, &dwILOffsetCheck))\n    {\n        // The entry already exists, so we don't need to insert it again\n        _ASSERTE(dwILOffsetCheck == dwILOffset);\n        return;\n    }\n\n    // Insert the IP and IL offset into the cache\n    \n    LONG versionStart = VolatileLoadWithoutBarrier(&s_stackWalkNativeToILCacheVersion);\n    if ((versionStart & 1) == 1)\n    {\n        // Cache is being updated by someone else, so we can't modify it\n        return;\n    }\n\n    if (versionStart != InterlockedCompareExchange(&s_stackWalkNativeToILCacheVersion, versionStart, versionStart | 1))\n    {\n        // Someone else updated the cache version while we were attempting to take the lock, so abort updating the cache\n        return;\n    }\n    // Now we have the lock, so we can safely update the cache\n\n    if (s_stackWalkCache == NULL)\n    {\n        // Initialize the cache if it is not already initialized\n        DWORD cacheSize = CLRConfig::GetConfigValue(CLRConfig::UNSUPPORTED_NativeToILOffsetCacheSize);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2178499801",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117218,
        "pr_file": "src/coreclr/vm/debugdebugger.cpp",
        "discussion_id": "2178499801",
        "commented_code": "@@ -1013,14 +1013,176 @@ void DebugStackTrace::Element::InitPass1(\n }\n \n #ifndef DACCESS_COMPILE\n+// This is an implementation of a cache of the Native->IL offset mappings used by managed stack traces. It exists for the following reasons:\n+// 1. When a large server experiences a large number of exceptions due to some other system failing, it can cause a tremendous number of stack traces to be generated, if customers are attempting to log.\n+// 2. The native->IL offset mapping is somewhat expensive to compute, and it is not necessary to compute it repeatedly for the same IP.\n+// 3. Often when these mappings are needed, the system is under stress, and throwing on MANY different threads with similar callstacks, so the cost of having locking around the cache may be significant.\n+//\n+// The cache is implemented as a simple hash table, where the key is the IP + fAdjustOffset\n+// flag, and the value is the IL offset. We use a version number to indicate when the cache\n+// is being updated, and to indicate that a found value is valid, and we use a simple linear\n+// probing algorithm to find the entry in the cache.\n+//\n+// The replacement policy is randomized, and there are s_stackWalkCacheWalk(8) possible buckets to check before giving up.\n+//\n+// Since the cache entries are greater than a single pointer, we use a simple version locking scheme to protect readers.\n+\n+struct StackWalkNativeToILCacheEntry\n+{\n+    void* ip = NULL; // The IP of the native code\n+    uint32_t ilOffset = 0; // The IL offset, with the adjust offset flag set if the native offset was adjusted by STACKWALK_CONTROLPC_ADJUST_OFFSET\n+};\n+\n+static LONG s_stackWalkNativeToILCacheVersion = 0;\n+static DWORD s_stackWalkCacheSize = 0; // This is the total size of the cache (We use a pointer+4 bytes for each entry, so on 64bit platforms 12KB of memory)\n+const DWORD s_stackWalkCacheWalk = 8; // Walk up to this many entries in the cache before giving up\n+const DWORD s_stackWalkCacheAdjustOffsetFlag = 0x80000000; // 2^31, put into the IL offset portion of the cache entry to check if the native offset was adjusted by STACKWALK_CONTROLPC_ADJUST_OFFSET\n+static StackWalkNativeToILCacheEntry* s_stackWalkCache = NULL;\n+\n+bool CheckNativeToILCacheCore(void* ip, bool fAdjustOffset, uint32_t* pILOffset)\n+{\n+    // Check the cache for the IP\n+    int hashCode = MixPointerIntoHash(ip);\n+    StackWalkNativeToILCacheEntry* cacheTable = VolatileLoad(&s_stackWalkCache);\n+    \n+    if (cacheTable == NULL)\n+    {\n+        // Cache is not initialized\n+        return false;\n+    }\n+    DWORD cacheSize = VolatileLoadWithoutBarrier(&s_stackWalkCacheSize);\n+    int index = hashCode % cacheSize;\n+\n+    DWORD count = 0;\n+    do\n+    {\n+        if (VolatileLoadWithoutBarrier(&cacheTable[index].ip) == ip)\n+        {\n+            // Cache hit\n+            uint32_t dwILOffset = VolatileLoad(&cacheTable[index].ilOffset); // It is IMPORTANT that this load have a barrier after it, so that the version check in the containing funciton is safe.\n+            if (fAdjustOffset != ((dwILOffset & s_stackWalkCacheAdjustOffsetFlag) == s_stackWalkCacheAdjustOffsetFlag))\n+            {\n+                continue; // The cache entry did not match on the adjust offset flag, so move to the next entry.\n+            }\n+\n+            dwILOffset &= ~s_stackWalkCacheAdjustOffsetFlag; // Clear the adjust offset flag\n+            *pILOffset = dwILOffset;\n+            return true;\n+        }\n+    } while (index = (index + 1) % cacheSize, count++ < s_stackWalkCacheWalk);\n+\n+    return false; // Not found in cache\n+}\n+\n+bool CheckNativeToILCache(void* ip, bool fAdjustOffset, uint32_t* pILOffset)\n+{\n+    LIMITED_METHOD_CONTRACT;\n+\n+    LONG versionStart = VolatileLoad(&s_stackWalkNativeToILCacheVersion);\n+\n+    if ((versionStart & 1) == 1)\n+    {\n+        // Cache is being updated, so we cannot use it\n+        return false;\n+    }\n+\n+    if (CheckNativeToILCacheCore(ip, fAdjustOffset, pILOffset))\n+    {\n+        // When looking in the cache, the last load from the cache is a VolatileLoad, which allows a load here to check the version in the cache\n+        LONG versionEnd = VolatileLoadWithoutBarrier(&s_stackWalkNativeToILCacheVersion);\n+        if (versionEnd == versionStart)\n+        {\n+            // Cache was not updated while we were checking it, so we can use it\n+            return true;\n+        }\n+    }\n+\n+    return false;\n+}\n+\n+void InsertIntoNativeToILCache(void* ip, bool fAdjustOffset, uint32_t dwILOffset)\n+{\n+    CONTRACTL\n+    {\n+        THROWS;\n+    }\n+    CONTRACTL_END;\n+\n+    uint32_t dwILOffsetCheck;\n+    if (CheckNativeToILCache(ip, fAdjustOffset, &dwILOffsetCheck))\n+    {\n+        // The entry already exists, so we don't need to insert it again\n+        _ASSERTE(dwILOffsetCheck == dwILOffset);\n+        return;\n+    }\n+\n+    // Insert the IP and IL offset into the cache\n+    \n+    LONG versionStart = VolatileLoadWithoutBarrier(&s_stackWalkNativeToILCacheVersion);\n+    if ((versionStart & 1) == 1)\n+    {\n+        // Cache is being updated by someone else, so we can't modify it\n+        return;\n+    }\n+\n+    if (versionStart != InterlockedCompareExchange(&s_stackWalkNativeToILCacheVersion, versionStart, versionStart | 1))\n+    {\n+        // Someone else updated the cache version while we were attempting to take the lock, so abort updating the cache\n+        return;\n+    }\n+    // Now we have the lock, so we can safely update the cache\n+\n+    if (s_stackWalkCache == NULL)\n+    {\n+        // Initialize the cache if it is not already initialized\n+        DWORD cacheSize = CLRConfig::GetConfigValue(CLRConfig::UNSUPPORTED_NativeToILOffsetCacheSize);",
        "comment_created_at": "2025-07-01T20:56:22+00:00",
        "comment_author": "Copilot",
        "comment_body": "If the `NativeToILOffsetCacheSize` config value is zero, you will allocate a zero-length cache and later perform `hash % cacheSize`, causing a division-by-zero; add a guard to ensure `cacheSize >= 1`.\n```suggestion\n        DWORD cacheSize = CLRConfig::GetConfigValue(CLRConfig::UNSUPPORTED_NativeToILOffsetCacheSize);\n        if (cacheSize < 1)\n        {\n            cacheSize = 1; // Ensure cache size is at least 1 to prevent division-by-zero\n        }\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "423804786",
    "pr_number": 36267,
    "pr_file": "src/coreclr/src/jit/importer.cpp",
    "created_at": "2020-05-12T15:00:26+00:00",
    "commented_code": "if (mustExpand && (retNode == nullptr))\n    {\n        NO_WAY(\"JIT must expand the intrinsic!\");\n        assert(!\"Unhandled must expand intrinsic, throwing PlatformNotSupportedException\");\n        return impUnsupportedHWIntrinsic(CORINFO_HELP_THROW_PLATFORM_NOT_SUPPORTED, method, sig, mustExpand);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "423804786",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 36267,
        "pr_file": "src/coreclr/src/jit/importer.cpp",
        "discussion_id": "423804786",
        "commented_code": "@@ -4272,7 +4272,8 @@ GenTree* Compiler::impIntrinsic(GenTree*                newobjThis,\n \n     if (mustExpand && (retNode == nullptr))\n     {\n-        NO_WAY(\"JIT must expand the intrinsic!\");\n+        assert(!\"Unhandled must expand intrinsic, throwing PlatformNotSupportedException\");\n+        return impUnsupportedHWIntrinsic(CORINFO_HELP_THROW_PLATFORM_NOT_SUPPORTED, method, sig, mustExpand);",
        "comment_created_at": "2020-05-12T15:00:26+00:00",
        "comment_author": "tannergooding",
        "comment_body": "Previously the JIT would fail fast with `The JIT compiler encountered invalid IL code or an internal limitation.`\r\n\r\nNow, it will assert in debug mode but will `throw PlatformNotSupportedException` at runtime.",
        "pr_file_module": null
      },
      {
        "comment_id": "423899202",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 36267,
        "pr_file": "src/coreclr/src/jit/importer.cpp",
        "discussion_id": "423804786",
        "commented_code": "@@ -4272,7 +4272,8 @@ GenTree* Compiler::impIntrinsic(GenTree*                newobjThis,\n \n     if (mustExpand && (retNode == nullptr))\n     {\n-        NO_WAY(\"JIT must expand the intrinsic!\");\n+        assert(!\"Unhandled must expand intrinsic, throwing PlatformNotSupportedException\");\n+        return impUnsupportedHWIntrinsic(CORINFO_HELP_THROW_PLATFORM_NOT_SUPPORTED, method, sig, mustExpand);",
        "comment_created_at": "2020-05-12T17:12:55+00:00",
        "comment_author": "tannergooding",
        "comment_body": "~This was changed to not use `impUnsupportedHWIntrinsic` and instead use `gtNewMustThrowException` directly.~\r\n\r\n`impUnsupportedHWIntrinsic` was renamed to `impUnsupportedNamedIntrinsic` and moved out of `FEATURE_HW_INTRINSIC`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2109477545",
    "pr_number": 116010,
    "pr_file": "src/coreclr/nativeaot/Runtime/ThunksMapping.cpp",
    "created_at": "2025-05-27T15:14:31+00:00",
    "commented_code": "}\nFCIMPLEND\n\nEXTERN_C void* QCALLTYPE RhAllocateThunksMapping()\nEXTERN_C void* QCALLTYPE RhAllocateThunksMapping(int* isOOM)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2109477545",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116010,
        "pr_file": "src/coreclr/nativeaot/Runtime/ThunksMapping.cpp",
        "discussion_id": "2109477545",
        "commented_code": "@@ -100,13 +100,18 @@ FCIMPL0(int, RhpGetThunkBlockSize)\n }\n FCIMPLEND\n \n-EXTERN_C void* QCALLTYPE RhAllocateThunksMapping()\n+EXTERN_C void* QCALLTYPE RhAllocateThunksMapping(int* isOOM)",
        "comment_created_at": "2025-05-27T15:14:31+00:00",
        "comment_author": "jkotas",
        "comment_body": "It is unusual to return error code via out argument, and only allow that error code to be OOM.\r\n\r\nCan we return proper error code, and return the pointer via `[out]` argument instead?\r\n\r\nThe error code can be an HRESULT or an enum specific to this call. (I know HRESULTs are Windows-specific, but they are part of BCL Exception so they are not going away x-plat, so there is not much value in trying hard to avoid them.)",
        "pr_file_module": null
      },
      {
        "comment_id": "2111355098",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116010,
        "pr_file": "src/coreclr/nativeaot/Runtime/ThunksMapping.cpp",
        "discussion_id": "2109477545",
        "commented_code": "@@ -100,13 +100,18 @@ FCIMPL0(int, RhpGetThunkBlockSize)\n }\n FCIMPLEND\n \n-EXTERN_C void* QCALLTYPE RhAllocateThunksMapping()\n+EXTERN_C void* QCALLTYPE RhAllocateThunksMapping(int* isOOM)",
        "comment_created_at": "2025-05-28T09:13:04+00:00",
        "comment_author": "MichalStrehovsky",
        "comment_body": "Good idea with reusing HRESULT! I didn't like the bool either, but I didn't want to invent a dedicated enum that we need to keep in sync between native and managed.",
        "pr_file_module": null
      },
      {
        "comment_id": "2114772864",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116010,
        "pr_file": "src/coreclr/nativeaot/Runtime/ThunksMapping.cpp",
        "discussion_id": "2109477545",
        "commented_code": "@@ -100,13 +100,18 @@ FCIMPL0(int, RhpGetThunkBlockSize)\n }\n FCIMPLEND\n \n-EXTERN_C void* QCALLTYPE RhAllocateThunksMapping()\n+EXTERN_C void* QCALLTYPE RhAllocateThunksMapping(int* isOOM)",
        "comment_created_at": "2025-05-29T21:24:11+00:00",
        "comment_author": "MichalStrehovsky",
        "comment_body": "@AaronRobinsonMSFT deleted the HRESULT definitions in #115858 so this no longer compiles.\r\n\r\nI would prefer going back to the bool if we don't want HRESULTs anymore.",
        "pr_file_module": null
      },
      {
        "comment_id": "2114808353",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116010,
        "pr_file": "src/coreclr/nativeaot/Runtime/ThunksMapping.cpp",
        "discussion_id": "2109477545",
        "commented_code": "@@ -100,13 +100,18 @@ FCIMPL0(int, RhpGetThunkBlockSize)\n }\n FCIMPLEND\n \n-EXTERN_C void* QCALLTYPE RhAllocateThunksMapping()\n+EXTERN_C void* QCALLTYPE RhAllocateThunksMapping(int* isOOM)",
        "comment_created_at": "2025-05-29T21:55:03+00:00",
        "comment_author": "jkotas",
        "comment_body": "I think it is fine add back what you need to get this to compile. ",
        "pr_file_module": null
      }
    ]
  }
]
