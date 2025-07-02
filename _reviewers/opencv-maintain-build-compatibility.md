---
title: Maintain build compatibility
description: When modifying build scripts or configurations, ensure compatibility
  across all supported environments and properly test changes through CI pipelines.
  For tools with version-dependent features, add version checks and provide alternative
  implementations for older versions.
repository: opencv/opencv
label: CI/CD
language: Txt
comments_count: 2
repository_stars: 82865
---

When modifying build scripts or configurations, ensure compatibility across all supported environments and properly test changes through CI pipelines. For tools with version-dependent features, add version checks and provide alternative implementations for older versions.

Example for CMake version-specific features:
```cmake
if(CMAKE_VERSION VERSION_LESS "3.13")
  # Use older approach for CMake < 3.13
  set(PROTOBUF_GENERATE_CPP_APPEND_PATH ON)
  protobuf_generate_cpp(fw_srcs fw_hdrs ${proto_files})
else()
  # Use newer approach available in CMake 3.13+
  protobuf_generate(
    APPEND_PATH
    LANGUAGE cpp
    IMPORT_DIRS ${Protobuf_IMPORT_DIRS}
    OUT_VAR fw_srcs
    PROTOC_EXE ${Protobuf_PROTOC_EXECUTABLE}
    PROTOS ${proto_files})
  # Process the output variables as needed
  set(fw_hdrs "${fw_srcs}")
  list(FILTER fw_srcs EXCLUDE REGEX ".+\.h$")
  list(FILTER fw_hdrs INCLUDE REGEX ".+\.h$")
endif()
```

Always reference the specific CI workflow that validates your build changes (e.g., "This change is tested by the workflow at .github/workflows/OCV-PR-4.x-Android-Test.yaml") to demonstrate the build continues to work across all supported platforms and configurations.


