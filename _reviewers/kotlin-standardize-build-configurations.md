---
title: Standardize build configurations
description: 'Maintain consistent and standardized build configurations across the
  project to improve maintainability and reduce errors:


  1. **Centralize dependency management** - Use shared dependency declarations rather
  than hardcoding versions in individual module build files. This ensures consistency
  across the project and makes version updates simpler.'
repository: JetBrains/kotlin
label: Configurations
language: Other
comments_count: 3
repository_stars: 50857
---

Maintain consistent and standardized build configurations across the project to improve maintainability and reduce errors:

1. **Centralize dependency management** - Use shared dependency declarations rather than hardcoding versions in individual module build files. This ensures consistency across the project and makes version updates simpler.

   ```gradle
   // Instead of:
   testImplementation("com.google.code.gson:gson:2.8.9")
   
   // Prefer using centralized dependency management:
   testImplementation(commonDependency("com.google.code.gson:gson"))
   ```

2. **Avoid duplicating configurations** - Don't repeat configuration code that's already defined in parent or root projects. Reference or inherit from common configurations instead.

3. **Prefer Kotlin DSL** - For new modules, use `.gradle.kts` (Kotlin) scripts rather than `.gradle` (Groovy) scripts to benefit from type safety, better IDE support, and consistency with the broader codebase.

By following these practices, you'll reduce configuration drift, make updates more manageable, and maintain a more consistent build environment.


[
  {
    "discussion_id": "1094239825",
    "pr_number": 5088,
    "pr_file": "libraries/stdlib/jvm/build.gradle",
    "created_at": "2023-02-02T09:22:04+00:00",
    "commented_code": "testApi project(':kotlin-test:kotlin-test-junit')\n\n    builtins project(':core:builtins')\n\n    testImplementation(\"com.google.code.gson:gson:2.8.9\")",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1094239825",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5088,
        "pr_file": "libraries/stdlib/jvm/build.gradle",
        "discussion_id": "1094239825",
        "commented_code": "@@ -79,6 +79,8 @@ dependencies {\n     testApi project(':kotlin-test:kotlin-test-junit')\n \n     builtins project(':core:builtins')\n+\n+    testImplementation(\"com.google.code.gson:gson:2.8.9\")",
        "comment_created_at": "2023-02-02T09:22:04+00:00",
        "comment_author": "Badya",
        "comment_body": "In order to have the same version of dependency across all the modules, it is better to declare it this way:\r\n```\r\ntestImplementation(commonDependency(\"com.google.code.gson:gson\"))\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1094461867",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5088,
        "pr_file": "libraries/stdlib/jvm/build.gradle",
        "discussion_id": "1094239825",
        "commented_code": "@@ -79,6 +79,8 @@ dependencies {\n     testApi project(':kotlin-test:kotlin-test-junit')\n \n     builtins project(':core:builtins')\n+\n+    testImplementation(\"com.google.code.gson:gson:2.8.9\")",
        "comment_created_at": "2023-02-02T12:33:13+00:00",
        "comment_author": "nikita-nazarov",
        "comment_body": "Thanks for the comment! Unfortunately `libraries/stdlib/jvm/build.gradle` is a groovy script and you can't use the `commonDependency(...)` function there (as it is defined in `DependenciesKt#commonDependency` and probably can't be directly imported). What would be the best way to approach this issue?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "441420936",
    "pr_number": 3415,
    "pr_file": "libraries/tools/atomicfu/build.gradle",
    "created_at": "2020-06-17T09:44:55+00:00",
    "commented_code": "repositories {\n    mavenCentral()\n}\n\napply plugin: 'kotlin'\napply plugin: 'jps-compatible'\n\nconfigurePublishing(project)\n\npill {\n    variant = 'FULL'\n}\n\ncompileJava {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "441420936",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3415,
        "pr_file": "libraries/tools/atomicfu/build.gradle",
        "discussion_id": "441420936",
        "commented_code": "@@ -0,0 +1,45 @@\n+repositories {\n+    mavenCentral()\n+}\n+\n+apply plugin: 'kotlin'\n+apply plugin: 'jps-compatible'\n+\n+configurePublishing(project)\n+\n+pill {\n+    variant = 'FULL'\n+}\n+\n+compileJava {",
        "comment_created_at": "2020-06-17T09:44:55+00:00",
        "comment_author": "4u7",
        "comment_body": "Looks like this code duplicates configuration done for all project in the root project\r\nhttps://github.com/JetBrains/kotlin/blob/master/build.gradle.kts#L948",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "441421656",
    "pr_number": 3415,
    "pr_file": "libraries/tools/atomicfu/build.gradle",
    "created_at": "2020-06-17T09:45:58+00:00",
    "commented_code": "repositories {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "441421656",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3415,
        "pr_file": "libraries/tools/atomicfu/build.gradle",
        "discussion_id": "441421656",
        "commented_code": "@@ -0,0 +1,45 @@\n+repositories {",
        "comment_created_at": "2020-06-17T09:45:58+00:00",
        "comment_author": "4u7",
        "comment_body": "Please prefer adding new modules with `.gradle.kts` scripts, it's not an issue tho",
        "pr_file_module": null
      }
    ]
  }
]
