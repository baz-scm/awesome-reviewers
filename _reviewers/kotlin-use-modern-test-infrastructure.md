---
title: Use modern test infrastructure
description: Always add new tests to the current recommended test infrastructure rather
  than legacy systems that are being phased out. This reduces technical debt and ensures
  tests remain maintainable as the codebase evolves.
repository: JetBrains/kotlin
label: Testing
language: Other
comments_count: 2
repository_stars: 50857
---

Always add new tests to the current recommended test infrastructure rather than legacy systems that are being phased out. This reduces technical debt and ensures tests remain maintainable as the codebase evolves.

When adding a new test:
1. Check if there's an ongoing migration effort for test infrastructure
2. Target the new recommended infrastructure
3. Follow project-specific guidelines for test generation

Example:
```kotlin
// Instead of adding to legacy build.gradle:
// standaloneTest("new_feature") {
//     source = "runtime/new_feature/test.kt"
// }

// Add a proper test class to the new infrastructure:
// e.g., in native/native.tests/tests/org/jetbrains/kotlin/konan/test/blackbox/NewFeatureTest.kt
class NewFeatureTest : AbstractNativeTest() {
    @Test
    fun testNewFeature() {
        // Test implementation
    }
}
```

For some test types, you may need to run generation tasks after adding new test data files.


[
  {
    "discussion_id": "1581150497",
    "pr_number": 5281,
    "pr_file": "kotlin-native/backend.native/tests/build.gradle",
    "created_at": "2024-04-26T14:53:10+00:00",
    "commented_code": "source = \"runtime/exceptions/throw_from_except_constr.kt\"\n}\n\nstandaloneTest(\"program_name\") {\n    source = \"runtime/program_name/runtime_program_name.kt\"\n}",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1581150497",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/backend.native/tests/build.gradle",
        "discussion_id": "1581150497",
        "commented_code": "@@ -380,6 +380,10 @@ standaloneTest(\"throw_from_except_constr\") {\n     source = \"runtime/exceptions/throw_from_except_constr.kt\"\n }\n \n+standaloneTest(\"program_name\") {\n+    source = \"runtime/program_name/runtime_program_name.kt\"\n+}",
        "comment_created_at": "2024-04-26T14:53:10+00:00",
        "comment_author": "SvyatoslavScherbina",
        "comment_body": "This file represents the legacy test infrastructure that we are actively trying to get rid of.\r\n\r\nPlease create a proper test class in\r\nhttps://github.com/JetBrains/kotlin/tree/master/native/native.tests/tests/org/jetbrains/kotlin/konan/test/blackbox instead.",
        "pr_file_module": null
      },
      {
        "comment_id": "1584875172",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5281,
        "pr_file": "kotlin-native/backend.native/tests/build.gradle",
        "discussion_id": "1581150497",
        "commented_code": "@@ -380,6 +380,10 @@ standaloneTest(\"throw_from_except_constr\") {\n     source = \"runtime/exceptions/throw_from_except_constr.kt\"\n }\n \n+standaloneTest(\"program_name\") {\n+    source = \"runtime/program_name/runtime_program_name.kt\"\n+}",
        "comment_created_at": "2024-04-30T13:54:43+00:00",
        "comment_author": "vonox7",
        "comment_body": "I ported the testcase to the new infrastructure.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1533445212",
    "pr_number": 5270,
    "pr_file": "kotlin-native/backend.native/tests/build.gradle",
    "created_at": "2024-03-21T08:47:02+00:00",
    "commented_code": "UtilsKt.dependsOnPlatformLibs(it)\n    }\n\n    standaloneTest(\"interop_objc_kt65260\") {\n        source = \"interop/objc/kt65260.kt\"\n        UtilsKt.dependsOnPlatformLibs(it)\n    }",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1533445212",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5270,
        "pr_file": "kotlin-native/backend.native/tests/build.gradle",
        "discussion_id": "1533445212",
        "commented_code": "@@ -1103,6 +1103,11 @@ if (PlatformInfo.isAppleTarget(project)) {\n         UtilsKt.dependsOnPlatformLibs(it)\n     }\n \n+    standaloneTest(\"interop_objc_kt65260\") {\n+        source = \"interop/objc/kt65260.kt\"\n+        UtilsKt.dependsOnPlatformLibs(it)\n+    }",
        "comment_created_at": "2024-03-21T08:47:02+00:00",
        "comment_author": "SvyatoslavScherbina",
        "comment_body": "This file is the legacy test infrastructure. We are currently migrating all tests from here.\r\nPlease add the new test there instead: https://github.com/JetBrains/kotlin/tree/master/native/native.tests/testData/codegen/cinterop/objc\r\nAfter creating a file, you will need to run `generateTests` Gradle task (or `Generate Tests` run configuration in IDEA). This will generate JUnit tests for the new testdata file.",
        "pr_file_module": null
      }
    ]
  }
]
