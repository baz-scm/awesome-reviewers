---
title: Document configuration version requirements
description: Make build configuration options explicit and document their version
  dependencies. When introducing configuration parameters that are version-specific,
  clearly indicate compatibility requirements and provide command-line options to
  make constraints optional when appropriate.
repository: opencv/opencv
label: Configurations
language: Python
comments_count: 2
repository_stars: 82865
---

Make build configuration options explicit and document their version dependencies. When introducing configuration parameters that are version-specific, clearly indicate compatibility requirements and provide command-line options to make constraints optional when appropriate.

For example, instead of hardcoding checks or settings:

```python
# Not recommended: Hardcoded check with no option to disable
check_have_ipp_flag(os.path.join(builder.libdest, "CMakeVars.txt"))

# Better approach: Make the check configurable
if args.strict_dependencies:
    check_have_ipp_flag(os.path.join(builder.libdest, "CMakeVars.txt"))

# When defining version-specific configurations, document requirements
# and use proper syntax
ABI("3", "arm64-v8a", None, 21, cmake_vars=dict(
    # Supported in Android NDK r27 and higher, ignored in earlier versions
    ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES='ON'
))
```

This approach ensures that configuration options remain flexible while clearly communicating version requirements to developers, preventing unexpected behavior across different environments.


[
  {
    "discussion_id": "2050238177",
    "pr_number": 27239,
    "pr_file": "platforms/android/build_sdk.py",
    "created_at": "2025-04-18T07:24:16+00:00",
    "commented_code": "builder.build_library(abi, do_install, args.no_media_ndk)\n\n    builder.gather_results()\n\n   \n    check_have_ipp_flag(os.path.join(builder.libdest, \"CMakeVars.txt\"))",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2050238177",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27239,
        "pr_file": "platforms/android/build_sdk.py",
        "discussion_id": "2050238177",
        "commented_code": "@@ -487,7 +505,9 @@ def get_ndk_dir():\n         builder.build_library(abi, do_install, args.no_media_ndk)\n \n     builder.gather_results()\n-\n+   \n+    check_have_ipp_flag(os.path.join(builder.libdest, \"CMakeVars.txt\"))",
        "comment_created_at": "2025-04-18T07:24:16+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I propose to add command line option, e.g. \"--strict-dependencies\" to make the check optional.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1726812141",
    "pr_number": 26057,
    "pr_file": "platforms/android/default.config.py",
    "created_at": "2024-08-22T10:39:53+00:00",
    "commented_code": "ABIs = [\n    ABI(\"2\", \"armeabi-v7a\", None, 21, cmake_vars=dict(ANDROID_ABI='armeabi-v7a with NEON')),\n    ABI(\"3\", \"arm64-v8a\",   None, 21, cmake_vars=dict('ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON')),",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1726812141",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26057,
        "pr_file": "platforms/android/default.config.py",
        "discussion_id": "1726812141",
        "commented_code": "@@ -0,0 +1,6 @@\n+ABIs = [\n+    ABI(\"2\", \"armeabi-v7a\", None, 21, cmake_vars=dict(ANDROID_ABI='armeabi-v7a with NEON')),\n+    ABI(\"3\", \"arm64-v8a\",   None, 21, cmake_vars=dict('ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON')),",
        "comment_created_at": "2024-08-22T10:39:53+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "Makes sense for \"Android NDK r27 and higher\" according to documentation.\r\n\r\nWhy do not enable that by default in the main build_sdk.py script?",
        "pr_file_module": null
      },
      {
        "comment_id": "1727047145",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26057,
        "pr_file": "platforms/android/default.config.py",
        "discussion_id": "1726812141",
        "commented_code": "@@ -0,0 +1,6 @@\n+ABIs = [\n+    ABI(\"2\", \"armeabi-v7a\", None, 21, cmake_vars=dict(ANDROID_ABI='armeabi-v7a with NEON')),\n+    ABI(\"3\", \"arm64-v8a\",   None, 21, cmake_vars=dict('ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON')),",
        "comment_created_at": "2024-08-22T13:20:09+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I want to switch CI to the default configuration and always build SDK and AAR packages with 16kb pages support. The packages will work with both old and new memory configuration. It just tunes ELF sections alignment a bit.  The option will be ignored with NDK before 27.",
        "pr_file_module": null
      },
      {
        "comment_id": "1728529743",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26057,
        "pr_file": "platforms/android/default.config.py",
        "discussion_id": "1726812141",
        "commented_code": "@@ -0,0 +1,6 @@\n+ABIs = [\n+    ABI(\"2\", \"armeabi-v7a\", None, 21, cmake_vars=dict(ANDROID_ABI='armeabi-v7a with NEON')),\n+    ABI(\"3\", \"arm64-v8a\",   None, 21, cmake_vars=dict('ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON')),",
        "comment_created_at": "2024-08-23T07:45:36+00:00",
        "comment_author": "mshabunin",
        "comment_body": "```suggestion\r\n    ABI(\"3\", \"arm64-v8a\",   None, 21, cmake_vars=dict(ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES='ON')),\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
