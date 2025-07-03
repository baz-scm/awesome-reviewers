---
title: Copy external string inputs
description: When storing string pointers from external sources (like command-line
  arguments), always validate the input and create managed copies to prevent null
  references and lifetime issues. This practice ensures that your stored references
  remain valid throughout your program's execution and prevents potential crashes
  from null or invalid pointers.
repository: JetBrains/kotlin
label: Null Handling
language: C++
comments_count: 2
repository_stars: 50857
---

When storing string pointers from external sources (like command-line arguments), always validate the input and create managed copies to prevent null references and lifetime issues. This practice ensures that your stored references remain valid throughout your program's execution and prevents potential crashes from null or invalid pointers.

Follow these steps when handling external string inputs:
1. Verify the pointer is valid (check boundary conditions)
2. Ensure the string isn't empty when needed
3. Create a copy with reasonable size limits for persistent storage

```cpp
// Unsafe approach:
kotlin::programName = argv[0]; // May cause crashes if argc=0 or lifetime issues later

// Safe approach:
if (argc > 0 && argv[0][0] != '\0') {
  kotlin::programName = strndup(argv[0], 4096); // Creates bounded copy with independent lifetime
}
```

This approach prevents crashes from invalid pointers, protects against potential buffer issues by limiting string length, and eliminates lifetime concerns by managing your own copy of the data.


[
  {
    "discussion_id": "1581157906",
    "pr_number": 5281,
    "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
    "created_at": "2024-04-26T14:58:47+00:00",
    "commented_code": "//--- Setup args --------------------------------------------------------------//\n\nOBJ_GETTER(setupArgs, int argc, const char** argv) {\n  kotlin::programName = argv[0];",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1581157906",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
        "discussion_id": "1581157906",
        "commented_code": "@@ -30,6 +30,8 @@ using namespace kotlin;\n //--- Setup args --------------------------------------------------------------//\n \n OBJ_GETTER(setupArgs, int argc, const char** argv) {\n+  kotlin::programName = argv[0];",
        "comment_created_at": "2024-04-26T14:58:47+00:00",
        "comment_author": "SvyatoslavScherbina",
        "comment_body": "Is `argv[0]` guaranteed to live long enough? What will happen if some code accesses `kotlin::programName` after the `main` function finishes?\r\nIs `argv` guaranteed to always have at least one element?",
        "pr_file_module": null
      },
      {
        "comment_id": "1584879531",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
        "discussion_id": "1581157906",
        "commented_code": "@@ -30,6 +30,8 @@ using namespace kotlin;\n //--- Setup args --------------------------------------------------------------//\n \n OBJ_GETTER(setupArgs, int argc, const char** argv) {\n+  kotlin::programName = argv[0];",
        "comment_created_at": "2024-04-30T13:57:23+00:00",
        "comment_author": "vonox7",
        "comment_body": "1. programName will now be set to null before argv leaves scope. I could not find a definite answer if it would be guaranteed to live long enough, so I opted for the safe choice.\r\n2. Theoretically it is guaranteed by the POSIX standard. However if it has 0 arguments, the code 1 line below would have crashed. I also added a testcase for argc=0, and added support for it via `std::max(0, ...)`. So now kotlin executables don't crash on startup when they are launched in a non posix compatible way.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1620522926",
    "pr_number": 5281,
    "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
    "created_at": "2024-05-30T11:26:13+00:00",
    "commented_code": "//--- Setup args --------------------------------------------------------------//\n\nOBJ_GETTER(setupArgs, int argc, const char** argv) {\n  if (argc > 0 && argv[0][0] != '\\0') {\n    kotlin::programName = argv[0];",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1620522926",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
        "discussion_id": "1620522926",
        "commented_code": "@@ -30,8 +30,12 @@ using namespace kotlin;\n //--- Setup args --------------------------------------------------------------//\n \n OBJ_GETTER(setupArgs, int argc, const char** argv) {\n+  if (argc > 0 && argv[0][0] != '\\0') {\n+    kotlin::programName = argv[0];",
        "comment_created_at": "2024-05-30T11:26:13+00:00",
        "comment_author": "projedi",
        "comment_body": "How about doing `kotlin::programName = strndup(argv[0], 4096)`? No need to `free` the result, and we don't have to worry about lifetimes. `4096` is just some random not-too-small not-too-big number to protect us from `argv[0]` being too large. Technically, the OS has some limits already, but might as well protect ourselves.",
        "pr_file_module": null
      },
      {
        "comment_id": "1629431106",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/runtime/src/launcher/cpp/launcher.cpp",
        "discussion_id": "1620522926",
        "commented_code": "@@ -30,8 +30,12 @@ using namespace kotlin;\n //--- Setup args --------------------------------------------------------------//\n \n OBJ_GETTER(setupArgs, int argc, const char** argv) {\n+  if (argc > 0 && argv[0][0] != '\\0') {\n+    kotlin::programName = argv[0];",
        "comment_created_at": "2024-06-06T12:23:11+00:00",
        "comment_author": "vonox7",
        "comment_body": "Ok, I applied your idea.",
        "pr_file_module": null
      }
    ]
  }
]
