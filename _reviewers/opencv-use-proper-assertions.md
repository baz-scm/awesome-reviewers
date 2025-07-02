---
title: Use proper assertions
description: 'Write tests with proper assertions to ensure reliability and maintainability.
  Follow these guidelines:


  1. **Check for empty data** before proceeding with tests to prevent invalid test
  conditions:'
repository: opencv/opencv
label: Testing
language: C++
comments_count: 7
repository_stars: 82865
---

Write tests with proper assertions to ensure reliability and maintainability. Follow these guidelines:

1. **Check for empty data** before proceeding with tests to prevent invalid test conditions:
```cpp
string path = cvtest::findDataFile("test_image.png");
Mat img = imread(path);
ASSERT_FALSE(img.empty()) << "Cannot open test image: " << path;
```

2. **Use ASSERT_* for critical conditions** that should halt test execution when failed:
```cpp
// Use ASSERT_TRUE for file operations and resource initialization
ASSERT_TRUE(fs.isOpened()) << "Failed to open file";

// Use EXPECT_* for test validations that shouldn't interrupt the test
EXPECT_EQ(dst.cols, 270);
```

3. **Maintain correct parameter order** in equality assertions with (expected, actual) to generate meaningful error messages:
```cpp
// Correct: ASSERT_EQ(expected_reference, actual_result)
ASSERT_EQ(4, img.channels());
EXPECT_EQ(6, lines[0][0]);
```

4. **Use specialized assertions** for common comparisons instead of custom loops:
```cpp
// Use instead of manual matrix comparison loops
EXPECT_MAT_NEAR(src_mat, dst_mat, 0);
// or
EXPECT_PRED_FORMAT2(cvtest::MatComparator(0, 0), src_mat, dst_mat);
```

Well-written assertions make tests more reliable, easier to debug, and help identify the exact cause of failures.


