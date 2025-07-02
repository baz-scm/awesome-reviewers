---
title: Guard optional dependencies
description: Configuration management requires careful handling of optional dependencies
  in both build scripts and source code. Always guard code that depends on optional
  modules or libraries with appropriate feature guards, and check for component existence
  before using them.
repository: opencv/opencv
label: Configurations
language: Other
comments_count: 5
repository_stars: 82865
---

Configuration management requires careful handling of optional dependencies in both build scripts and source code. Always guard code that depends on optional modules or libraries with appropriate feature guards, and check for component existence before using them.

In build scripts:
```cmake
# Check for optional components before using them
FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)
if(WEBP_MUX_LIBRARY)
  SET(WEBP_LIBRARIES ${WEBP_LIBRARIES} ${WEBP_MUX_LIBRARY})
endif()
```

In header files:
```cpp
// Guard features that depend on optional modules
#ifdef HAVE_OPENCV_DNN
// DNN-dependent code here
#endif
```

For configuration variables, use standardized naming conventions:
- `HAVE_` prefix for feature availability (e.g., `HAVE_ZLIB` instead of `ZLIB_FOUND`)
- `OPENCV_` prefix for OpenCV-specific settings to avoid conflicts (e.g., `OPENCV_ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES`)

When detecting incompatible dependencies, provide clear messages and fallback options:
```cmake
if(HAVE_CXX17 AND OPENEXR_VERSION VERSION_LESS "2.3.0")
  message(STATUS "OpenEXR(ver ${OPENEXR_VERSION}) doesn't support C++17. Updating OpenEXR 2.3.0+ is required.")
  # Provide fallback or clear error
endif()
```