[
  {
    "discussion_id": "1644650533",
    "pr_number": 25569,
    "pr_file": "3rdparty/zlib-ng/CMakeLists.txt",
    "created_at": "2024-06-18T15:21:31+00:00",
    "commented_code": "set_target_properties(${ZLIB_LIBRARY} PROPERTIES FOLDER \"3rdparty\")\nendif()\n\nif(NOT BUILD_SHARED_LIBS)\n  ocv_install_target(${ZLIB_LIBRARY} EXPORT OpenCVModules ARCHIVE DESTINATION ${OPENCV_3P_LIB_INSTALL_PATH} COMPONENT dev)\nendif()",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1644650533",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25569,
        "pr_file": "3rdparty/zlib-ng/CMakeLists.txt",
        "discussion_id": "1644650533",
        "commented_code": "@@ -789,8 +789,4 @@ if(ENABLE_SOLUTION_FOLDERS)\n   set_target_properties(${ZLIB_LIBRARY} PROPERTIES FOLDER \"3rdparty\")\n endif()\n \n-if(NOT BUILD_SHARED_LIBS)\n-  ocv_install_target(${ZLIB_LIBRARY} EXPORT OpenCVModules ARCHIVE DESTINATION ${OPENCV_3P_LIB_INSTALL_PATH} COMPONENT dev)\n-endif()",
        "comment_created_at": "2024-06-18T15:21:31+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "It should break static linkage, if OpenCV is build against own zlib-ng, but not system-wide.",
        "pr_file_module": null
      },
      {
        "comment_id": "1652983240",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25569,
        "pr_file": "3rdparty/zlib-ng/CMakeLists.txt",
        "discussion_id": "1644650533",
        "commented_code": "@@ -789,8 +789,4 @@ if(ENABLE_SOLUTION_FOLDERS)\n   set_target_properties(${ZLIB_LIBRARY} PROPERTIES FOLDER \"3rdparty\")\n endif()\n \n-if(NOT BUILD_SHARED_LIBS)\n-  ocv_install_target(${ZLIB_LIBRARY} EXPORT OpenCVModules ARCHIVE DESTINATION ${OPENCV_3P_LIB_INSTALL_PATH} COMPONENT dev)\n-endif()",
        "comment_created_at": "2024-06-25T14:50:47+00:00",
        "comment_author": "FantasqueX",
        "comment_body": "Sorry for late reply. This `ocv_install_target` statement isn't removed. It is moved to outer space because both static linkage and dynamic linkage need this statement in Android build. So, this will only affect dynamic linkage.",
        "pr_file_module": null
      },
      {
        "comment_id": "1661358623",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25569,
        "pr_file": "3rdparty/zlib-ng/CMakeLists.txt",
        "discussion_id": "1644650533",
        "commented_code": "@@ -789,8 +789,4 @@ if(ENABLE_SOLUTION_FOLDERS)\n   set_target_properties(${ZLIB_LIBRARY} PROPERTIES FOLDER \"3rdparty\")\n endif()\n \n-if(NOT BUILD_SHARED_LIBS)\n-  ocv_install_target(${ZLIB_LIBRARY} EXPORT OpenCVModules ARCHIVE DESTINATION ${OPENCV_3P_LIB_INSTALL_PATH} COMPONENT dev)\n-endif()",
        "comment_created_at": "2024-07-01T17:38:37+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "We should not redistribute system or sysroot libraries even for static OpenCV builds. Only own 3rdparty built binaries are redistributed.\r\n\r\nWhich builder configuration does check of your modification?",
        "pr_file_module": null
      },
      {
        "comment_id": "1661770972",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25569,
        "pr_file": "3rdparty/zlib-ng/CMakeLists.txt",
        "discussion_id": "1644650533",
        "commented_code": "@@ -789,8 +789,4 @@ if(ENABLE_SOLUTION_FOLDERS)\n   set_target_properties(${ZLIB_LIBRARY} PROPERTIES FOLDER \"3rdparty\")\n endif()\n \n-if(NOT BUILD_SHARED_LIBS)\n-  ocv_install_target(${ZLIB_LIBRARY} EXPORT OpenCVModules ARCHIVE DESTINATION ${OPENCV_3P_LIB_INSTALL_PATH} COMPONENT dev)\n-endif()",
        "comment_created_at": "2024-07-02T03:29:13+00:00",
        "comment_author": "FantasqueX",
        "comment_body": "https://github.com/opencv/ci-gha-workflow/blob/main/.github/workflows/OCV-PR-4.x-Android-Test.yaml\r\nHowever, I cannot find previous build failure log.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2137746431",
    "pr_number": 27428,
    "pr_file": "modules/dnn/CMakeLists.txt",
    "created_at": "2025-06-10T12:19:34+00:00",
    "commented_code": "if(PROTOBUF_UPDATE_FILES)\n    file(GLOB proto_files \"${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/*.proto\" \"${CMAKE_CURRENT_LIST_DIR}/src/caffe/opencv-caffe.proto\" \"${CMAKE_CURRENT_LIST_DIR}/src/onnx/opencv-onnx.proto\")\n    set(PROTOBUF_GENERATE_CPP_APPEND_PATH ON) # required for tensorflow\n    protobuf_generate_cpp(fw_srcs fw_hdrs ${proto_files})\n    protobuf_generate(\n        APPEND_PATH # required for tensorflow\n        LANGUAGE cpp\n        IMPORT_DIRS ${Protobuf_IMPORT_DIRS}\n        OUT_VAR fw_srcs\n        PROTOC_EXE ${Protobuf_PROTOC_EXECUTABLE}\n        PROTOS ${proto_files})\n    set(fw_hdrs \"${fw_srcs}\")\n    # separate the header files and source files\n    list(FILTER fw_srcs EXCLUDE REGEX \".+\\.h$\")\n    list(FILTER fw_hdrs INCLUDE REGEX \".+\\.h$\")",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2137746431",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27428,
        "pr_file": "modules/dnn/CMakeLists.txt",
        "discussion_id": "2137746431",
        "commented_code": "@@ -115,8 +115,17 @@ if(HAVE_PROTOBUF)\n \n   if(PROTOBUF_UPDATE_FILES)\n     file(GLOB proto_files \"${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/*.proto\" \"${CMAKE_CURRENT_LIST_DIR}/src/caffe/opencv-caffe.proto\" \"${CMAKE_CURRENT_LIST_DIR}/src/onnx/opencv-onnx.proto\")\n-    set(PROTOBUF_GENERATE_CPP_APPEND_PATH ON) # required for tensorflow\n-    protobuf_generate_cpp(fw_srcs fw_hdrs ${proto_files})\n+    protobuf_generate(\n+        APPEND_PATH # required for tensorflow\n+        LANGUAGE cpp\n+        IMPORT_DIRS ${Protobuf_IMPORT_DIRS}\n+        OUT_VAR fw_srcs\n+        PROTOC_EXE ${Protobuf_PROTOC_EXECUTABLE}\n+        PROTOS ${proto_files})\n+    set(fw_hdrs \"${fw_srcs}\")\n+    # separate the header files and source files\n+    list(FILTER fw_srcs EXCLUDE REGEX \".+\\.h$\")\n+    list(FILTER fw_hdrs INCLUDE REGEX \".+\\.h$\")",
        "comment_created_at": "2025-06-10T12:19:34+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "> protobuf_generate Added in version 3.13.\r\n\r\nIt breaks build with older CMake. I propose to add CMake version check and presume the old branch for old CMake.\r\n",
        "pr_file_module": null
      }
    ]
  }
]
