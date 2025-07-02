---
title: Explicit API versioning
description: When extending interfaces with new methods or functionality, always implement
  proper versioning to ensure compatibility across different clients. Breaking changes
  should increment major versions, while additive changes should increment minor versions.
  More importantly, implement version checks in your code to gracefully handle compatibility.
repository: dotnet/runtime
label: API
language: Other
comments_count: 2
repository_stars: 16578
---

When extending interfaces with new methods or functionality, always implement proper versioning to ensure compatibility across different clients. Breaking changes should increment major versions, while additive changes should increment minor versions. More importantly, implement version checks in your code to gracefully handle compatibility.

For example, when adding a new method to an interface:

```csharp
// 1. Update the version constant when adding functionality
#define API_INTERFACE_MAJOR_VERSION 2  // Increment for breaking changes
#define API_INTERFACE_MINOR_VERSION 5  // Increment for non-breaking additions

// 2. Implement version checks in code that calls the new functionality
if (runtimeVersion >= API_INTERFACE_MAJOR_VERSION) {
    // Call new method safely knowing it exists
    interface.NewMethod();
} else {
    // Provide alternative implementation or graceful degradation
    FallbackImplementation();
}
```

This approach allows clients on older versions to continue functioning when interacting with newer APIs and vice versa. Remember that versioning is only useful if actively checked during runtime - simply incrementing version numbers without implementing corresponding checks provides no actual compatibility benefits.


[
  {
    "discussion_id": "2147023439",
    "pr_number": 116310,
    "pr_file": "src/coreclr/gc/env/gctoeeinterface.standalone.inl",
    "created_at": "2025-06-14T16:46:52+00:00",
    "commented_code": "return ::GCToEEInterface::RefCountedHandleCallbacks(pObject);\n        }\n\n        void TriggerClientBridgeProcessing(MarkCrossReferencesArgs* args)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2147023439",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/env/gctoeeinterface.standalone.inl",
        "discussion_id": "2147023439",
        "commented_code": "@@ -49,6 +49,11 @@ namespace standalone\n             return ::GCToEEInterface::RefCountedHandleCallbacks(pObject);\n         }\n \n+        void TriggerClientBridgeProcessing(MarkCrossReferencesArgs* args)",
        "comment_created_at": "2025-06-14T16:46:52+00:00",
        "comment_author": "jkotas",
        "comment_body": "Do we need bump `EE_INTERFACE_MAJOR_VERSION` for this this?",
        "pr_file_module": null
      },
      {
        "comment_id": "2150551533",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/env/gctoeeinterface.standalone.inl",
        "discussion_id": "2147023439",
        "commented_code": "@@ -49,6 +49,11 @@ namespace standalone\n             return ::GCToEEInterface::RefCountedHandleCallbacks(pObject);\n         }\n \n+        void TriggerClientBridgeProcessing(MarkCrossReferencesArgs* args)",
        "comment_created_at": "2025-06-16T17:57:54+00:00",
        "comment_author": "BrzVlad",
        "comment_body": "I'm not sure but I don't think so, given this is a new feature entirely (cc @Maoni0). I also don't think there will be a use case for the standalone GC anytime soon on android. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2150562339",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/env/gctoeeinterface.standalone.inl",
        "discussion_id": "2147023439",
        "commented_code": "@@ -49,6 +49,11 @@ namespace standalone\n             return ::GCToEEInterface::RefCountedHandleCallbacks(pObject);\n         }\n \n+        void TriggerClientBridgeProcessing(MarkCrossReferencesArgs* args)",
        "comment_created_at": "2025-06-16T18:03:20+00:00",
        "comment_author": "jkotas",
        "comment_body": "I am worried about the existing standalone GC scenarios that the GC team cares about being broken. As implemented in the PR currently, I do not think you can use new GC with old runtime, and vice versa.",
        "pr_file_module": null
      },
      {
        "comment_id": "2150802205",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/env/gctoeeinterface.standalone.inl",
        "discussion_id": "2147023439",
        "commented_code": "@@ -49,6 +49,11 @@ namespace standalone\n             return ::GCToEEInterface::RefCountedHandleCallbacks(pObject);\n         }\n \n+        void TriggerClientBridgeProcessing(MarkCrossReferencesArgs* args)",
        "comment_created_at": "2025-06-16T20:20:03+00:00",
        "comment_author": "Maoni0",
        "comment_body": "yes. @BrzVlad, as I mentioned before, we definitely care about making the standalone GC work. an example I mentioned was the `LogErrorToHost` method. you can see how that one is added and used. basically you increase the version of the runtime and check for it to know if a particular method exists.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2172423534",
    "pr_number": 116310,
    "pr_file": "src/coreclr/gc/gcinterface.h",
    "created_at": "2025-06-27T16:37:54+00:00",
    "commented_code": "// The minor version of the IGCHeap interface. Non-breaking changes are required\n// to bump the minor version number. GCs and EEs with minor version number\n// mismatches can still interoperate correctly, with some care.\n#define GC_INTERFACE_MINOR_VERSION 4\n#define GC_INTERFACE_MINOR_VERSION 5",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2172423534",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/gcinterface.h",
        "discussion_id": "2172423534",
        "commented_code": "@@ -11,11 +11,11 @@\n // The minor version of the IGCHeap interface. Non-breaking changes are required\n // to bump the minor version number. GCs and EEs with minor version number\n // mismatches can still interoperate correctly, with some care.\n-#define GC_INTERFACE_MINOR_VERSION 4\n+#define GC_INTERFACE_MINOR_VERSION 5",
        "comment_created_at": "2025-06-27T16:37:54+00:00",
        "comment_author": "mangod9",
        "comment_body": "is update to minor version required as well here? ",
        "pr_file_module": null
      },
      {
        "comment_id": "2173134763",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/coreclr/gc/gcinterface.h",
        "discussion_id": "2172423534",
        "commented_code": "@@ -11,11 +11,11 @@\n // The minor version of the IGCHeap interface. Non-breaking changes are required\n // to bump the minor version number. GCs and EEs with minor version number\n // mismatches can still interoperate correctly, with some care.\n-#define GC_INTERFACE_MINOR_VERSION 4\n+#define GC_INTERFACE_MINOR_VERSION 5",
        "comment_created_at": "2025-06-28T05:32:34+00:00",
        "comment_author": "Maoni0",
        "comment_body": "I don't think we actually use the minor version :) nowhere do we use this version for anything (we just log a message if the version in the standalone GC is lower). the original intention for this was that it could be useful to detect some non breaking behavior and do something different but I don't think we've since made use of that.",
        "pr_file_module": null
      }
    ]
  }
]
