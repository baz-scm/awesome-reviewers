---
title: Structure configuration options
description: Design and document configuration options (feature flags, environment
  variables, conditional compilation) to be clear, consistent, and maintainable. Group
  related configurations together and avoid unnecessary splits or redundancies. Document
  the purpose and behavior of each option, including valid values and interaction
  effects.
repository: dotnet/runtime
label: Configurations
language: C++
comments_count: 4
repository_stars: 16578
---

Design and document configuration options (feature flags, environment variables, conditional compilation) to be clear, consistent, and maintainable. Group related configurations together and avoid unnecessary splits or redundancies. Document the purpose and behavior of each option, including valid values and interaction effects.

For conditional compilation:
```cpp
// GOOD: Clear hierarchy and purpose
#if !defined(DACCESS_COMPILE) && !defined(FEATURE_CDAC_UNWINDER)
// Code for in-process execution only
#endif

// AVOID: Redundant or overly specific conditions
#if defined(HOST_WINDOWS) // Redundant if file is Windows-only
// ...
#endif
```

For environment variables, provide clear levels with documented behavior:
```cpp
// GOOD: Well-documented configuration with clear levels
// DOTNET_InterpreterMode=0: default, interpreter only used with explicit opt-in
// DOTNET_InterpreterMode=1: use interpreter except for R2R code and System.Private.CoreLib
// DOTNET_InterpreterMode=2: use interpreter for everything except intrinsics
// DOTNET_InterpreterMode=3: full interpreter-only mode, no fallbacks
```

For feature flags, consolidate related functionality until there's a clear need for separation:
```cpp
// PREFER: Single feature flag for closely related functionality
#ifdef FEATURE_JAVAMARSHAL
// All Java interop code including GC bridge
#endif

// AVOID: Premature separation that creates confusing boundaries
#ifdef FEATURE_JAVAMARSHAL
// Some Java interop code
#endif
#ifdef FEATURE_GCBRIDGE
// Closely related GC bridge functionality
#endif
```


