---
title: Memory barrier pairing
description: When implementing low-level synchronization mechanisms in multi-threaded
  code, ensure that memory barriers are correctly paired between reader and writer
  operations. For each read barrier, implement a corresponding write barrier to maintain
  memory consistency and prevent race conditions.
repository: dotnet/runtime
label: Concurrency
language: Other
comments_count: 2
repository_stars: 16578
---

When implementing low-level synchronization mechanisms in multi-threaded code, ensure that memory barriers are correctly paired between reader and writer operations. For each read barrier, implement a corresponding write barrier to maintain memory consistency and prevent race conditions.

For example, in ARM64 assembly:
```asm
// Read side
dmb ishld   // Data memory barrier for load operations

// Write side (corresponding barrier needed)
dmb ishst   // Data memory barrier for store operations
```

Consider whether specialized atomic instructions (like `ldar` for loads or `stlr` for stores) might provide the same memory ordering guarantees with potentially better performance in specific scenarios. However, ensure these are implemented at the correct locations in the code to properly maintain the synchronization semantics.


[
  {
    "discussion_id": "2101341553",
    "pr_number": 115746,
    "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
    "created_at": "2025-05-21T23:16:21+00:00",
    "commented_code": ".irp STUB_PAGE_SIZE, 16384, 32768, 65536\n\n    LEAF_ENTRY StubPrecodeCode\\STUB_PAGE_SIZE\n        dmb ishld",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2101341553",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115746,
        "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
        "discussion_id": "2101341553",
        "commented_code": "@@ -120,9 +120,12 @@ LEAF_END_MARKED CallCountingStubCodeTemplate, _TEXT\n     .irp STUB_PAGE_SIZE, 16384, 32768, 65536\n \n     LEAF_ENTRY StubPrecodeCode\\STUB_PAGE_SIZE\n+        dmb ishld",
        "comment_created_at": "2025-05-21T23:16:21+00:00",
        "comment_author": "jkotas",
        "comment_body": "Do we need a counter-part barrier on the writer sides (e.g. in DynamicHelperFixup)?",
        "pr_file_module": null
      },
      {
        "comment_id": "2103480198",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115746,
        "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
        "discussion_id": "2101341553",
        "commented_code": "@@ -120,9 +120,12 @@ LEAF_END_MARKED CallCountingStubCodeTemplate, _TEXT\n     .irp STUB_PAGE_SIZE, 16384, 32768, 65536\n \n     LEAF_ENTRY StubPrecodeCode\\STUB_PAGE_SIZE\n+        dmb ishld",
        "comment_created_at": "2025-05-22T22:23:35+00:00",
        "comment_author": "davidwrighton",
        "comment_body": "Yes. I had written... or at least thought about writing it. I'll have that put together soon.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2104177969",
    "pr_number": 115746,
    "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
    "created_at": "2025-05-23T09:14:03+00:00",
    "commented_code": "IN_PAGE_INDEX = 0\n    .rept STUB_PRECODE_NUM_THUNKS_PER_MAPPING\n\n    dmb ishld",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2104177969",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115746,
        "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
        "discussion_id": "2104177969",
        "commented_code": "@@ -30,11 +30,11 @@\n     IN_PAGE_INDEX = 0\n     .rept STUB_PRECODE_NUM_THUNKS_PER_MAPPING\n \n+    dmb ishld",
        "comment_created_at": "2025-05-23T09:14:03+00:00",
        "comment_author": "janvorli",
        "comment_body": "Do we need a separate barrier instruction? Would it be possible to use ldar instruction instead of the ldr to achieve the same thing?",
        "pr_file_module": null
      },
      {
        "comment_id": "2104479348",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115746,
        "pr_file": "src/coreclr/vm/arm64/thunktemplates.S",
        "discussion_id": "2104177969",
        "commented_code": "@@ -30,11 +30,11 @@\n     IN_PAGE_INDEX = 0\n     .rept STUB_PRECODE_NUM_THUNKS_PER_MAPPING\n \n+    dmb ishld",
        "comment_created_at": "2025-05-23T12:23:39+00:00",
        "comment_author": "davidwrighton",
        "comment_body": "It would need to be an ldar that loads the address of the stub, not an ldar in the stub. ",
        "pr_file_module": null
      }
    ]
  }
]