[
  {
    "discussion_id": "2097147988",
    "pr_number": 25569,
    "pr_file": "cmake/OpenCVGenConfig.cmake",
    "created_at": "2025-05-20T07:06:39+00:00",
    "commented_code": "set(OpenCV_USE_MANGLED_PATHS_CONFIGCMAKE FALSE)\nendif()\n\nif(ZLIB_FOUND)",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2097147988",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25569,
        "pr_file": "cmake/OpenCVGenConfig.cmake",
        "discussion_id": "2097147988",
        "commented_code": "@@ -11,6 +11,10 @@ else()\n   set(OpenCV_USE_MANGLED_PATHS_CONFIGCMAKE FALSE)\n endif()\n \n+if(ZLIB_FOUND)",
        "comment_created_at": "2025-05-20T07:06:39+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "> ZLIB_FOUND\r\n\r\nWrong.\r\n\r\nWe should not mess with CMakes `find_package(Zlib)` from anywhere (e.g. libiff may find own ZLIB).\r\n`HAVE_ZLIB` must be used for OpenCV usage checks.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2051463839",
    "pr_number": 26906,
    "pr_file": "modules/objdetect/src/mcc/checker_detector.hpp",
    "created_at": "2025-04-19T12:09:47+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n\n/*\n * MIT License\n *\n * Copyright (c) 2018 Pedro Diamel Marrero Fern\u00e1ndez\n *\n * Permission is hereby granted, free of charge, to any person obtaining a copy\n * of this software and associated documentation files (the \"Software\"), to deal\n * in the Software without restriction, including without limitation the rights\n * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n * copies of the Software, and to permit persons to whom the Software is\n * furnished to do so, subject to the following conditions:\n *\n * The above copyright notice and this permission notice shall be included in all\n * copies or substantial portions of the Software.\n *\n * THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n * SOFTWARE.\n */\n\n#ifndef _MCC_CHECKER_DETECTOR_HPP\n#define _MCC_CHECKER_DETECTOR_HPP\n\n#include \"opencv2/objdetect.hpp\"\n#include \"charts.hpp\"\n\nnamespace cv\n{\nnamespace mcc\n{\n\nclass CCheckerDetectorImpl : public CCheckerDetector\n{\n\n    typedef std::vector<Point> PointsVector;\n    typedef std::vector<PointsVector> ContoursVector;\n\npublic:\n    CCheckerDetectorImpl();\n    CCheckerDetectorImpl(const dnn::Net& _net){",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2051463839",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26906,
        "pr_file": "modules/objdetect/src/mcc/checker_detector.hpp",
        "discussion_id": "2051463839",
        "commented_code": "@@ -0,0 +1,207 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+\n+/*\n+ * MIT License\n+ *\n+ * Copyright (c) 2018 Pedro Diamel Marrero Fern\u00e1ndez\n+ *\n+ * Permission is hereby granted, free of charge, to any person obtaining a copy\n+ * of this software and associated documentation files (the \"Software\"), to deal\n+ * in the Software without restriction, including without limitation the rights\n+ * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n+ * copies of the Software, and to permit persons to whom the Software is\n+ * furnished to do so, subject to the following conditions:\n+ *\n+ * The above copyright notice and this permission notice shall be included in all\n+ * copies or substantial portions of the Software.\n+ *\n+ * THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n+ * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n+ * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n+ * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n+ * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n+ * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n+ * SOFTWARE.\n+ */\n+\n+#ifndef _MCC_CHECKER_DETECTOR_HPP\n+#define _MCC_CHECKER_DETECTOR_HPP\n+\n+#include \"opencv2/objdetect.hpp\"\n+#include \"charts.hpp\"\n+\n+namespace cv\n+{\n+namespace mcc\n+{\n+\n+class CCheckerDetectorImpl : public CCheckerDetector\n+{\n+\n+    typedef std::vector<Point> PointsVector;\n+    typedef std::vector<PointsVector> ContoursVector;\n+\n+public:\n+    CCheckerDetectorImpl();\n+    CCheckerDetectorImpl(const dnn::Net& _net){",
        "comment_created_at": "2025-04-19T12:09:47+00:00",
        "comment_author": "mshabunin",
        "comment_body": "This PR breaks build without _opencv_dnn_ - all related code should be guarded by `#ifdef HAVE_OPENCV_DNN` or _objdetect_->_dnn_ dependency should be required.\r\n\r\n**cc** @asmorkalov ",
        "pr_file_module": null
      },
      {
        "comment_id": "2051823993",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26906,
        "pr_file": "modules/objdetect/src/mcc/checker_detector.hpp",
        "discussion_id": "2051463839",
        "commented_code": "@@ -0,0 +1,207 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+\n+/*\n+ * MIT License\n+ *\n+ * Copyright (c) 2018 Pedro Diamel Marrero Fern\u00e1ndez\n+ *\n+ * Permission is hereby granted, free of charge, to any person obtaining a copy\n+ * of this software and associated documentation files (the \"Software\"), to deal\n+ * in the Software without restriction, including without limitation the rights\n+ * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n+ * copies of the Software, and to permit persons to whom the Software is\n+ * furnished to do so, subject to the following conditions:\n+ *\n+ * The above copyright notice and this permission notice shall be included in all\n+ * copies or substantial portions of the Software.\n+ *\n+ * THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n+ * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n+ * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n+ * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n+ * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n+ * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n+ * SOFTWARE.\n+ */\n+\n+#ifndef _MCC_CHECKER_DETECTOR_HPP\n+#define _MCC_CHECKER_DETECTOR_HPP\n+\n+#include \"opencv2/objdetect.hpp\"\n+#include \"charts.hpp\"\n+\n+namespace cv\n+{\n+namespace mcc\n+{\n+\n+class CCheckerDetectorImpl : public CCheckerDetector\n+{\n+\n+    typedef std::vector<Point> PointsVector;\n+    typedef std::vector<PointsVector> ContoursVector;\n+\n+public:\n+    CCheckerDetectorImpl();\n+    CCheckerDetectorImpl(const dnn::Net& _net){",
        "comment_created_at": "2025-04-20T22:32:21+00:00",
        "comment_author": "gursimarsingh",
        "comment_body": "Adding a fix in this PR https://github.com/opencv/opencv/pull/27246 ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1899933291",
    "pr_number": 26057,
    "pr_file": "cmake/OpenCVCompilerOptions.cmake",
    "created_at": "2024-12-31T06:06:22+00:00",
    "commented_code": "endif()\nendif()\n\n# For 16k pages support with NDK prior 27\n# Details: https://developer.android.com/guide/practices/page-sizes?hl=en\nif(ANDROID AND ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES AND (ANDROID_ABI STREQUAL arm64-v8a OR ANDROID_ABI STREQUAL x86_64))",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1899933291",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26057,
        "pr_file": "cmake/OpenCVCompilerOptions.cmake",
        "discussion_id": "1899933291",
        "commented_code": "@@ -404,6 +404,14 @@ if(NOT OPENCV_SKIP_LINK_NO_UNDEFINED)\n   endif()\n endif()\n \n+# For 16k pages support with NDK prior 27\n+# Details: https://developer.android.com/guide/practices/page-sizes?hl=en\n+if(ANDROID AND ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES AND (ANDROID_ABI STREQUAL arm64-v8a OR ANDROID_ABI STREQUAL x86_64))",
        "comment_created_at": "2024-12-31T06:06:22+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "> ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES\r\n\r\n`OPENCV_ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES` to avoid possible conflicts",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1627890810",
    "pr_number": 25608,
    "pr_file": "cmake/OpenCVFindWebP.cmake",
    "created_at": "2024-06-05T14:23:41+00:00",
    "commented_code": "# Look for the library.\n    FIND_LIBRARY(WEBP_LIBRARY NAMES webp)\n    MARK_AS_ADVANCED(WEBP_LIBRARY)\n    FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)\n    FIND_LIBRARY(WEBP_DEMUX_LIBRARY NAMES webpdemux)\n\n    # handle the QUIETLY and REQUIRED arguments and set WEBP_FOUND to TRUE if\n    # all listed variables are TRUE\n    INCLUDE(${CMAKE_ROOT}/Modules/FindPackageHandleStandardArgs.cmake)\n    FIND_PACKAGE_HANDLE_STANDARD_ARGS(WebP DEFAULT_MSG WEBP_LIBRARY WEBP_INCLUDE_DIR)\n\n    SET(WEBP_LIBRARIES ${WEBP_LIBRARY})\n    \n    SET(WEBP_LIBRARIES ${WEBP_LIBRARY} webpmux webpdemux)",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1627890810",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25608,
        "pr_file": "cmake/OpenCVFindWebP.cmake",
        "discussion_id": "1627890810",
        "commented_code": "@@ -21,13 +21,15 @@ else()\n \n     # Look for the library.\n     FIND_LIBRARY(WEBP_LIBRARY NAMES webp)\n-    MARK_AS_ADVANCED(WEBP_LIBRARY)\n+    FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)\n+    FIND_LIBRARY(WEBP_DEMUX_LIBRARY NAMES webpdemux)\n \n     # handle the QUIETLY and REQUIRED arguments and set WEBP_FOUND to TRUE if\n     # all listed variables are TRUE\n     INCLUDE(${CMAKE_ROOT}/Modules/FindPackageHandleStandardArgs.cmake)\n     FIND_PACKAGE_HANDLE_STANDARD_ARGS(WebP DEFAULT_MSG WEBP_LIBRARY WEBP_INCLUDE_DIR)\n-\n-    SET(WEBP_LIBRARIES ${WEBP_LIBRARY})\n+    \n+    SET(WEBP_LIBRARIES ${WEBP_LIBRARY} webpmux webpdemux)",
        "comment_created_at": "2024-06-05T14:23:41+00:00",
        "comment_author": "vrabaud",
        "comment_body": "You should only add webpmux and webpdemux if they are found. When building WebP from third_party, it is all bundled in one library.\r\nSo:\r\n```cmake\r\nif(WEBP_MUX_LIBRARY)\r\n  SET(WEBP_LIBRARIES ${WEBP_LIBRARY} ${WEBP_MUX_LIBRARY})\r\nendif()\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1629475029",
    "pr_number": 25608,
    "pr_file": "cmake/OpenCVFindWebP.cmake",
    "created_at": "2024-06-06T12:46:37+00:00",
    "commented_code": "# Look for the library.\n    FIND_LIBRARY(WEBP_LIBRARY NAMES webp)\n    MARK_AS_ADVANCED(WEBP_LIBRARY)\n    FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)\n    FIND_LIBRARY(WEBP_DEMUX_LIBRARY NAMES webpdemux)\n\n    # handle the QUIETLY and REQUIRED arguments and set WEBP_FOUND to TRUE if\n    # all listed variables are TRUE\n    INCLUDE(${CMAKE_ROOT}/Modules/FindPackageHandleStandardArgs.cmake)\n    FIND_PACKAGE_HANDLE_STANDARD_ARGS(WebP DEFAULT_MSG WEBP_LIBRARY WEBP_INCLUDE_DIR)\n\n    SET(WEBP_LIBRARIES ${WEBP_LIBRARY})\n    if(WEBP_MUX_LIBRARY)",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1629475029",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25608,
        "pr_file": "cmake/OpenCVFindWebP.cmake",
        "discussion_id": "1629475029",
        "commented_code": "@@ -21,13 +21,17 @@ else()\n \n     # Look for the library.\n     FIND_LIBRARY(WEBP_LIBRARY NAMES webp)\n-    MARK_AS_ADVANCED(WEBP_LIBRARY)\n+    FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)\n+    FIND_LIBRARY(WEBP_DEMUX_LIBRARY NAMES webpdemux)\n \n     # handle the QUIETLY and REQUIRED arguments and set WEBP_FOUND to TRUE if\n     # all listed variables are TRUE\n     INCLUDE(${CMAKE_ROOT}/Modules/FindPackageHandleStandardArgs.cmake)\n     FIND_PACKAGE_HANDLE_STANDARD_ARGS(WebP DEFAULT_MSG WEBP_LIBRARY WEBP_INCLUDE_DIR)\n \n-    SET(WEBP_LIBRARIES ${WEBP_LIBRARY})\n+    if(WEBP_MUX_LIBRARY)",
        "comment_created_at": "2024-06-06T12:46:37+00:00",
        "comment_author": "vrabaud",
        "comment_body": "SET(WEBP_LIBRARIES ${WEBP_LIBRARY})\r\n if(WEBP_MUX_LIBRARY)\r\n        SET(WEBP_LIBRARIES ${WEBP_LIBRARIES} ${WEBP_MUX_LIBRARY} ${WEBP_DEMUX_LIBRARY})\r\n    endif()",
        "pr_file_module": null
      }
    ]
  }
]