[
  {
    "discussion_id": "2024750669",
    "pr_number": 27051,
    "pr_file": "modules/photo/perf/perf_ccm.cpp",
    "created_at": "2025-04-02T12:44:24+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n\n#include \"perf_precomp.hpp\"\n#include \"opencv2/photo.hpp\"\n\nnamespace opencv_test\n{\nnamespace\n{\n\nusing namespace std;\nusing namespace cv::ccm;\n\nPERF_TEST(CV_mcc_perf, infer) {\n    // read gold chartsRGB\n    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n    FileStorage fs(path, FileStorage::READ);\n    Mat chartsRGB;\n    FileNode node = fs[\"chartsRGB\"];\n    node >> chartsRGB;\n    fs.release();",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2024750669",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27051,
        "pr_file": "modules/photo/perf/perf_ccm.cpp",
        "discussion_id": "2024750669",
        "commented_code": "@@ -0,0 +1,41 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+\n+#include \"perf_precomp.hpp\"\n+#include \"opencv2/photo.hpp\"\n+\n+namespace opencv_test\n+{\n+namespace\n+{\n+\n+using namespace std;\n+using namespace cv::ccm;\n+\n+PERF_TEST(CV_mcc_perf, infer) {\n+    // read gold chartsRGB\n+    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n+    FileStorage fs(path, FileStorage::READ);\n+    Mat chartsRGB;\n+    FileNode node = fs[\"chartsRGB\"];\n+    node >> chartsRGB;\n+    fs.release();",
        "comment_created_at": "2025-04-02T12:44:24+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "`ASSERT_FALSE(chartsRGB.empty());`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2091413835",
    "pr_number": 27051,
    "pr_file": "modules/photo/perf/perf_ccm.cpp",
    "created_at": "2025-05-15T15:07:08+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n\n#include \"perf_precomp.hpp\"\n#include \"opencv2/photo.hpp\"\n\nnamespace opencv_test {\nnamespace {\n\nusing namespace cv;\nusing namespace std;\n\nPERF_TEST(CV_ccm_perf_480_640, correctImage)\n{\n    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n    FileStorage fs(path, FileStorage::READ);\n    Mat chartsRGB;\n    fs[\"chartsRGB\"] >> chartsRGB;\n    fs.release();\n\n    cv::ccm::ColorCorrectionModel model(\n        chartsRGB.col(1).clone().reshape(3, chartsRGB.rows/3) / 255.0,\n        cv::ccm::COLORCHECKER_MACBETH\n    );\n    model.compute();\n    Mat img(480, 640, CV_8UC3);\n    randu(img, 0, 255);\n    img.convertTo(img, CV_64F, 1.0/255.0);\n\n    Mat correctedImage;\n    TEST_CYCLE() { model.correctImage(img, correctedImage); }\n    SANITY_CHECK_NOTHING();\n}\n\nPERF_TEST(CV_ccm_perf_720_1280, correctImage)\n{\n    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n    FileStorage fs(path, FileStorage::READ);\n    Mat chartsRGB;\n    fs[\"chartsRGB\"] >> chartsRGB;",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2091413835",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27051,
        "pr_file": "modules/photo/perf/perf_ccm.cpp",
        "discussion_id": "2091413835",
        "commented_code": "@@ -0,0 +1,103 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+\n+#include \"perf_precomp.hpp\"\n+#include \"opencv2/photo.hpp\"\n+\n+namespace opencv_test {\n+namespace {\n+\n+using namespace cv;\n+using namespace std;\n+\n+PERF_TEST(CV_ccm_perf_480_640, correctImage)\n+{\n+    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n+    FileStorage fs(path, FileStorage::READ);\n+    Mat chartsRGB;\n+    fs[\"chartsRGB\"] >> chartsRGB;\n+    fs.release();\n+\n+    cv::ccm::ColorCorrectionModel model(\n+        chartsRGB.col(1).clone().reshape(3, chartsRGB.rows/3) / 255.0,\n+        cv::ccm::COLORCHECKER_MACBETH\n+    );\n+    model.compute();\n+    Mat img(480, 640, CV_8UC3);\n+    randu(img, 0, 255);\n+    img.convertTo(img, CV_64F, 1.0/255.0);\n+\n+    Mat correctedImage;\n+    TEST_CYCLE() { model.correctImage(img, correctedImage); }\n+    SANITY_CHECK_NOTHING();\n+}\n+\n+PERF_TEST(CV_ccm_perf_720_1280, correctImage)\n+{\n+    string path = cvtest::findDataFile(\"cv/mcc/mcc_ccm_test.yml\");\n+    FileStorage fs(path, FileStorage::READ);\n+    Mat chartsRGB;\n+    fs[\"chartsRGB\"] >> chartsRGB;",
        "comment_created_at": "2025-05-15T15:07:08+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "`ASSERT_FALSE(chartsRGB.empty());` here and bellow.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2110097906",
    "pr_number": 27362,
    "pr_file": "modules/core/test/test_mat.cpp",
    "created_at": "2025-05-27T20:07:08+00:00",
    "commented_code": "EXPECT_EQ(25u, m2.total());\n}\n\nTEST(Core_Mat, empty)\n{\n    // Should not crash.\n    uint8_t data[2] = {0, 1};\n    cv::Mat mat_nd(/*ndims=*/0, /*sizes=*/nullptr, CV_8UC1, /*data=*/data);\n    cv::Mat1b mat(0, 0, /*data=*/data, /*steps=*/1);\n}",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2110097906",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27362,
        "pr_file": "modules/core/test/test_mat.cpp",
        "discussion_id": "2110097906",
        "commented_code": "@@ -1446,6 +1446,14 @@ TEST(Core_Mat, regression_9507)\n     EXPECT_EQ(25u, m2.total());\n }\n \n+TEST(Core_Mat, empty)\n+{\n+    // Should not crash.\n+    uint8_t data[2] = {0, 1};\n+    cv::Mat mat_nd(/*ndims=*/0, /*sizes=*/nullptr, CV_8UC1, /*data=*/data);\n+    cv::Mat1b mat(0, 0, /*data=*/data, /*steps=*/1);\n+}",
        "comment_created_at": "2025-05-27T20:07:08+00:00",
        "comment_author": "vpisarev",
        "comment_body": "suggest to add some checks to the test:\r\n\r\n```\r\nTEST(Core_Mat, empty)\r\n{\r\n    // Should not crash.\r\n    uint8_t data[2] = {0, 1};\r\n    cv::Mat mat_nd(/*ndims=*/0, /*sizes=*/nullptr, CV_8UC1, /*data=*/data);\r\n    cv::Mat1b mat(0, 0, /*data=*/data, /*steps=*/1);\r\n    EXPECT_EQ(mat_nd.dims, 0);\r\n    EXPECT_EQ(mat.dims, 2);\r\n    EXPECT_LE(mat_nd.total(), 1u); // 0 for 4.x, 1 for 5.x\r\n    EXPECT_EQ(mat.total(), 0u);\r\n    EXPECT_TRUE(mat.empty());\r\n    // mat_nd.empty() should return true for 4.x and false for 5.x\r\n}\r\n```\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2115278244",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27362,
        "pr_file": "modules/core/test/test_mat.cpp",
        "discussion_id": "2110097906",
        "commented_code": "@@ -1446,6 +1446,14 @@ TEST(Core_Mat, regression_9507)\n     EXPECT_EQ(25u, m2.total());\n }\n \n+TEST(Core_Mat, empty)\n+{\n+    // Should not crash.\n+    uint8_t data[2] = {0, 1};\n+    cv::Mat mat_nd(/*ndims=*/0, /*sizes=*/nullptr, CV_8UC1, /*data=*/data);\n+    cv::Mat1b mat(0, 0, /*data=*/data, /*steps=*/1);\n+}",
        "comment_created_at": "2025-05-30T07:09:08+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "> // 0 for 4.x, 1 for 5.x\r\n\r\nDo we really to introduce support in OpenCV 4.x for functionality which has different behavior in OpenCV 5.x.",
        "pr_file_module": null
      },
      {
        "comment_id": "2120384779",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27362,
        "pr_file": "modules/core/test/test_mat.cpp",
        "discussion_id": "2110097906",
        "commented_code": "@@ -1446,6 +1446,14 @@ TEST(Core_Mat, regression_9507)\n     EXPECT_EQ(25u, m2.total());\n }\n \n+TEST(Core_Mat, empty)\n+{\n+    // Should not crash.\n+    uint8_t data[2] = {0, 1};\n+    cv::Mat mat_nd(/*ndims=*/0, /*sizes=*/nullptr, CV_8UC1, /*data=*/data);\n+    cv::Mat1b mat(0, 0, /*data=*/data, /*steps=*/1);\n+}",
        "comment_created_at": "2025-06-02T08:14:36+00:00",
        "comment_author": "vrabaud",
        "comment_body": "I fixed the test. @vpisarev , please decide with @opencv-alalek if it worth adding the test on total and empty.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1956243656",
    "pr_number": 26907,
    "pr_file": "modules/features2d/test/test_fast.cpp",
    "created_at": "2025-02-14T14:32:43+00:00",
    "commented_code": "TEST(Features2d_FAST, regression) { CV_FastTest test; test.safe_run(); }\n\n// #define DUMP_TEST_DATA\n\nTEST(Features2d_FAST, noNMS)\n{\n    Mat img = imread(string(cvtest::TS::ptr()->get_data_path()) + \"inpaint/orig.png\", cv::IMREAD_GRAYSCALE);\n    string xml = string(cvtest::TS::ptr()->get_data_path()) + \"fast/result_no_nonmax.xml\";\n\n    vector<KeyPoint> keypoints;\n    FAST(img, keypoints, 100, false, FastFeatureDetector::DetectorType::TYPE_9_16);\n    Mat kps(1, (int)(keypoints.size() * sizeof(KeyPoint)), CV_8U, &keypoints[0]);\n\n    Mat gt_kps;\n    FileStorage fs(xml, FileStorage::READ);\n#ifdef DUMP_TEST_DATA\n    if (!fs.isOpened())\n    {\n        fs.open(xml, FileStorage::WRITE);\n        fs << \"exp_kps\" << kps;\n        fs.release();\n        fs.open(xml, FileStorage::READ);\n    }\n#endif\n    EXPECT_TRUE(fs.isOpened());",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1956243656",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26907,
        "pr_file": "modules/features2d/test/test_fast.cpp",
        "discussion_id": "1956243656",
        "commented_code": "@@ -135,4 +135,34 @@ void CV_FastTest::run( int )\n \n TEST(Features2d_FAST, regression) { CV_FastTest test; test.safe_run(); }\n \n+// #define DUMP_TEST_DATA\n+\n+TEST(Features2d_FAST, noNMS)\n+{\n+    Mat img = imread(string(cvtest::TS::ptr()->get_data_path()) + \"inpaint/orig.png\", cv::IMREAD_GRAYSCALE);\n+    string xml = string(cvtest::TS::ptr()->get_data_path()) + \"fast/result_no_nonmax.xml\";\n+\n+    vector<KeyPoint> keypoints;\n+    FAST(img, keypoints, 100, false, FastFeatureDetector::DetectorType::TYPE_9_16);\n+    Mat kps(1, (int)(keypoints.size() * sizeof(KeyPoint)), CV_8U, &keypoints[0]);\n+\n+    Mat gt_kps;\n+    FileStorage fs(xml, FileStorage::READ);\n+#ifdef DUMP_TEST_DATA\n+    if (!fs.isOpened())\n+    {\n+        fs.open(xml, FileStorage::WRITE);\n+        fs << \"exp_kps\" << kps;\n+        fs.release();\n+        fs.open(xml, FileStorage::READ);\n+    }\n+#endif\n+    EXPECT_TRUE(fs.isOpened());",
        "comment_created_at": "2025-02-14T14:32:43+00:00",
        "comment_author": "mshabunin",
        "comment_body": "Maybe `ASSERT_TRUE` would be better in this case? Here and on line 163 (`ASSERT_GT`).",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1940521696",
    "pr_number": 26872,
    "pr_file": "modules/imgcodecs/perf/perf_decode_encode.cpp",
    "created_at": "2025-02-04T05:20:31+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html\n\n#include \"perf_precomp.hpp\"\n\nnamespace opencv_test\n{\n\n#ifdef HAVE_PNG\n\nusing namespace perf;\n\ntypedef perf::TestBaseWithParam<std::string> Decode;\ntypedef perf::TestBaseWithParam<std::string> Encode;\n\nconst string exts[] = {\n#ifdef HAVE_AVIF\n    \".avif\",\n#endif\n    \".bmp\",\n#ifdef HAVE_IMGCODEC_GIF\n    \".gif\",\n#endif\n#if (defined(HAVE_JASPER) && defined(OPENCV_IMGCODECS_ENABLE_JASPER_TESTS)) \\\n    || defined(HAVE_OPENJPEG)\n    \".jp2\",\n#endif\n#ifdef HAVE_JPEG\n    \".jpg\",\n#endif\n#ifdef HAVE_JPEGXL\n    \".jxl\",\n#endif\n    \".png\",\n#ifdef HAVE_IMGCODEC_PXM\n    \".ppm\",\n#endif\n#ifdef HAVE_IMGCODEC_SUNRASTER\n    \".ras\",\n#endif\n#ifdef HAVE_TIFF\n    \".tiff\",\n#endif\n#ifdef HAVE_WEBP\n    \".webp\",\n#endif\n};\n\nconst string exts_multi[] = {\n#ifdef HAVE_AVIF\n    \".avif\",\n#endif\n#ifdef HAVE_IMGCODEC_GIF\n    \".gif\",\n#endif\n    \".png\",\n#ifdef HAVE_TIFF\n    \".tiff\",\n#endif\n#ifdef HAVE_WEBP\n    \".webp\",\n#endif\n};\n\nPERF_TEST_P(Decode, bgr, testing::ValuesIn(exts))\n{\n    String filename = getDataPath(\"perf/1920x1080.png\");\n\n    Mat src = imread(filename);\n    vector<uchar> buf;\n    EXPECT_TRUE(imencode(GetParam(), src, buf));\n\n    TEST_CYCLE() imdecode(buf, IMREAD_UNCHANGED);\n\n    SANITY_CHECK_NOTHING();\n}\n\nPERF_TEST_P(Decode, rgb, testing::ValuesIn(exts))\n{\n    String filename = getDataPath(\"perf/1920x1080.png\");\n\n    Mat src = imread(filename);",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1940521696",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26872,
        "pr_file": "modules/imgcodecs/perf/perf_decode_encode.cpp",
        "discussion_id": "1940521696",
        "commented_code": "@@ -0,0 +1,127 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html\n+\n+#include \"perf_precomp.hpp\"\n+\n+namespace opencv_test\n+{\n+\n+#ifdef HAVE_PNG\n+\n+using namespace perf;\n+\n+typedef perf::TestBaseWithParam<std::string> Decode;\n+typedef perf::TestBaseWithParam<std::string> Encode;\n+\n+const string exts[] = {\n+#ifdef HAVE_AVIF\n+    \".avif\",\n+#endif\n+    \".bmp\",\n+#ifdef HAVE_IMGCODEC_GIF\n+    \".gif\",\n+#endif\n+#if (defined(HAVE_JASPER) && defined(OPENCV_IMGCODECS_ENABLE_JASPER_TESTS)) \\\n+    || defined(HAVE_OPENJPEG)\n+    \".jp2\",\n+#endif\n+#ifdef HAVE_JPEG\n+    \".jpg\",\n+#endif\n+#ifdef HAVE_JPEGXL\n+    \".jxl\",\n+#endif\n+    \".png\",\n+#ifdef HAVE_IMGCODEC_PXM\n+    \".ppm\",\n+#endif\n+#ifdef HAVE_IMGCODEC_SUNRASTER\n+    \".ras\",\n+#endif\n+#ifdef HAVE_TIFF\n+    \".tiff\",\n+#endif\n+#ifdef HAVE_WEBP\n+    \".webp\",\n+#endif\n+};\n+\n+const string exts_multi[] = {\n+#ifdef HAVE_AVIF\n+    \".avif\",\n+#endif\n+#ifdef HAVE_IMGCODEC_GIF\n+    \".gif\",\n+#endif\n+    \".png\",\n+#ifdef HAVE_TIFF\n+    \".tiff\",\n+#endif\n+#ifdef HAVE_WEBP\n+    \".webp\",\n+#endif\n+};\n+\n+PERF_TEST_P(Decode, bgr, testing::ValuesIn(exts))\n+{\n+    String filename = getDataPath(\"perf/1920x1080.png\");\n+\n+    Mat src = imread(filename);\n+    vector<uchar> buf;\n+    EXPECT_TRUE(imencode(GetParam(), src, buf));\n+\n+    TEST_CYCLE() imdecode(buf, IMREAD_UNCHANGED);\n+\n+    SANITY_CHECK_NOTHING();\n+}\n+\n+PERF_TEST_P(Decode, rgb, testing::ValuesIn(exts))\n+{\n+    String filename = getDataPath(\"perf/1920x1080.png\");\n+\n+    Mat src = imread(filename);",
        "comment_created_at": "2025-02-04T05:20:31+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "`EXPECT_FALSE(src.empty()) << Cannot open test image perf/1920x1080.png;`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1436144317",
    "pr_number": 21407,
    "pr_file": "modules/imgproc/test/test_houghlines.cpp",
    "created_at": "2023-12-25T19:32:31+00:00",
    "commented_code": "EXPECT_NEAR(lines[0][1], 1.57179642, 1e-4);\n}\n\nTEST(WeightedHoughLines, horizontal)\n{\n    Mat img(25, 25, CV_8UC1, Scalar(0));\n    // draw lines. from top to bottom, stronger to weaker.\n    line(img, Point(0, 6), Point(25, 6), Scalar(255));\n    line(img, Point(0, 12), Point(25, 12), Scalar(254));\n    line(img, Point(0, 18), Point(25, 18), Scalar(253));\n    \n    // detect lines\n    std::vector<Vec2f> lines;\n    int threshold{253*25-1};\n    bool use_edgeval{true};\n    HoughLines(img, lines, 1, CV_PI/180, threshold, 0, 0, 0.0, CV_PI, use_edgeval);\n    \n    // check results\n    ASSERT_EQ(lines.size(), 3U);\n    // detected lines is assumed sorted from stronger to weaker. \n    EXPECT_EQ(lines[0][0], 6);\n    EXPECT_EQ(lines[1][0], 12);\n    EXPECT_EQ(lines[2][0], 18);",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1436144317",
        "repo_full_name": "opencv/opencv",
        "pr_number": 21407,
        "pr_file": "modules/imgproc/test/test_houghlines.cpp",
        "discussion_id": "1436144317",
        "commented_code": "@@ -340,6 +340,53 @@ TEST(HoughLines, regression_21983)\n     EXPECT_NEAR(lines[0][1], 1.57179642, 1e-4);\n }\n \n+TEST(WeightedHoughLines, horizontal)\n+{\n+    Mat img(25, 25, CV_8UC1, Scalar(0));\n+    // draw lines. from top to bottom, stronger to weaker.\n+    line(img, Point(0, 6), Point(25, 6), Scalar(255));\n+    line(img, Point(0, 12), Point(25, 12), Scalar(254));\n+    line(img, Point(0, 18), Point(25, 18), Scalar(253));\n+    \n+    // detect lines\n+    std::vector<Vec2f> lines;\n+    int threshold{253*25-1};\n+    bool use_edgeval{true};\n+    HoughLines(img, lines, 1, CV_PI/180, threshold, 0, 0, 0.0, CV_PI, use_edgeval);\n+    \n+    // check results\n+    ASSERT_EQ(lines.size(), 3U);\n+    // detected lines is assumed sorted from stronger to weaker. \n+    EXPECT_EQ(lines[0][0], 6);\n+    EXPECT_EQ(lines[1][0], 12);\n+    EXPECT_EQ(lines[2][0], 18);",
        "comment_created_at": "2023-12-25T19:32:31+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "Signature for `_EQ` is `ASSERT_EQ(expected_reference, actual_result);`.\r\nCorrect order of parameters are required to emit valid error messages.\r\n\r\nReference: https://github.com/opencv/opencv/blob/4.0.0/modules/ts/include/opencv2/ts/ts_gtest.h#L8196-L8200\r\n\r\n```\r\nGTEST_API_ AssertionResult EqFailure(const char* expected_expression,\r\n                                     const char* actual_expression,\r\n                                     const std::string& expected_value,\r\n                                     const std::string& actual_value,\r\n                                     bool ignoring_case);\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1881420274",
        "repo_full_name": "opencv/opencv",
        "pr_number": 21407,
        "pr_file": "modules/imgproc/test/test_houghlines.cpp",
        "discussion_id": "1436144317",
        "commented_code": "@@ -340,6 +340,53 @@ TEST(HoughLines, regression_21983)\n     EXPECT_NEAR(lines[0][1], 1.57179642, 1e-4);\n }\n \n+TEST(WeightedHoughLines, horizontal)\n+{\n+    Mat img(25, 25, CV_8UC1, Scalar(0));\n+    // draw lines. from top to bottom, stronger to weaker.\n+    line(img, Point(0, 6), Point(25, 6), Scalar(255));\n+    line(img, Point(0, 12), Point(25, 12), Scalar(254));\n+    line(img, Point(0, 18), Point(25, 18), Scalar(253));\n+    \n+    // detect lines\n+    std::vector<Vec2f> lines;\n+    int threshold{253*25-1};\n+    bool use_edgeval{true};\n+    HoughLines(img, lines, 1, CV_PI/180, threshold, 0, 0, 0.0, CV_PI, use_edgeval);\n+    \n+    // check results\n+    ASSERT_EQ(lines.size(), 3U);\n+    // detected lines is assumed sorted from stronger to weaker. \n+    EXPECT_EQ(lines[0][0], 6);\n+    EXPECT_EQ(lines[1][0], 12);\n+    EXPECT_EQ(lines[2][0], 18);",
        "comment_created_at": "2024-12-12T05:50:54+00:00",
        "comment_author": "MasahiroOgawa",
        "comment_body": "I'm sorry. I fixed it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1789212179",
    "pr_number": 26254,
    "pr_file": "modules/core/test/test_mat.cpp",
    "created_at": "2024-10-06T19:08:34+00:00",
    "commented_code": "EXPECT_EQ(s, \"InputArray: empty()=true kind=0x00010000 flags=0x01010000 total(-1)=0 dims(-1)=0 size(-1)=0x0 type(-1)=CV_8UC1\");\n}\n\nTEST(Mat, reshape_1d)\n{\n    std::vector<int> v = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};\n    Mat m = Mat(v).reshape(0, 2);\n\n    int newrows = 2;\n    EXPECT_EQ(m.dims, newrows);\n    EXPECT_EQ(m.type(), CV_32S);\n    EXPECT_EQ(m.ptr<int>(), &v[0]);\n    EXPECT_EQ(m.rows, newrows);\n    EXPECT_EQ(m.total(), v.size());\n\n    int sz[] = {(int)v.size()};\n    Mat m1 = m.reshape(0, 1, sz);\n    EXPECT_EQ(m1.dims, 1);\n    EXPECT_EQ(m1.type(), CV_32S);",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1789212179",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26254,
        "pr_file": "modules/core/test/test_mat.cpp",
        "discussion_id": "1789212179",
        "commented_code": "@@ -2647,4 +2647,77 @@ TEST(InputArray, dumpEmpty)\n     EXPECT_EQ(s, \"InputArray: empty()=true kind=0x00010000 flags=0x01010000 total(-1)=0 dims(-1)=0 size(-1)=0x0 type(-1)=CV_8UC1\");\n }\n \n+TEST(Mat, reshape_1d)\n+{\n+    std::vector<int> v = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};\n+    Mat m = Mat(v).reshape(0, 2);\n+\n+    int newrows = 2;\n+    EXPECT_EQ(m.dims, newrows);\n+    EXPECT_EQ(m.type(), CV_32S);\n+    EXPECT_EQ(m.ptr<int>(), &v[0]);\n+    EXPECT_EQ(m.rows, newrows);\n+    EXPECT_EQ(m.total(), v.size());\n+\n+    int sz[] = {(int)v.size()};\n+    Mat m1 = m.reshape(0, 1, sz);\n+    EXPECT_EQ(m1.dims, 1);\n+    EXPECT_EQ(m1.type(), CV_32S);",
        "comment_created_at": "2024-10-06T19:08:34+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "Signature for `_EQ` is `ASSERT_EQ(expected_reference, actual_result);`.\r\nCorrect order of parameters are required to emit valid error messages.\r\n\r\nReference: https://github.com/opencv/opencv/blob/4.0.0/modules/ts/include/opencv2/ts/ts_gtest.h#L8196-L8200\r\n\r\n```\r\nGTEST_API_ AssertionResult EqFailure(const char* expected_expression,\r\n                                     const char* actual_expression,\r\n                                     const std::string& expected_value,\r\n                                     const std::string& actual_value,\r\n                                     bool ignoring_case);\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