[
  {
    "discussion_id": "2063738084",
    "pr_number": 110472,
    "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
    "created_at": "2025-04-28T14:05:28+00:00",
    "commented_code": "#define FIELD_OFFSET(type, field)    ((LONG)__builtin_offsetof(type, field))\n#endif\n\n#ifdef HOST_UNIX\n#define RtlZeroMemory ZeroMemory\n\n#if defined(TARGET_ARM64)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2063738084",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
        "discussion_id": "2063738084",
        "commented_code": "@@ -33,12 +33,13 @@\n #define FIELD_OFFSET(type, field)    ((LONG)__builtin_offsetof(type, field))\n #endif\n \n-#ifdef HOST_UNIX\n-#define RtlZeroMemory ZeroMemory\n-\n #if defined(TARGET_ARM64)",
        "comment_created_at": "2025-04-28T14:05:28+00:00",
        "comment_author": "SwapnilGaikwad",
        "comment_body": "@kunalspathak should this be `if !defined(DACCESS_COMPILE) && defined(TARGET_ARM64)` ? The same on [Line:273](https://github.com/dotnet/runtime/pull/110472/commits/a99f6391e0a6ea4ce6036e8aae87a20b18d2c195#diff-8d8eea22f227bfd092bc709d426a8e62e6d68ec03c03fcd5b36b579bb78ba729R273)",
        "pr_file_module": null
      },
      {
        "comment_id": "2065030223",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
        "discussion_id": "2063738084",
        "commented_code": "@@ -33,12 +33,13 @@\n #define FIELD_OFFSET(type, field)    ((LONG)__builtin_offsetof(type, field))\n #endif\n \n-#ifdef HOST_UNIX\n-#define RtlZeroMemory ZeroMemory\n-\n #if defined(TARGET_ARM64)",
        "comment_created_at": "2025-04-28T23:38:51+00:00",
        "comment_author": "kunalspathak",
        "comment_body": "The only place where `PacStripPtr` is getting used in this file is in ` !defined(DACCESS_COMPILE)`, so doesn't harm to keep it that way...so you might need `#if defined(TARGET_ARM64) && !defined(DACCESS_COMPILE)` here.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2070677876",
    "pr_number": 110472,
    "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
    "created_at": "2025-05-01T19:09:08+00:00",
    "commented_code": "#endif // !defined(DEBUGGER_UNWIND)\n\n//\n// Macros for stripping pointer authentication (PAC) bits.\n//\n#if !defined(DACCESS_COMPILE) && defined(TARGET_ARM64)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2070677876",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
        "discussion_id": "2070677876",
        "commented_code": "@@ -265,16 +269,71 @@ do {\n \n #endif // !defined(DEBUGGER_UNWIND)\n \n-//\n // Macros for stripping pointer authentication (PAC) bits.\n-//\n+#if !defined(DACCESS_COMPILE) && defined(TARGET_ARM64)",
        "comment_created_at": "2025-05-01T19:09:08+00:00",
        "comment_author": "jkotas",
        "comment_body": "```suggestion\r\n#if !defined(DACCESS_COMPILE) && !defined(FEATURE_CDAC_UNWINDER)`\r\n```\r\nWe have two builds of out-of-proc unwinders: DACCESS and CDAC. I think we want to take the offline path for both out-of-proc unwinders. `TARGET_ARM64` should not be needed in the condition once you do enable to the offline path for all out-of-proc unwinders.\r\n\r\n(All similar ifdefs in this file should be changed like this.)",
        "pr_file_module": null
      },
      {
        "comment_id": "2091082579",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/unwinder/arm64/unwinder.cpp",
        "discussion_id": "2070677876",
        "commented_code": "@@ -265,16 +269,71 @@ do {\n \n #endif // !defined(DEBUGGER_UNWIND)\n \n-//\n // Macros for stripping pointer authentication (PAC) bits.\n-//\n+#if !defined(DACCESS_COMPILE) && defined(TARGET_ARM64)",
        "comment_created_at": "2025-05-15T12:40:54+00:00",
        "comment_author": "SwapnilGaikwad",
        "comment_body": "Done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2127147792",
    "pr_number": 116310,
    "pr_file": "src/coreclr/vm/interoplibinterface_shared.cpp",
    "created_at": "2025-06-04T17:58:24+00:00",
    "commented_code": "ObjCMarshalNative::AfterRefCountedHandleCallbacks();\n#endif // FEATURE_OBJCMARSHAL\n}\n\n#ifdef FEATURE_GCBRIDGE\n\nnamespace\n{\n    Volatile<BOOL> g_GCBridgeActive = FALSE;\n    CLREvent* g_bridgeFinished = nullptr;\n\n    void ReleaseGCBridgeArgumentsWorker(\n        _In_ size_t sccsLen,\n        _In_ StronglyConnectedComponent* sccs,\n        _In_ ComponentCrossReference* ccrs)\n    {\n        CONTRACTL\n        {\n            NOTHROW;\n            GC_NOTRIGGER;\n        }\n        CONTRACTL_END;\n\n        // Memory was allocated for the collections by the GC.\n        // See callers of GCToEEInterface::TriggerGCBridge().\n\n        // Free memory in each of the SCCs\n        for (size_t i = 0; i < sccsLen; i++)\n        {\n            free(sccs[i].Context);\n        }\n        free(sccs);\n        free(ccrs);\n    }\n}\n\nbool Interop::IsGCBridgeActive()\n{\n    CONTRACTL\n    {\n        MODE_COOPERATIVE;\n    }\n    CONTRACTL_END;\n\n    return g_GCBridgeActive;\n}\n\nvoid Interop::WaitForGCBridgeFinish()\n{\n    CONTRACTL\n    {\n        MODE_COOPERATIVE;\n    }\n    CONTRACTL_END;\n\n    while (g_GCBridgeActive)\n    {\n        GCX_PREEMP();\n        g_bridgeFinished->Wait(INFINITE, false);\n        // In theory, even though we waited for bridge to finish, because we are in preemptive mode\n        // the thread could have been suspended and another GC could have happened, triggering bridge\n        // processing again. In this case we would wait again for bridge processing.\n    }\n}\n\nvoid Interop::TriggerClientBridgeProcessing(\n    _In_ size_t sccsLen,\n    _In_ StronglyConnectedComponent* sccs,\n    _In_ size_t ccrsLen,\n    _In_ ComponentCrossReference* ccrs)\n{\n    CONTRACTL\n    {\n        NOTHROW;\n        GC_NOTRIGGER;\n    }\n    CONTRACTL_END;\n\n    if (g_GCBridgeActive)\n    {\n        // Release the memory allocated since the GCBridge\n        // is already running and we're not passing them to it.\n        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n        return;\n    }\n\n    bool gcBridgeTriggered;\n\n#ifdef FEATURE_JAVAMARSHAL\n    gcBridgeTriggered = JavaNative::TriggerClientBridgeProcessing(sccsLen, sccs, ccrsLen, ccrs);\n#endif // FEATURE_JAVAMARSHAL\n\n    if (!gcBridgeTriggered)\n    {\n        // Release the memory allocated since the GCBridge\n        // wasn't trigger for some reason.\n        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n        return;\n    }\n\n    // This runs during GC while the world is stopped, no synchronisation required\n    if (!g_bridgeFinished)\n    {\n        g_bridgeFinished = new CLREvent();\n        g_bridgeFinished->CreateManualEvent(false);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2127147792",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/vm/interoplibinterface_shared.cpp",
        "discussion_id": "2127147792",
        "commented_code": "@@ -154,3 +154,142 @@ void Interop::OnAfterGCScanRoots(_In_ bool isConcurrent)\n         ObjCMarshalNative::AfterRefCountedHandleCallbacks();\n #endif // FEATURE_OBJCMARSHAL\n }\n+\n+#ifdef FEATURE_GCBRIDGE\n+\n+namespace\n+{\n+    Volatile<BOOL> g_GCBridgeActive = FALSE;\n+    CLREvent* g_bridgeFinished = nullptr;\n+\n+    void ReleaseGCBridgeArgumentsWorker(\n+        _In_ size_t sccsLen,\n+        _In_ StronglyConnectedComponent* sccs,\n+        _In_ ComponentCrossReference* ccrs)\n+    {\n+        CONTRACTL\n+        {\n+            NOTHROW;\n+            GC_NOTRIGGER;\n+        }\n+        CONTRACTL_END;\n+\n+        // Memory was allocated for the collections by the GC.\n+        // See callers of GCToEEInterface::TriggerGCBridge().\n+\n+        // Free memory in each of the SCCs\n+        for (size_t i = 0; i < sccsLen; i++)\n+        {\n+            free(sccs[i].Context);\n+        }\n+        free(sccs);\n+        free(ccrs);\n+    }\n+}\n+\n+bool Interop::IsGCBridgeActive()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    return g_GCBridgeActive;\n+}\n+\n+void Interop::WaitForGCBridgeFinish()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    while (g_GCBridgeActive)\n+    {\n+        GCX_PREEMP();\n+        g_bridgeFinished->Wait(INFINITE, false);\n+        // In theory, even though we waited for bridge to finish, because we are in preemptive mode\n+        // the thread could have been suspended and another GC could have happened, triggering bridge\n+        // processing again. In this case we would wait again for bridge processing.\n+    }\n+}\n+\n+void Interop::TriggerClientBridgeProcessing(\n+    _In_ size_t sccsLen,\n+    _In_ StronglyConnectedComponent* sccs,\n+    _In_ size_t ccrsLen,\n+    _In_ ComponentCrossReference* ccrs)\n+{\n+    CONTRACTL\n+    {\n+        NOTHROW;\n+        GC_NOTRIGGER;\n+    }\n+    CONTRACTL_END;\n+\n+    if (g_GCBridgeActive)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // is already running and we're not passing them to it.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    bool gcBridgeTriggered;\n+\n+#ifdef FEATURE_JAVAMARSHAL\n+    gcBridgeTriggered = JavaNative::TriggerClientBridgeProcessing(sccsLen, sccs, ccrsLen, ccrs);\n+#endif // FEATURE_JAVAMARSHAL\n+\n+    if (!gcBridgeTriggered)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // wasn't trigger for some reason.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    // This runs during GC while the world is stopped, no synchronisation required\n+    if (!g_bridgeFinished)\n+    {\n+        g_bridgeFinished = new CLREvent();\n+        g_bridgeFinished->CreateManualEvent(false);",
        "comment_created_at": "2025-06-04T17:58:24+00:00",
        "comment_author": "AaronRobinsonMSFT",
        "comment_body": "This should associated with the java code, not in the shared location.",
        "pr_file_module": null
      },
      {
        "comment_id": "2127148287",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/vm/interoplibinterface_shared.cpp",
        "discussion_id": "2127147792",
        "commented_code": "@@ -154,3 +154,142 @@ void Interop::OnAfterGCScanRoots(_In_ bool isConcurrent)\n         ObjCMarshalNative::AfterRefCountedHandleCallbacks();\n #endif // FEATURE_OBJCMARSHAL\n }\n+\n+#ifdef FEATURE_GCBRIDGE\n+\n+namespace\n+{\n+    Volatile<BOOL> g_GCBridgeActive = FALSE;\n+    CLREvent* g_bridgeFinished = nullptr;\n+\n+    void ReleaseGCBridgeArgumentsWorker(\n+        _In_ size_t sccsLen,\n+        _In_ StronglyConnectedComponent* sccs,\n+        _In_ ComponentCrossReference* ccrs)\n+    {\n+        CONTRACTL\n+        {\n+            NOTHROW;\n+            GC_NOTRIGGER;\n+        }\n+        CONTRACTL_END;\n+\n+        // Memory was allocated for the collections by the GC.\n+        // See callers of GCToEEInterface::TriggerGCBridge().\n+\n+        // Free memory in each of the SCCs\n+        for (size_t i = 0; i < sccsLen; i++)\n+        {\n+            free(sccs[i].Context);\n+        }\n+        free(sccs);\n+        free(ccrs);\n+    }\n+}\n+\n+bool Interop::IsGCBridgeActive()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    return g_GCBridgeActive;\n+}\n+\n+void Interop::WaitForGCBridgeFinish()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    while (g_GCBridgeActive)\n+    {\n+        GCX_PREEMP();\n+        g_bridgeFinished->Wait(INFINITE, false);\n+        // In theory, even though we waited for bridge to finish, because we are in preemptive mode\n+        // the thread could have been suspended and another GC could have happened, triggering bridge\n+        // processing again. In this case we would wait again for bridge processing.\n+    }\n+}\n+\n+void Interop::TriggerClientBridgeProcessing(\n+    _In_ size_t sccsLen,\n+    _In_ StronglyConnectedComponent* sccs,\n+    _In_ size_t ccrsLen,\n+    _In_ ComponentCrossReference* ccrs)\n+{\n+    CONTRACTL\n+    {\n+        NOTHROW;\n+        GC_NOTRIGGER;\n+    }\n+    CONTRACTL_END;\n+\n+    if (g_GCBridgeActive)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // is already running and we're not passing them to it.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    bool gcBridgeTriggered;\n+\n+#ifdef FEATURE_JAVAMARSHAL\n+    gcBridgeTriggered = JavaNative::TriggerClientBridgeProcessing(sccsLen, sccs, ccrsLen, ccrs);\n+#endif // FEATURE_JAVAMARSHAL\n+\n+    if (!gcBridgeTriggered)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // wasn't trigger for some reason.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    // This runs during GC while the world is stopped, no synchronisation required\n+    if (!g_bridgeFinished)\n+    {\n+        g_bridgeFinished = new CLREvent();\n+        g_bridgeFinished->CreateManualEvent(false);",
        "comment_created_at": "2025-06-04T17:58:43+00:00",
        "comment_author": "AaronRobinsonMSFT",
        "comment_body": "All of it can be done when the `Initialize()` call is made.",
        "pr_file_module": null
      },
      {
        "comment_id": "2145518519",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/vm/interoplibinterface_shared.cpp",
        "discussion_id": "2127147792",
        "commented_code": "@@ -154,3 +154,142 @@ void Interop::OnAfterGCScanRoots(_In_ bool isConcurrent)\n         ObjCMarshalNative::AfterRefCountedHandleCallbacks();\n #endif // FEATURE_OBJCMARSHAL\n }\n+\n+#ifdef FEATURE_GCBRIDGE\n+\n+namespace\n+{\n+    Volatile<BOOL> g_GCBridgeActive = FALSE;\n+    CLREvent* g_bridgeFinished = nullptr;\n+\n+    void ReleaseGCBridgeArgumentsWorker(\n+        _In_ size_t sccsLen,\n+        _In_ StronglyConnectedComponent* sccs,\n+        _In_ ComponentCrossReference* ccrs)\n+    {\n+        CONTRACTL\n+        {\n+            NOTHROW;\n+            GC_NOTRIGGER;\n+        }\n+        CONTRACTL_END;\n+\n+        // Memory was allocated for the collections by the GC.\n+        // See callers of GCToEEInterface::TriggerGCBridge().\n+\n+        // Free memory in each of the SCCs\n+        for (size_t i = 0; i < sccsLen; i++)\n+        {\n+            free(sccs[i].Context);\n+        }\n+        free(sccs);\n+        free(ccrs);\n+    }\n+}\n+\n+bool Interop::IsGCBridgeActive()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    return g_GCBridgeActive;\n+}\n+\n+void Interop::WaitForGCBridgeFinish()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    while (g_GCBridgeActive)\n+    {\n+        GCX_PREEMP();\n+        g_bridgeFinished->Wait(INFINITE, false);\n+        // In theory, even though we waited for bridge to finish, because we are in preemptive mode\n+        // the thread could have been suspended and another GC could have happened, triggering bridge\n+        // processing again. In this case we would wait again for bridge processing.\n+    }\n+}\n+\n+void Interop::TriggerClientBridgeProcessing(\n+    _In_ size_t sccsLen,\n+    _In_ StronglyConnectedComponent* sccs,\n+    _In_ size_t ccrsLen,\n+    _In_ ComponentCrossReference* ccrs)\n+{\n+    CONTRACTL\n+    {\n+        NOTHROW;\n+        GC_NOTRIGGER;\n+    }\n+    CONTRACTL_END;\n+\n+    if (g_GCBridgeActive)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // is already running and we're not passing them to it.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    bool gcBridgeTriggered;\n+\n+#ifdef FEATURE_JAVAMARSHAL\n+    gcBridgeTriggered = JavaNative::TriggerClientBridgeProcessing(sccsLen, sccs, ccrsLen, ccrs);\n+#endif // FEATURE_JAVAMARSHAL\n+\n+    if (!gcBridgeTriggered)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // wasn't trigger for some reason.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    // This runs during GC while the world is stopped, no synchronisation required\n+    if (!g_bridgeFinished)\n+    {\n+        g_bridgeFinished = new CLREvent();\n+        g_bridgeFinished->CreateManualEvent(false);",
        "comment_created_at": "2025-06-13T16:48:22+00:00",
        "comment_author": "BrzVlad",
        "comment_body": "I'm not sure why this should be associated with java code. Seems to me that even if we were to interop with another garbage collected language via gcbridge, we would still need to do this weak reference waiting for bridge to finish. So I think that `JavaMarshal` is just about the exposed C# api. If we were to add another api for another language, wouldn't it have the exact same format and call the exact same methods in `Interop::*`. Why should we move stuff out of the shared location ?\r\n\r\nHaving said that, the distinction between `FEATURE_JAVAMARSHAL` and `FEATURE_GCBRIDGE` is quite minimal and I feel it just adds confusion currently. In my humble opinion, I would just have everything under `FEATURE_JAVAMARSHAL` instead. If we are to interop with another language in the future, we can easily make the split then, I don't feel like we need it now.",
        "pr_file_module": null
      },
      {
        "comment_id": "2146032081",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/vm/interoplibinterface_shared.cpp",
        "discussion_id": "2127147792",
        "commented_code": "@@ -154,3 +154,142 @@ void Interop::OnAfterGCScanRoots(_In_ bool isConcurrent)\n         ObjCMarshalNative::AfterRefCountedHandleCallbacks();\n #endif // FEATURE_OBJCMARSHAL\n }\n+\n+#ifdef FEATURE_GCBRIDGE\n+\n+namespace\n+{\n+    Volatile<BOOL> g_GCBridgeActive = FALSE;\n+    CLREvent* g_bridgeFinished = nullptr;\n+\n+    void ReleaseGCBridgeArgumentsWorker(\n+        _In_ size_t sccsLen,\n+        _In_ StronglyConnectedComponent* sccs,\n+        _In_ ComponentCrossReference* ccrs)\n+    {\n+        CONTRACTL\n+        {\n+            NOTHROW;\n+            GC_NOTRIGGER;\n+        }\n+        CONTRACTL_END;\n+\n+        // Memory was allocated for the collections by the GC.\n+        // See callers of GCToEEInterface::TriggerGCBridge().\n+\n+        // Free memory in each of the SCCs\n+        for (size_t i = 0; i < sccsLen; i++)\n+        {\n+            free(sccs[i].Context);\n+        }\n+        free(sccs);\n+        free(ccrs);\n+    }\n+}\n+\n+bool Interop::IsGCBridgeActive()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    return g_GCBridgeActive;\n+}\n+\n+void Interop::WaitForGCBridgeFinish()\n+{\n+    CONTRACTL\n+    {\n+        MODE_COOPERATIVE;\n+    }\n+    CONTRACTL_END;\n+\n+    while (g_GCBridgeActive)\n+    {\n+        GCX_PREEMP();\n+        g_bridgeFinished->Wait(INFINITE, false);\n+        // In theory, even though we waited for bridge to finish, because we are in preemptive mode\n+        // the thread could have been suspended and another GC could have happened, triggering bridge\n+        // processing again. In this case we would wait again for bridge processing.\n+    }\n+}\n+\n+void Interop::TriggerClientBridgeProcessing(\n+    _In_ size_t sccsLen,\n+    _In_ StronglyConnectedComponent* sccs,\n+    _In_ size_t ccrsLen,\n+    _In_ ComponentCrossReference* ccrs)\n+{\n+    CONTRACTL\n+    {\n+        NOTHROW;\n+        GC_NOTRIGGER;\n+    }\n+    CONTRACTL_END;\n+\n+    if (g_GCBridgeActive)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // is already running and we're not passing them to it.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    bool gcBridgeTriggered;\n+\n+#ifdef FEATURE_JAVAMARSHAL\n+    gcBridgeTriggered = JavaNative::TriggerClientBridgeProcessing(sccsLen, sccs, ccrsLen, ccrs);\n+#endif // FEATURE_JAVAMARSHAL\n+\n+    if (!gcBridgeTriggered)\n+    {\n+        // Release the memory allocated since the GCBridge\n+        // wasn't trigger for some reason.\n+        ReleaseGCBridgeArgumentsWorker(sccsLen, sccs, ccrs);\n+        return;\n+    }\n+\n+    // This runs during GC while the world is stopped, no synchronisation required\n+    if (!g_bridgeFinished)\n+    {\n+        g_bridgeFinished = new CLREvent();\n+        g_bridgeFinished->CreateManualEvent(false);",
        "comment_created_at": "2025-06-13T20:23:40+00:00",
        "comment_author": "AaronRobinsonMSFT",
        "comment_body": "> I'm not sure why this should be associated with java code.\r\n\r\nSure, but there is no reason to do that here. This is creating an unnecessary branch. The `Initialize()` function is precisely for this kind of initialization. I would this there.\r\n\r\n> In my humble opinion, I would just have everything under FEATURE_JAVAMARSHAL instead.\r\n\r\nOkay, let's do it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2158105119",
    "pr_number": 116769,
    "pr_file": "src/coreclr/interpreter/compiler.cpp",
    "created_at": "2025-06-20T05:51:46+00:00",
    "commented_code": "flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n\n        m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n        {\n            NamedIntrinsic ni = GetNamedIntrinsic(\n                m_compHnd, m_methodHnd, callInfo.hMethod,\n#ifdef FEATURE_JIT\n                true",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2158105119",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116769,
        "pr_file": "src/coreclr/interpreter/compiler.cpp",
        "discussion_id": "2158105119",
        "commented_code": "@@ -2342,6 +2377,23 @@ void InterpCompiler::EmitCall(CORINFO_RESOLVED_TOKEN* pConstrainedToken, bool re\n         flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n \n         m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n+        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n+        {\n+            NamedIntrinsic ni = GetNamedIntrinsic(\n+                m_compHnd, m_methodHnd, callInfo.hMethod,\n+#ifdef FEATURE_JIT\n+                true",
        "comment_created_at": "2025-06-20T05:51:46+00:00",
        "comment_author": "jkotas",
        "comment_body": "We want to be able to test interpreter-only mode on Windows and Linux even with support JIT compiled in. This should be based on some config switch - like `DOTNET_Interpter=*` that should make us to use the interpreter for all methods.",
        "pr_file_module": null
      },
      {
        "comment_id": "2158826147",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116769,
        "pr_file": "src/coreclr/interpreter/compiler.cpp",
        "discussion_id": "2158105119",
        "commented_code": "@@ -2342,6 +2377,23 @@ void InterpCompiler::EmitCall(CORINFO_RESOLVED_TOKEN* pConstrainedToken, bool re\n         flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n \n         m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n+        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n+        {\n+            NamedIntrinsic ni = GetNamedIntrinsic(\n+                m_compHnd, m_methodHnd, callInfo.hMethod,\n+#ifdef FEATURE_JIT\n+                true",
        "comment_created_at": "2025-06-20T12:16:19+00:00",
        "comment_author": "kg",
        "comment_body": "Should I introduce that flag as part of this PR?",
        "pr_file_module": null
      },
      {
        "comment_id": "2159142791",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116769,
        "pr_file": "src/coreclr/interpreter/compiler.cpp",
        "discussion_id": "2158105119",
        "commented_code": "@@ -2342,6 +2377,23 @@ void InterpCompiler::EmitCall(CORINFO_RESOLVED_TOKEN* pConstrainedToken, bool re\n         flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n \n         m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n+        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n+        {\n+            NamedIntrinsic ni = GetNamedIntrinsic(\n+                m_compHnd, m_methodHnd, callInfo.hMethod,\n+#ifdef FEATURE_JIT\n+                true",
        "comment_created_at": "2025-06-20T14:42:32+00:00",
        "comment_author": "jkotas",
        "comment_body": "@janvorli Do you have thoughts how we want to test interpreter-only mode?\r\n\r\nI am thinking we may want to introduce a new dedicated environment variable: `DOTNET_InterpreterMode`:\r\n\r\n`DOTNET_InterpreterMode=0`: default, do not use interpreter except explicit opt-in via `DOTNET_Interpreter`\r\n`DOTNET_InterpreterMode=1`: use interpreter for everything except (1) methods that have R2R compiled code and (2) all code in System.Private.CoreLib. All code in System.Private.CoreLib falls back to JIT if there is no R2R available for it. This can replace the testing mode introduced in https://github.com/dotnet/runtime/pull/116570/files#diff-3e5a329159ca5b2268e62be8a0d776b6092681e9b241210cb4d57e3454816abcR403 since it will cover code in non-entrypoint assemblies too and thus will be more comprehensive. This mode should have good balance between speed and coverage. We may want to use it for running libraries tests with interpreter eventually.\r\n`DOTNET_InterpreterMode=2`: use interpreter for everything except intrinsics. All intrinsics fallback to JIT. Implies `DOTNET_ReadyToRun=0`. I am not sure how much this will be useful in practice, but it sounds like interesting mode to have.\r\n`DOTNET_InterpreterMode=3`: use interpreter for everything, the full interpreter-only mode, no fallbacks to R2R or JIT whatsoever. Implies `DOTNET_ReadyToRun=0`, `DOTNET_EnableHWIntrinsic=0`, \r\n\r\nAn alternative is to piece together solutions from existing environment variables (`DOTNET_Interpreter`, `DOTNET_ReadyToRun`, `DOTNET_EnableHWIntrinsic`, ...), but it may be hard to make it do what we want exactly.\r\n\r\n> Should I introduce that flag as part of this PR?\r\n\r\nI do not have an opinion - it is fine with me to introduce it as part of this PR once we agree on how it should work.",
        "pr_file_module": null
      },
      {
        "comment_id": "2159427105",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116769,
        "pr_file": "src/coreclr/interpreter/compiler.cpp",
        "discussion_id": "2158105119",
        "commented_code": "@@ -2342,6 +2377,23 @@ void InterpCompiler::EmitCall(CORINFO_RESOLVED_TOKEN* pConstrainedToken, bool re\n         flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n \n         m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n+        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n+        {\n+            NamedIntrinsic ni = GetNamedIntrinsic(\n+                m_compHnd, m_methodHnd, callInfo.hMethod,\n+#ifdef FEATURE_JIT\n+                true",
        "comment_created_at": "2025-06-20T17:32:14+00:00",
        "comment_author": "janvorli",
        "comment_body": "@jkotas the approach you have suggested sounds good to me. \r\nI am not sure if the mode 1 would replace the testing mode for coreclr tests though, as it would also interpret the xunit stuff which I assume would be quite slow.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2159562926",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116769,
        "pr_file": "src/coreclr/interpreter/compiler.cpp",
        "discussion_id": "2158105119",
        "commented_code": "@@ -2342,6 +2377,23 @@ void InterpCompiler::EmitCall(CORINFO_RESOLVED_TOKEN* pConstrainedToken, bool re\n         flags = (CORINFO_CALLINFO_FLAGS)(flags | CORINFO_CALLINFO_CALLVIRT);\n \n         m_compHnd->getCallInfo(&resolvedCallToken, pConstrainedToken, m_methodInfo->ftn, flags, &callInfo);\n+        if (callInfo.methodFlags & CORINFO_FLG_INTRINSIC)\n+        {\n+            NamedIntrinsic ni = GetNamedIntrinsic(\n+                m_compHnd, m_methodHnd, callInfo.hMethod,\n+#ifdef FEATURE_JIT\n+                true",
        "comment_created_at": "2025-06-20T19:32:42+00:00",
        "comment_author": "jkotas",
        "comment_body": "> I am not sure if the mode 1 would replace the testing mode for coreclr tests though, as it would also interpret the xunit stuff which I assume would be quite slow.\r\n\r\ncoreclr tests should have the xunit stuff source generated. It should not be a lot of code - it does not run reflection and other heavy lifting like regular xunit.",
        "pr_file_module": null
      }
    ]
  }
]
