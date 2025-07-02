---
title: Use optimized functions
description: When implementing algorithms, prefer using OpenCV's built-in optimized
  functions over writing custom implementations. OpenCV's library functions are typically
  vectorized, extensively tested, and optimized for performance across different platforms
  and hardware architectures.
repository: opencv/opencv
label: Algorithms
language: C++
comments_count: 7
repository_stars: 82865
---

When implementing algorithms, prefer using OpenCV's built-in optimized functions over writing custom implementations. OpenCV's library functions are typically vectorized, extensively tested, and optimized for performance across different platforms and hardware architectures.

Key examples:
1. Use `inRange()` instead of custom saturation checks (Discussion 7)
2. Use `cv::sum()` for channel operations instead of manually splitting and summing (Discussion 9)
3. Consider converting frequently used operations to vectorized functions that can leverage SIMD instructions (Discussion 10, 17)
4. Use mathematical functions with scalar parameters when available, such as `divide(src, 2, dst)` instead of creating intermediate matrices (Discussion 20)
5. Use OpenCV's metrics functions like `cv::PSNR()` instead of custom implementations (Discussion 42)
6. Prefer `cv::RNG` over standard library random generators for deterministic behavior and testability (Discussion 47)

Example - Instead of this:
```cpp
Mat saturate(Mat& src, const double& low, const double& up)
{
    Mat dst = Mat::ones(src.size(), CV_8UC1);
    MatIterator_<Vec3d> it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();
    MatIterator_<uchar> it_dst = dst.begin<uchar>();
    for (; it_src != end_src; ++it_src, ++it_dst)
    {
        for (int i = 0; i < 3; ++i)
        {
            if ((*it_src)[i] > up || (*it_src)[i] < low)
            {
                *it_dst = 0;
                break;
            }
        }
    }
    return dst;
}
```

Use this:
```cpp
Mat saturate(Mat& src, const double& low, const double& up)
{
    Mat dst;
    inRange(src, Scalar(low, low, low), Scalar(up, up, up), dst);
    return dst;
}
```


[
  {
    "discussion_id": "2024769056",
    "pr_number": 27051,
    "pr_file": "modules/photo/src/ccm/utils.cpp",
    "created_at": "2025-04-02T12:53:13+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n//\n// Author: Longbu Wang <wanglongbu@huawei.com.com>\n//         Jinheng Zhang <zhangjinheng1@huawei.com>\n//         Chenqi Shan <shanchenqi@huawei.com>\n\n#include \"utils.hpp\"\n\nnamespace cv {\nnamespace ccm {\n\ninline double gammaCorrection_(const double& element, const double& gamma)\n{\n    return (element >= 0 ? pow(element, gamma) : -pow((-element), gamma));\n}\n\nMat gammaCorrection(const Mat& src, const double& gamma, Mat dst)\n{\n    return elementWise(src, [gamma](double element) -> double { return gammaCorrection_(element, gamma); }, dst);\n}\n\nMat maskCopyTo(const Mat& src, const Mat& mask)\n{\n    Mat dst(countNonZero(mask), 1, src.type());\n    const int channel = src.channels();\n    auto it_mask = mask.begin<uchar>();\n    switch (channel)\n    {\n    case 1:\n    {\n        auto it_src = src.begin<double>(), end_src = src.end<double>();\n        auto it_dst = dst.begin<double>();\n        for (; it_src != end_src; ++it_src, ++it_mask)\n        {\n            if (*it_mask)\n            {\n                (*it_dst) = (*it_src);\n                ++it_dst;\n            }\n        }\n        break;\n    }\n    case 3:\n    {\n        auto it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();\n        auto it_dst = dst.begin<Vec3d>();\n        for (; it_src != end_src; ++it_src, ++it_mask)\n        {\n            if (*it_mask)\n            {\n                (*it_dst) = (*it_src);\n                ++it_dst;\n            }\n        }\n        break;\n    }\n    default:\n        CV_Error(Error::StsBadArg, \"Wrong channel!\" );\n        break;\n    }\n    return dst;\n}\n\nMat multiple(const Mat& xyz, const Mat& ccm)\n{\n    Mat tmp = xyz.reshape(1, xyz.rows * xyz.cols);\n    Mat res = tmp * ccm;\n    res = res.reshape(res.cols, xyz.rows);\n    return res;\n}\n\nMat saturate(Mat& src, const double& low, const double& up)\n{\n    Mat dst = Mat::ones(src.size(), CV_8UC1);\n    MatIterator_<Vec3d> it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();\n    MatIterator_<uchar> it_dst = dst.begin<uchar>();\n    for (; it_src != end_src; ++it_src, ++it_dst)\n    {\n        for (int i = 0; i < 3; ++i)\n        {\n            if ((*it_src)[i] > up || (*it_src)[i] < low)\n            {\n                *it_dst = 0;\n                break;\n            }\n        }\n    }\n    return dst;\n}",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2024769056",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27051,
        "pr_file": "modules/photo/src/ccm/utils.cpp",
        "discussion_id": "2024769056",
        "commented_code": "@@ -0,0 +1,100 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+//\n+// Author: Longbu Wang <wanglongbu@huawei.com.com>\n+//         Jinheng Zhang <zhangjinheng1@huawei.com>\n+//         Chenqi Shan <shanchenqi@huawei.com>\n+\n+#include \"utils.hpp\"\n+\n+namespace cv {\n+namespace ccm {\n+\n+inline double gammaCorrection_(const double& element, const double& gamma)\n+{\n+    return (element >= 0 ? pow(element, gamma) : -pow((-element), gamma));\n+}\n+\n+Mat gammaCorrection(const Mat& src, const double& gamma, Mat dst)\n+{\n+    return elementWise(src, [gamma](double element) -> double { return gammaCorrection_(element, gamma); }, dst);\n+}\n+\n+Mat maskCopyTo(const Mat& src, const Mat& mask)\n+{\n+    Mat dst(countNonZero(mask), 1, src.type());\n+    const int channel = src.channels();\n+    auto it_mask = mask.begin<uchar>();\n+    switch (channel)\n+    {\n+    case 1:\n+    {\n+        auto it_src = src.begin<double>(), end_src = src.end<double>();\n+        auto it_dst = dst.begin<double>();\n+        for (; it_src != end_src; ++it_src, ++it_mask)\n+        {\n+            if (*it_mask)\n+            {\n+                (*it_dst) = (*it_src);\n+                ++it_dst;\n+            }\n+        }\n+        break;\n+    }\n+    case 3:\n+    {\n+        auto it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();\n+        auto it_dst = dst.begin<Vec3d>();\n+        for (; it_src != end_src; ++it_src, ++it_mask)\n+        {\n+            if (*it_mask)\n+            {\n+                (*it_dst) = (*it_src);\n+                ++it_dst;\n+            }\n+        }\n+        break;\n+    }\n+    default:\n+        CV_Error(Error::StsBadArg, \"Wrong channel!\" );\n+        break;\n+    }\n+    return dst;\n+}\n+\n+Mat multiple(const Mat& xyz, const Mat& ccm)\n+{\n+    Mat tmp = xyz.reshape(1, xyz.rows * xyz.cols);\n+    Mat res = tmp * ccm;\n+    res = res.reshape(res.cols, xyz.rows);\n+    return res;\n+}\n+\n+Mat saturate(Mat& src, const double& low, const double& up)\n+{\n+    Mat dst = Mat::ones(src.size(), CV_8UC1);\n+    MatIterator_<Vec3d> it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();\n+    MatIterator_<uchar> it_dst = dst.begin<uchar>();\n+    for (; it_src != end_src; ++it_src, ++it_dst)\n+    {\n+        for (int i = 0; i < 3; ++i)\n+        {\n+            if ((*it_src)[i] > up || (*it_src)[i] < low)\n+            {\n+                *it_dst = 0;\n+                break;\n+            }\n+        }\n+    }\n+    return dst;\n+}",
        "comment_created_at": "2025-04-02T12:53:13+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "inRange should be enough instead of it: https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga48af0ab51e36436c5d04340e036ce981",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2064230851",
    "pr_number": 27051,
    "pr_file": "modules/photo/src/ccm/ccm.cpp",
    "created_at": "2025-04-28T18:10:17+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n//\n// Author: Longbu Wang <wanglongbu@huawei.com.com>\n//         Jinheng Zhang <zhangjinheng1@huawei.com>\n//         Chenqi Shan <shanchenqi@huawei.com>\n\n#include \"opencv2/photo.hpp\"\n#include \"linearize.hpp\"\nnamespace cv {\nnamespace ccm {\nclass ColorCorrectionModel::Impl\n{\npublic:\n    Mat src;\n\n    std::shared_ptr<Color> dst = std::make_shared<Color>();\n    Mat dist;\n    RGBBase_& cs;\n    // Track initialization parameters for serialization\n    ColorSpace csEnum;\n    Mat mask;\n\n    // RGBl of detected data and the reference\n    Mat srcRgbl;\n    Mat dstRgbl;\n\n    // ccm type and shape\n    CcmType ccmType;\n    int shape;\n\n    // linear method and distance\n    std::shared_ptr<Linear> linear = std::make_shared<Linear>();\n    DistanceType distance;\n    LinearizationType linearizationType;\n\n    Mat weights;\n    Mat weightsList;\n    Mat ccm;\n    Mat ccm0;\n    double gamma;\n    int deg;\n    std::vector<double> saturatedThreshold;\n    InitialMethodType initialMethodType;\n    double weightsCoeff;\n    int maskedLen;\n    double loss;\n    int maxCount;\n    double epsilon;\n    Impl();\n\n    /** @brief Make no change for CCM_LINEAR.\n             convert cv::Mat A to [A, 1] in CCM_AFFINE.\n        @param inp the input array, type of cv::Mat.\n        @return the output array, type of cv::Mat\n    */\n    Mat prepare(const Mat& inp);\n\n    /** @brief Calculate weights and mask.\n        @param weightsList the input array, type of cv::Mat.\n        @param weightsCoeff type of double.\n        @param saturateMask the input array, type of cv::Mat.\n    */\n    void calWeightsMasks(const Mat& weightsList, double weightsCoeff, Mat saturateMask);\n\n    /** @brief Fitting nonlinear - optimization initial value by white balance.\n        @return the output array, type of Mat\n    */\n    void initialWhiteBalance(void);\n\n    /** @brief Fitting nonlinear-optimization initial value by least square.\n        @param fit if fit is True, return optimalization for rgbl distance function.\n    */\n    void initialLeastSquare(bool fit = false);\n\n    double calcLoss_(Color color);\n    double calcLoss(const Mat ccm_);\n\n    /** @brief Fitting ccm if distance function is associated with CIE Lab color space.\n             see details in https://github.com/opencv/opencv/blob/master/modules/core/include/opencv2/core/optim.hpp\n            Set terminal criteria for solver is possible.\n    */\n    void fitting(void);\n\n    void getColor(Mat& img_, bool islinear = false);\n    void getColor(ColorCheckerType constColor);\n    void getColor(Mat colors_, ColorSpace cs_, Mat colored_);\n    void getColor(Mat colors_, ColorSpace refColorSpace_);\n\n    /** @brief Loss function base on cv::MinProblemSolver::Function.\n             see details in https://github.com/opencv/opencv/blob/master/modules/core/include/opencv2/core/optim.hpp\n    */\n    class LossFunction : public MinProblemSolver::Function\n    {\n    public:\n        ColorCorrectionModel::Impl* ccmLoss;\n        LossFunction(ColorCorrectionModel::Impl* ccm)\n            : ccmLoss(ccm) {};\n\n        /** @brief Reset dims to ccm->shape.\n        */\n        int getDims() const CV_OVERRIDE\n        {\n            return ccmLoss->shape;\n        }\n\n        /** @brief Reset calculation.\n        */\n        double calc(const double* x) const CV_OVERRIDE\n        {\n            Mat ccm_(ccmLoss->shape, 1, CV_64F);\n            for (int i = 0; i < ccmLoss->shape; i++)\n            {\n                ccm_.at<double>(i, 0) = x[i];\n            }\n            ccm_ = ccm_.reshape(0, ccmLoss->shape / 3);\n            return ccmLoss->calcLoss(ccm_);\n        }\n    };\n};\n\nColorCorrectionModel::Impl::Impl()\n    : cs(*GetCS::getInstance().getRgb(COLOR_SPACE_SRGB))\n    , csEnum(COLOR_SPACE_SRGB)\n    , ccmType(CCM_LINEAR)\n    , distance(DISTANCE_CIE2000)\n    , linearizationType(LINEARIZATION_GAMMA)\n    , weights(Mat())\n    , gamma(2.2)\n    , deg(3)\n    , saturatedThreshold({ 0, 0.98 })\n    , initialMethodType(INITIAL_METHOD_LEAST_SQUARE)\n    , weightsCoeff(0)\n    , maxCount(5000)\n    , epsilon(1.e-4)\n{}\n\nMat ColorCorrectionModel::Impl::prepare(const Mat& inp)\n{\n    switch (ccmType)\n    {\n    case cv::ccm::CCM_LINEAR:\n        shape = 9;\n        return inp;\n    case cv::ccm::CCM_AFFINE:\n    {\n        shape = 12;\n        Mat arr1 = Mat::ones(inp.size(), CV_64F);\n        Mat arr_out(inp.size(), CV_64FC4);\n        Mat arr_channels[3];\n        split(inp, arr_channels);\n        merge(std::vector<Mat> { arr_channels[0], arr_channels[1], arr_channels[2], arr1 }, arr_out);\n        return arr_out;\n    }\n    default:\n        CV_Error(Error::StsBadArg, \"Wrong ccmType!\");\n        break;\n    }\n}\n\nvoid ColorCorrectionModel::Impl::calWeightsMasks(const Mat& weightsList_, double weightsCoeff_, Mat saturateMask)\n{\n    // weights\n    if (!weightsList_.empty())\n    {\n        weights = weightsList_;\n    }\n    else if (weightsCoeff_ != 0)\n    {\n        pow(dst->toLuminant(cs.io), weightsCoeff_, weights);\n    }\n\n    // masks\n    Mat weight_mask = Mat::ones(src.rows, 1, CV_8U);\n    if (!weights.empty())\n    {\n        weight_mask = weights > 0;\n    }\n    this->mask = (weight_mask) & (saturateMask);\n\n    // weights' mask\n    if (!weights.empty())\n    {\n        Mat weights_masked = maskCopyTo(this->weights, this->mask);\n        weights = weights_masked / mean(weights_masked)[0];\n    }\n    maskedLen = (int)sum(mask)[0];\n}\n\nvoid ColorCorrectionModel::Impl::initialWhiteBalance(void)\n{\n    Mat schannels[4];\n    split(srcRgbl, schannels);\n    Mat dchannels[4];\n    split(dstRgbl, dchannels);\n    std::vector<double> initialVec = { sum(dchannels[0])[0] / sum(schannels[0])[0], 0, 0, 0,\n        sum(dchannels[1])[0] / sum(schannels[1])[0], 0, 0, 0,\n        sum(dchannels[2])[0] / sum(schannels[2])[0], 0, 0, 0 };",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2064230851",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27051,
        "pr_file": "modules/photo/src/ccm/ccm.cpp",
        "discussion_id": "2064230851",
        "commented_code": "@@ -0,0 +1,504 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+//\n+// Author: Longbu Wang <wanglongbu@huawei.com.com>\n+//         Jinheng Zhang <zhangjinheng1@huawei.com>\n+//         Chenqi Shan <shanchenqi@huawei.com>\n+\n+#include \"opencv2/photo.hpp\"\n+#include \"linearize.hpp\"\n+namespace cv {\n+namespace ccm {\n+class ColorCorrectionModel::Impl\n+{\n+public:\n+    Mat src;\n+\n+    std::shared_ptr<Color> dst = std::make_shared<Color>();\n+    Mat dist;\n+    RGBBase_& cs;\n+    // Track initialization parameters for serialization\n+    ColorSpace csEnum;\n+    Mat mask;\n+\n+    // RGBl of detected data and the reference\n+    Mat srcRgbl;\n+    Mat dstRgbl;\n+\n+    // ccm type and shape\n+    CcmType ccmType;\n+    int shape;\n+\n+    // linear method and distance\n+    std::shared_ptr<Linear> linear = std::make_shared<Linear>();\n+    DistanceType distance;\n+    LinearizationType linearizationType;\n+\n+    Mat weights;\n+    Mat weightsList;\n+    Mat ccm;\n+    Mat ccm0;\n+    double gamma;\n+    int deg;\n+    std::vector<double> saturatedThreshold;\n+    InitialMethodType initialMethodType;\n+    double weightsCoeff;\n+    int maskedLen;\n+    double loss;\n+    int maxCount;\n+    double epsilon;\n+    Impl();\n+\n+    /** @brief Make no change for CCM_LINEAR.\n+             convert cv::Mat A to [A, 1] in CCM_AFFINE.\n+        @param inp the input array, type of cv::Mat.\n+        @return the output array, type of cv::Mat\n+    */\n+    Mat prepare(const Mat& inp);\n+\n+    /** @brief Calculate weights and mask.\n+        @param weightsList the input array, type of cv::Mat.\n+        @param weightsCoeff type of double.\n+        @param saturateMask the input array, type of cv::Mat.\n+    */\n+    void calWeightsMasks(const Mat& weightsList, double weightsCoeff, Mat saturateMask);\n+\n+    /** @brief Fitting nonlinear - optimization initial value by white balance.\n+        @return the output array, type of Mat\n+    */\n+    void initialWhiteBalance(void);\n+\n+    /** @brief Fitting nonlinear-optimization initial value by least square.\n+        @param fit if fit is True, return optimalization for rgbl distance function.\n+    */\n+    void initialLeastSquare(bool fit = false);\n+\n+    double calcLoss_(Color color);\n+    double calcLoss(const Mat ccm_);\n+\n+    /** @brief Fitting ccm if distance function is associated with CIE Lab color space.\n+             see details in https://github.com/opencv/opencv/blob/master/modules/core/include/opencv2/core/optim.hpp\n+            Set terminal criteria for solver is possible.\n+    */\n+    void fitting(void);\n+\n+    void getColor(Mat& img_, bool islinear = false);\n+    void getColor(ColorCheckerType constColor);\n+    void getColor(Mat colors_, ColorSpace cs_, Mat colored_);\n+    void getColor(Mat colors_, ColorSpace refColorSpace_);\n+\n+    /** @brief Loss function base on cv::MinProblemSolver::Function.\n+             see details in https://github.com/opencv/opencv/blob/master/modules/core/include/opencv2/core/optim.hpp\n+    */\n+    class LossFunction : public MinProblemSolver::Function\n+    {\n+    public:\n+        ColorCorrectionModel::Impl* ccmLoss;\n+        LossFunction(ColorCorrectionModel::Impl* ccm)\n+            : ccmLoss(ccm) {};\n+\n+        /** @brief Reset dims to ccm->shape.\n+        */\n+        int getDims() const CV_OVERRIDE\n+        {\n+            return ccmLoss->shape;\n+        }\n+\n+        /** @brief Reset calculation.\n+        */\n+        double calc(const double* x) const CV_OVERRIDE\n+        {\n+            Mat ccm_(ccmLoss->shape, 1, CV_64F);\n+            for (int i = 0; i < ccmLoss->shape; i++)\n+            {\n+                ccm_.at<double>(i, 0) = x[i];\n+            }\n+            ccm_ = ccm_.reshape(0, ccmLoss->shape / 3);\n+            return ccmLoss->calcLoss(ccm_);\n+        }\n+    };\n+};\n+\n+ColorCorrectionModel::Impl::Impl()\n+    : cs(*GetCS::getInstance().getRgb(COLOR_SPACE_SRGB))\n+    , csEnum(COLOR_SPACE_SRGB)\n+    , ccmType(CCM_LINEAR)\n+    , distance(DISTANCE_CIE2000)\n+    , linearizationType(LINEARIZATION_GAMMA)\n+    , weights(Mat())\n+    , gamma(2.2)\n+    , deg(3)\n+    , saturatedThreshold({ 0, 0.98 })\n+    , initialMethodType(INITIAL_METHOD_LEAST_SQUARE)\n+    , weightsCoeff(0)\n+    , maxCount(5000)\n+    , epsilon(1.e-4)\n+{}\n+\n+Mat ColorCorrectionModel::Impl::prepare(const Mat& inp)\n+{\n+    switch (ccmType)\n+    {\n+    case cv::ccm::CCM_LINEAR:\n+        shape = 9;\n+        return inp;\n+    case cv::ccm::CCM_AFFINE:\n+    {\n+        shape = 12;\n+        Mat arr1 = Mat::ones(inp.size(), CV_64F);\n+        Mat arr_out(inp.size(), CV_64FC4);\n+        Mat arr_channels[3];\n+        split(inp, arr_channels);\n+        merge(std::vector<Mat> { arr_channels[0], arr_channels[1], arr_channels[2], arr1 }, arr_out);\n+        return arr_out;\n+    }\n+    default:\n+        CV_Error(Error::StsBadArg, \"Wrong ccmType!\");\n+        break;\n+    }\n+}\n+\n+void ColorCorrectionModel::Impl::calWeightsMasks(const Mat& weightsList_, double weightsCoeff_, Mat saturateMask)\n+{\n+    // weights\n+    if (!weightsList_.empty())\n+    {\n+        weights = weightsList_;\n+    }\n+    else if (weightsCoeff_ != 0)\n+    {\n+        pow(dst->toLuminant(cs.io), weightsCoeff_, weights);\n+    }\n+\n+    // masks\n+    Mat weight_mask = Mat::ones(src.rows, 1, CV_8U);\n+    if (!weights.empty())\n+    {\n+        weight_mask = weights > 0;\n+    }\n+    this->mask = (weight_mask) & (saturateMask);\n+\n+    // weights' mask\n+    if (!weights.empty())\n+    {\n+        Mat weights_masked = maskCopyTo(this->weights, this->mask);\n+        weights = weights_masked / mean(weights_masked)[0];\n+    }\n+    maskedLen = (int)sum(mask)[0];\n+}\n+\n+void ColorCorrectionModel::Impl::initialWhiteBalance(void)\n+{\n+    Mat schannels[4];\n+    split(srcRgbl, schannels);\n+    Mat dchannels[4];\n+    split(dstRgbl, dchannels);\n+    std::vector<double> initialVec = { sum(dchannels[0])[0] / sum(schannels[0])[0], 0, 0, 0,\n+        sum(dchannels[1])[0] / sum(schannels[1])[0], 0, 0, 0,\n+        sum(dchannels[2])[0] / sum(schannels[2])[0], 0, 0, 0 };",
        "comment_created_at": "2025-04-28T18:10:17+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "No need to spit cv::Mat by channels for it. cv::sum supports channels: https://docs.opencv.org/5.x/d2/de8/group__core__array.html#ga716e10a2dd9e228e4d3c95818f106722",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2064246723",
    "pr_number": 27051,
    "pr_file": "modules/photo/src/ccm/utils.cpp",
    "created_at": "2025-04-28T18:19:59+00:00",
    "commented_code": "// This file is part of OpenCV project.\n// It is subject to the license terms in the LICENSE file found in the top-level directory\n// of this distribution and at http://opencv.org/license.html.\n//\n// Author: Longbu Wang <wanglongbu@huawei.com.com>\n//         Jinheng Zhang <zhangjinheng1@huawei.com>\n//         Chenqi Shan <shanchenqi@huawei.com>\n\n#include \"utils.hpp\"\n\nnamespace cv {\nnamespace ccm {\n\ninline double gammaCorrection_(double element, double gamma)\n{\n    return (element >= 0 ? pow(element, gamma) : -pow((-element), gamma));\n}\n\nMat gammaCorrection(const Mat& src, double gamma, Mat dst)\n{\n    return elementWise(src, [gamma](double element) -> double { return gammaCorrection_(element, gamma); }, dst);\n}",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2064246723",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27051,
        "pr_file": "modules/photo/src/ccm/utils.cpp",
        "discussion_id": "2064246723",
        "commented_code": "@@ -0,0 +1,86 @@\n+// This file is part of OpenCV project.\n+// It is subject to the license terms in the LICENSE file found in the top-level directory\n+// of this distribution and at http://opencv.org/license.html.\n+//\n+// Author: Longbu Wang <wanglongbu@huawei.com.com>\n+//         Jinheng Zhang <zhangjinheng1@huawei.com>\n+//         Chenqi Shan <shanchenqi@huawei.com>\n+\n+#include \"utils.hpp\"\n+\n+namespace cv {\n+namespace ccm {\n+\n+inline double gammaCorrection_(double element, double gamma)\n+{\n+    return (element >= 0 ? pow(element, gamma) : -pow((-element), gamma));\n+}\n+\n+Mat gammaCorrection(const Mat& src, double gamma, Mat dst)\n+{\n+    return elementWise(src, [gamma](double element) -> double { return gammaCorrection_(element, gamma); }, dst);\n+}",
        "comment_created_at": "2025-04-28T18:19:59+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I propose to convert Gamma correction to public function with InputArray and OutputArray. It's useful independently from the pipeline and also may be significantly optimized with universal intrinsics.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2055506089",
    "pr_number": 27238,
    "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
    "created_at": "2025-04-23T08:16:24+00:00",
    "commented_code": "}\n}\n\n\nstatic void rotationKernel(\n    float* data, const float* rotation_table,\n    size_t seq_len, size_t d\n)\n{\n    CV_Assert(d % 2 == 0);\n    const size_t d_half = d / 2;\n\n    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n\n    auto fn = [&](const cv::Range& range)\n    {\n        for (int t = range.start; t < range.end; ++t)\n        {\n            float* out_ptr    = data + size_t(t) * d;\n            const float* table_ptr = rotation_table + size_t(t) * d;\n            size_t i = 0;\n\n#if (CV_SIMD || CV_SIMD_SCALABLE)\n            const size_t w = VTraits<v_float32>::vlanes();\n            for (; i + w <= d_half; i += w)\n            {\n                v_float32 sin_v, cos_v, x_even, x_odd;\n                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n\n                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n\n                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n            }\n#endif\n            // scalar tail\n            for (; i < d_half; ++i)\n            {\n                float s  = table_ptr[2*i  ];\n                float c  = table_ptr[2*i+1];\n                float xe = out_ptr[2*i];\n                float xo = out_ptr[2*i+1];\n                out_ptr[2*i]   = xe * c - xo * s;\n                out_ptr[2*i+1] = xo * c + xe * s;\n            }\n        }\n    };\n\n    // This will spin up threads and run fn over [0, seq_len)\n    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n}\n\nstatic void precompRotationTable(float *data,\n                                  size_t seq_len,\n                                  size_t d) {\n    // RoPE precomputation\n    // RoPE is a positional encoding method used in transformer models.\n    // It uses sine and cosine functions to encode the position of tokens in a sequence\n    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n\n    // assume data is of shape [seq_ken,d]\n    const float  logBase = std::log(10000.0f);\n    const float  inv_d   = 1.0f / float(d);\n    const size_t d_half = d / 2;\n    for (size_t pos = 0; pos < seq_len; ++pos) {\n\n        size_t i = 0;\n        float* data_ptr = data + pos * d;\n\n#if (CV_SIMD || CV_SIMD_SCALABLE)\n        const size_t w = VTraits<v_float32>::vlanes();\n        const v_float32 v_logBase = v_setall_f32(logBase);\n        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n\n        for (; i + w <= d_half; i+=w) {\n            int idx_buf[CV_SIMD_WIDTH];",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2055506089",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27238,
        "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
        "discussion_id": "2055506089",
        "commented_code": "@@ -24,6 +24,105 @@ static void packWeight(size_t num_heads, size_t head_size, size_t input_hidden_s\n     }\n }\n \n+\n+static void rotationKernel(\n+    float* data, const float* rotation_table,\n+    size_t seq_len, size_t d\n+)\n+{\n+    CV_Assert(d % 2 == 0);\n+    const size_t d_half = d / 2;\n+\n+    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n+\n+    auto fn = [&](const cv::Range& range)\n+    {\n+        for (int t = range.start; t < range.end; ++t)\n+        {\n+            float* out_ptr    = data + size_t(t) * d;\n+            const float* table_ptr = rotation_table + size_t(t) * d;\n+            size_t i = 0;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+            const size_t w = VTraits<v_float32>::vlanes();\n+            for (; i + w <= d_half; i += w)\n+            {\n+                v_float32 sin_v, cos_v, x_even, x_odd;\n+                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n+                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n+\n+                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n+                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n+\n+                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n+            }\n+#endif\n+            // scalar tail\n+            for (; i < d_half; ++i)\n+            {\n+                float s  = table_ptr[2*i  ];\n+                float c  = table_ptr[2*i+1];\n+                float xe = out_ptr[2*i];\n+                float xo = out_ptr[2*i+1];\n+                out_ptr[2*i]   = xe * c - xo * s;\n+                out_ptr[2*i+1] = xo * c + xe * s;\n+            }\n+        }\n+    };\n+\n+    // This will spin up threads and run fn over [0, seq_len)\n+    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n+}\n+\n+static void precompRotationTable(float *data,\n+                                  size_t seq_len,\n+                                  size_t d) {\n+    // RoPE precomputation\n+    // RoPE is a positional encoding method used in transformer models.\n+    // It uses sine and cosine functions to encode the position of tokens in a sequence\n+    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n+\n+    // assume data is of shape [seq_ken,d]\n+    const float  logBase = std::log(10000.0f);\n+    const float  inv_d   = 1.0f / float(d);\n+    const size_t d_half = d / 2;\n+    for (size_t pos = 0; pos < seq_len; ++pos) {\n+\n+        size_t i = 0;\n+        float* data_ptr = data + pos * d;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+        const size_t w = VTraits<v_float32>::vlanes();\n+        const v_float32 v_logBase = v_setall_f32(logBase);\n+        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n+        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n+\n+        for (; i + w <= d_half; i+=w) {\n+            int idx_buf[CV_SIMD_WIDTH];",
        "comment_created_at": "2025-04-23T08:16:24+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "CV_SIMD_WIDTH is compile time constant. It may not work correctly with _SCALABLE branch. please use `VTraits<xxx>::max_nlanes` instead. For fixed-size SIMD it works in the same way.",
        "pr_file_module": null
      },
      {
        "comment_id": "2055511356",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27238,
        "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
        "discussion_id": "2055506089",
        "commented_code": "@@ -24,6 +24,105 @@ static void packWeight(size_t num_heads, size_t head_size, size_t input_hidden_s\n     }\n }\n \n+\n+static void rotationKernel(\n+    float* data, const float* rotation_table,\n+    size_t seq_len, size_t d\n+)\n+{\n+    CV_Assert(d % 2 == 0);\n+    const size_t d_half = d / 2;\n+\n+    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n+\n+    auto fn = [&](const cv::Range& range)\n+    {\n+        for (int t = range.start; t < range.end; ++t)\n+        {\n+            float* out_ptr    = data + size_t(t) * d;\n+            const float* table_ptr = rotation_table + size_t(t) * d;\n+            size_t i = 0;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+            const size_t w = VTraits<v_float32>::vlanes();\n+            for (; i + w <= d_half; i += w)\n+            {\n+                v_float32 sin_v, cos_v, x_even, x_odd;\n+                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n+                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n+\n+                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n+                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n+\n+                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n+            }\n+#endif\n+            // scalar tail\n+            for (; i < d_half; ++i)\n+            {\n+                float s  = table_ptr[2*i  ];\n+                float c  = table_ptr[2*i+1];\n+                float xe = out_ptr[2*i];\n+                float xo = out_ptr[2*i+1];\n+                out_ptr[2*i]   = xe * c - xo * s;\n+                out_ptr[2*i+1] = xo * c + xe * s;\n+            }\n+        }\n+    };\n+\n+    // This will spin up threads and run fn over [0, seq_len)\n+    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n+}\n+\n+static void precompRotationTable(float *data,\n+                                  size_t seq_len,\n+                                  size_t d) {\n+    // RoPE precomputation\n+    // RoPE is a positional encoding method used in transformer models.\n+    // It uses sine and cosine functions to encode the position of tokens in a sequence\n+    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n+\n+    // assume data is of shape [seq_ken,d]\n+    const float  logBase = std::log(10000.0f);\n+    const float  inv_d   = 1.0f / float(d);\n+    const size_t d_half = d / 2;\n+    for (size_t pos = 0; pos < seq_len; ++pos) {\n+\n+        size_t i = 0;\n+        float* data_ptr = data + pos * d;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+        const size_t w = VTraits<v_float32>::vlanes();\n+        const v_float32 v_logBase = v_setall_f32(logBase);\n+        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n+        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n+\n+        for (; i + w <= d_half; i+=w) {\n+            int idx_buf[CV_SIMD_WIDTH];",
        "comment_created_at": "2025-04-23T08:19:39+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "@fengyuentau please correct me, if I'm wrong.",
        "pr_file_module": null
      },
      {
        "comment_id": "2055637649",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27238,
        "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
        "discussion_id": "2055506089",
        "commented_code": "@@ -24,6 +24,105 @@ static void packWeight(size_t num_heads, size_t head_size, size_t input_hidden_s\n     }\n }\n \n+\n+static void rotationKernel(\n+    float* data, const float* rotation_table,\n+    size_t seq_len, size_t d\n+)\n+{\n+    CV_Assert(d % 2 == 0);\n+    const size_t d_half = d / 2;\n+\n+    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n+\n+    auto fn = [&](const cv::Range& range)\n+    {\n+        for (int t = range.start; t < range.end; ++t)\n+        {\n+            float* out_ptr    = data + size_t(t) * d;\n+            const float* table_ptr = rotation_table + size_t(t) * d;\n+            size_t i = 0;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+            const size_t w = VTraits<v_float32>::vlanes();\n+            for (; i + w <= d_half; i += w)\n+            {\n+                v_float32 sin_v, cos_v, x_even, x_odd;\n+                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n+                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n+\n+                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n+                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n+\n+                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n+            }\n+#endif\n+            // scalar tail\n+            for (; i < d_half; ++i)\n+            {\n+                float s  = table_ptr[2*i  ];\n+                float c  = table_ptr[2*i+1];\n+                float xe = out_ptr[2*i];\n+                float xo = out_ptr[2*i+1];\n+                out_ptr[2*i]   = xe * c - xo * s;\n+                out_ptr[2*i+1] = xo * c + xe * s;\n+            }\n+        }\n+    };\n+\n+    // This will spin up threads and run fn over [0, seq_len)\n+    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n+}\n+\n+static void precompRotationTable(float *data,\n+                                  size_t seq_len,\n+                                  size_t d) {\n+    // RoPE precomputation\n+    // RoPE is a positional encoding method used in transformer models.\n+    // It uses sine and cosine functions to encode the position of tokens in a sequence\n+    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n+\n+    // assume data is of shape [seq_ken,d]\n+    const float  logBase = std::log(10000.0f);\n+    const float  inv_d   = 1.0f / float(d);\n+    const size_t d_half = d / 2;\n+    for (size_t pos = 0; pos < seq_len; ++pos) {\n+\n+        size_t i = 0;\n+        float* data_ptr = data + pos * d;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+        const size_t w = VTraits<v_float32>::vlanes();\n+        const v_float32 v_logBase = v_setall_f32(logBase);\n+        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n+        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n+\n+        for (; i + w <= d_half; i+=w) {\n+            int idx_buf[CV_SIMD_WIDTH];",
        "comment_created_at": "2025-04-23T09:25:04+00:00",
        "comment_author": "nklskyoy",
        "comment_body": "@asmorkalov,\r\n\r\n```\r\nconst size_t w = VTraits<v_float32>::vlanes();\r\n...\r\nint idx_buf[w];\r\n```\r\n\r\ncaused  **[-Wvla-cxx-extension]** in GCC and the build for Win64 failed. \r\nI wasn't sure what's the proper way to deal with this..",
        "pr_file_module": null
      },
      {
        "comment_id": "2059815455",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27238,
        "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
        "discussion_id": "2055506089",
        "commented_code": "@@ -24,6 +24,105 @@ static void packWeight(size_t num_heads, size_t head_size, size_t input_hidden_s\n     }\n }\n \n+\n+static void rotationKernel(\n+    float* data, const float* rotation_table,\n+    size_t seq_len, size_t d\n+)\n+{\n+    CV_Assert(d % 2 == 0);\n+    const size_t d_half = d / 2;\n+\n+    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n+\n+    auto fn = [&](const cv::Range& range)\n+    {\n+        for (int t = range.start; t < range.end; ++t)\n+        {\n+            float* out_ptr    = data + size_t(t) * d;\n+            const float* table_ptr = rotation_table + size_t(t) * d;\n+            size_t i = 0;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+            const size_t w = VTraits<v_float32>::vlanes();\n+            for (; i + w <= d_half; i += w)\n+            {\n+                v_float32 sin_v, cos_v, x_even, x_odd;\n+                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n+                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n+\n+                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n+                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n+\n+                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n+            }\n+#endif\n+            // scalar tail\n+            for (; i < d_half; ++i)\n+            {\n+                float s  = table_ptr[2*i  ];\n+                float c  = table_ptr[2*i+1];\n+                float xe = out_ptr[2*i];\n+                float xo = out_ptr[2*i+1];\n+                out_ptr[2*i]   = xe * c - xo * s;\n+                out_ptr[2*i+1] = xo * c + xe * s;\n+            }\n+        }\n+    };\n+\n+    // This will spin up threads and run fn over [0, seq_len)\n+    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n+}\n+\n+static void precompRotationTable(float *data,\n+                                  size_t seq_len,\n+                                  size_t d) {\n+    // RoPE precomputation\n+    // RoPE is a positional encoding method used in transformer models.\n+    // It uses sine and cosine functions to encode the position of tokens in a sequence\n+    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n+\n+    // assume data is of shape [seq_ken,d]\n+    const float  logBase = std::log(10000.0f);\n+    const float  inv_d   = 1.0f / float(d);\n+    const size_t d_half = d / 2;\n+    for (size_t pos = 0; pos < seq_len; ++pos) {\n+\n+        size_t i = 0;\n+        float* data_ptr = data + pos * d;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+        const size_t w = VTraits<v_float32>::vlanes();\n+        const v_float32 v_logBase = v_setall_f32(logBase);\n+        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n+        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n+\n+        for (; i + w <= d_half; i+=w) {\n+            int idx_buf[CV_SIMD_WIDTH];",
        "comment_created_at": "2025-04-25T08:38:09+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "Yes, it does not work, because `w` value is not known in compile time. `VTraits<xxx>::max_nlanes` is compile time constant. It's equal to `CV_SIMD_WIDTH` for fixed SIMD size architectures (x86). RISC-V RVV vector size is not known in compile time, but we know maximum vector length and use it for intermediate buffers to fit any feasible vector size.",
        "pr_file_module": null
      },
      {
        "comment_id": "2062730807",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27238,
        "pr_file": "modules/dnn/src/layers/attention_layer.cpp",
        "discussion_id": "2055506089",
        "commented_code": "@@ -24,6 +24,105 @@ static void packWeight(size_t num_heads, size_t head_size, size_t input_hidden_s\n     }\n }\n \n+\n+static void rotationKernel(\n+    float* data, const float* rotation_table,\n+    size_t seq_len, size_t d\n+)\n+{\n+    CV_Assert(d % 2 == 0);\n+    const size_t d_half = d / 2;\n+\n+    double nstripes = double(seq_len) * d_half * (1.0/1024.0);\n+\n+    auto fn = [&](const cv::Range& range)\n+    {\n+        for (int t = range.start; t < range.end; ++t)\n+        {\n+            float* out_ptr    = data + size_t(t) * d;\n+            const float* table_ptr = rotation_table + size_t(t) * d;\n+            size_t i = 0;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+            const size_t w = VTraits<v_float32>::vlanes();\n+            for (; i + w <= d_half; i += w)\n+            {\n+                v_float32 sin_v, cos_v, x_even, x_odd;\n+                v_load_deinterleave(table_ptr + 2*i, sin_v, cos_v);\n+                v_load_deinterleave(out_ptr    + 2*i, x_even, x_odd);\n+\n+                v_float32 out_even = v_sub(v_mul(cos_v, x_even), v_mul(sin_v, x_odd));\n+                v_float32 out_odd  = v_add(v_mul(sin_v, x_even), v_mul(cos_v, x_odd));\n+\n+                v_store_interleave(out_ptr + 2*i, out_even, out_odd);\n+            }\n+#endif\n+            // scalar tail\n+            for (; i < d_half; ++i)\n+            {\n+                float s  = table_ptr[2*i  ];\n+                float c  = table_ptr[2*i+1];\n+                float xe = out_ptr[2*i];\n+                float xo = out_ptr[2*i+1];\n+                out_ptr[2*i]   = xe * c - xo * s;\n+                out_ptr[2*i+1] = xo * c + xe * s;\n+            }\n+        }\n+    };\n+\n+    // This will spin up threads and run fn over [0, seq_len)\n+    parallel_for_(cv::Range(0, int(seq_len)), fn, nstripes);\n+}\n+\n+static void precompRotationTable(float *data,\n+                                  size_t seq_len,\n+                                  size_t d) {\n+    // RoPE precomputation\n+    // RoPE is a positional encoding method used in transformer models.\n+    // It uses sine and cosine functions to encode the position of tokens in a sequence\n+    // initially introduced for NLP in https://arxiv.org/pdf/2104.09864\n+\n+    // assume data is of shape [seq_ken,d]\n+    const float  logBase = std::log(10000.0f);\n+    const float  inv_d   = 1.0f / float(d);\n+    const size_t d_half = d / 2;\n+    for (size_t pos = 0; pos < seq_len; ++pos) {\n+\n+        size_t i = 0;\n+        float* data_ptr = data + pos * d;\n+\n+#if (CV_SIMD || CV_SIMD_SCALABLE)\n+        const size_t w = VTraits<v_float32>::vlanes();\n+        const v_float32 v_logBase = v_setall_f32(logBase);\n+        const v_float32 v_inv_d   = v_setall_f32(inv_d);\n+        const v_float32 v_neg2    = v_setall_f32(-2.0f);\n+\n+        for (; i + w <= d_half; i+=w) {\n+            int idx_buf[CV_SIMD_WIDTH];",
        "comment_created_at": "2025-04-27T21:55:13+00:00",
        "comment_author": "nklskyoy",
        "comment_body": "I have replaced  CV_SIMD_WIDTH with VTraits<v_float32>::max_nlanes for both CV_SIMD and CV_SIMD_SCALABLE branch",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1562079542",
    "pr_number": 25394,
    "pr_file": "modules/core/src/convert.dispatch.cpp",
    "created_at": "2024-04-12T06:31:13+00:00",
    "commented_code": "int dtype = CV_MAKETYPE(ddepth, cn);\n\n    Mat src = *this;\n    dst.create(dims, size, dtype);\n    Mat dstMat = dst.getMat();\n    Mat dstMat;\n    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1562079542",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25394,
        "pr_file": "modules/core/src/convert.dispatch.cpp",
        "discussion_id": "1562079542",
        "commented_code": "@@ -278,8 +278,16 @@ void Mat::convertTo(OutputArray dst, int type_, double alpha, double beta) const\n     int dtype = CV_MAKETYPE(ddepth, cn);\n \n     Mat src = *this;\n-    dst.create(dims, size, dtype);\n-    Mat dstMat = dst.getMat();\n+    Mat dstMat;\n+    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
        "comment_created_at": "2024-04-12T06:31:13+00:00",
        "comment_author": "dkurt",
        "comment_body": "There is no check for size/dims match. For example, ROI will have the same data ptr:\r\n```cpp\r\nMat m (10, 10, CV_8U);\r\nMat roi = m.rowRange(0, 2);\r\nm.convertTo(roi, CV_8S);\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1563996085",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25394,
        "pr_file": "modules/core/src/convert.dispatch.cpp",
        "discussion_id": "1562079542",
        "commented_code": "@@ -278,8 +278,16 @@ void Mat::convertTo(OutputArray dst, int type_, double alpha, double beta) const\n     int dtype = CV_MAKETYPE(ddepth, cn);\n \n     Mat src = *this;\n-    dst.create(dims, size, dtype);\n-    Mat dstMat = dst.getMat();\n+    Mat dstMat;\n+    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
        "comment_created_at": "2024-04-13T12:33:15+00:00",
        "comment_author": "Gao-HaoYuan",
        "comment_body": "I had through **!dst.getMat().isSubmatrix()** to determine this case.",
        "pr_file_module": null
      },
      {
        "comment_id": "1564539155",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25394,
        "pr_file": "modules/core/src/convert.dispatch.cpp",
        "discussion_id": "1562079542",
        "commented_code": "@@ -278,8 +278,16 @@ void Mat::convertTo(OutputArray dst, int type_, double alpha, double beta) const\n     int dtype = CV_MAKETYPE(ddepth, cn);\n \n     Mat src = *this;\n-    dst.create(dims, size, dtype);\n-    Mat dstMat = dst.getMat();\n+    Mat dstMat;\n+    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
        "comment_created_at": "2024-04-14T07:46:22+00:00",
        "comment_author": "dkurt",
        "comment_body": "What about the following case? `.data` matched but not the shapes.\r\n```cpp\r\nMat m (10, 10, CV_8U);\r\nMat m2(5, 10, CV_8U, m.ptr<uint8_t>());\r\nm.convertTo(m2, CV_8S);\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1564719925",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25394,
        "pr_file": "modules/core/src/convert.dispatch.cpp",
        "discussion_id": "1562079542",
        "commented_code": "@@ -278,8 +278,16 @@ void Mat::convertTo(OutputArray dst, int type_, double alpha, double beta) const\n     int dtype = CV_MAKETYPE(ddepth, cn);\n \n     Mat src = *this;\n-    dst.create(dims, size, dtype);\n-    Mat dstMat = dst.getMat();\n+    Mat dstMat;\n+    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
        "comment_created_at": "2024-04-14T13:15:04+00:00",
        "comment_author": "Gao-HaoYuan",
        "comment_body": "Firstly, if **roi** is a submatrix, the refcount will add 1. \r\n`if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype) && refcount == 2) `\r\n This condition can recognize the first case.\r\n`Mat m (10, 10, CV_8U);\r\nMat roi = m.rowRange(0, 2);\r\nm.convertTo(roi, CV_8S);`\r\n\r\nBUt, I have come up with a new question. Like, \r\n\r\n`Mat m (10, 10, CV_8U);\r\nMat m2(10, 10, CV_8U, m.ptr<uint8_t>());\r\nm.convertTo(m2, CV_8S);`\r\n\r\nIn this case,  the member 'u' is NULL. By checking whether 'u' is null, we can solve this problem.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1564721975",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25394,
        "pr_file": "modules/core/src/convert.dispatch.cpp",
        "discussion_id": "1562079542",
        "commented_code": "@@ -278,8 +278,16 @@ void Mat::convertTo(OutputArray dst, int type_, double alpha, double beta) const\n     int dtype = CV_MAKETYPE(ddepth, cn);\n \n     Mat src = *this;\n-    dst.create(dims, size, dtype);\n-    Mat dstMat = dst.getMat();\n+    Mat dstMat;\n+    if (this->data == dst.getMat().data && this->elemSize() == CV_ELEM_SIZE(dtype)) {",
        "comment_created_at": "2024-04-14T13:19:50+00:00",
        "comment_author": "Gao-HaoYuan",
        "comment_body": "`Mat m (10, 10, CV_8U); Mat m2(10, 10, CV_8U, m.ptr<uint8_t>()); m.convertTo(m, CV_8S);`\r\n\r\nAnd, in this case, the original data of 'm' will be released, and 'm2' may encounter unpredictable errors. I believe such risky behavior should be noted by OpenCV users.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1930610880",
    "pr_number": 26831,
    "pr_file": "modules/photo/test/test_denoising.cpp",
    "created_at": "2025-01-27T14:22:49+00:00",
    "commented_code": "t = (double)getTickCount() - t;\n    printf(\"execution time: %gms\\n\", t*1000./getTickFrequency());\n}\n// Related issue :\n// - https://github.com/opencv/opencv/issues/26582\nclass Photo_DenoisingGrayscaleMulti16Bit : public ::testing::Test {\nprotected:\n    struct TestConfig {\n        int width = 127;\n        int height = 129;\n        int imgs_count = 3;\n        float h = 15.0f;\n        int templateWindowSize = 7;\n        int searchWindowSize = 21;\n    };\n\n    static double computePSNR(const cv::Mat& I1, const cv::Mat& I2) {\n        CV_Assert(I1.type() == I2.type() && I1.size() == I2.size());\n        cv::Mat s1;\n        cv::absdiff(I1, I2, s1);\n        s1.convertTo(s1, CV_32F);\n        s1 = s1.mul(s1);\n        cv::Scalar s = cv::sum(s1);\n        double mse = s[0] / static_cast<double>(I1.total());\n\n        if (mse == 0) return INFINITY;\n\n        double max_pixel = 65535.0;\n        return 10.0 * log10((max_pixel * max_pixel) / mse);\n    }",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1930610880",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26831,
        "pr_file": "modules/photo/test/test_denoising.cpp",
        "discussion_id": "1930610880",
        "commented_code": "@@ -164,5 +164,80 @@ TEST(Photo_Denoising, speed)\n     t = (double)getTickCount() - t;\n     printf(\"execution time: %gms\\n\", t*1000./getTickFrequency());\n }\n+// Related issue :\n+// - https://github.com/opencv/opencv/issues/26582\n+class Photo_DenoisingGrayscaleMulti16Bit : public ::testing::Test {\n+protected:\n+    struct TestConfig {\n+        int width = 127;\n+        int height = 129;\n+        int imgs_count = 3;\n+        float h = 15.0f;\n+        int templateWindowSize = 7;\n+        int searchWindowSize = 21;\n+    };\n+\n+    static double computePSNR(const cv::Mat& I1, const cv::Mat& I2) {\n+        CV_Assert(I1.type() == I2.type() && I1.size() == I2.size());\n+        cv::Mat s1;\n+        cv::absdiff(I1, I2, s1);\n+        s1.convertTo(s1, CV_32F);\n+        s1 = s1.mul(s1);\n+        cv::Scalar s = cv::sum(s1);\n+        double mse = s[0] / static_cast<double>(I1.total());\n+\n+        if (mse == 0) return INFINITY;\n+\n+        double max_pixel = 65535.0;\n+        return 10.0 * log10((max_pixel * max_pixel) / mse);\n+    }",
        "comment_created_at": "2025-01-27T14:22:49+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "Please use cv::PSNR instead: https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga3119e3ea73010a6f810bb05aa36ac8d6",
        "pr_file_module": null
      },
      {
        "comment_id": "1930621103",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26831,
        "pr_file": "modules/photo/test/test_denoising.cpp",
        "discussion_id": "1930610880",
        "commented_code": "@@ -164,5 +164,80 @@ TEST(Photo_Denoising, speed)\n     t = (double)getTickCount() - t;\n     printf(\"execution time: %gms\\n\", t*1000./getTickFrequency());\n }\n+// Related issue :\n+// - https://github.com/opencv/opencv/issues/26582\n+class Photo_DenoisingGrayscaleMulti16Bit : public ::testing::Test {\n+protected:\n+    struct TestConfig {\n+        int width = 127;\n+        int height = 129;\n+        int imgs_count = 3;\n+        float h = 15.0f;\n+        int templateWindowSize = 7;\n+        int searchWindowSize = 21;\n+    };\n+\n+    static double computePSNR(const cv::Mat& I1, const cv::Mat& I2) {\n+        CV_Assert(I1.type() == I2.type() && I1.size() == I2.size());\n+        cv::Mat s1;\n+        cv::absdiff(I1, I2, s1);\n+        s1.convertTo(s1, CV_32F);\n+        s1 = s1.mul(s1);\n+        cv::Scalar s = cv::sum(s1);\n+        double mse = s[0] / static_cast<double>(I1.total());\n+\n+        if (mse == 0) return INFINITY;\n+\n+        double max_pixel = 65535.0;\n+        return 10.0 * log10((max_pixel * max_pixel) / mse);\n+    }",
        "comment_created_at": "2025-01-27T14:29:00+00:00",
        "comment_author": "shyama7004",
        "comment_body": "Ok, I will .",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1915996982",
    "pr_number": 26773,
    "pr_file": "modules/imgproc/src/shapedescr.cpp",
    "created_at": "2025-01-15T06:18:42+00:00",
    "commented_code": "static inline Point2f getOfs(int i, float eps)\n{\n    return Point2f(((i & 1)*2 - 1)*eps, ((i & 2) - 1)*eps);\n    std::mt19937 gen(i);\n    std::uniform_real_distribution<float> dis(-eps, eps);\n    return Point2f(dis(gen), dis(gen));",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1915996982",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26773,
        "pr_file": "modules/imgproc/src/shapedescr.cpp",
        "discussion_id": "1915996982",
        "commented_code": "@@ -342,7 +342,9 @@ namespace cv\n \n static inline Point2f getOfs(int i, float eps)\n {\n-    return Point2f(((i & 1)*2 - 1)*eps, ((i & 2) - 1)*eps);\n+    std::mt19937 gen(i);\n+    std::uniform_real_distribution<float> dis(-eps, eps);\n+    return Point2f(dis(gen), dis(gen));",
        "comment_created_at": "2025-01-15T06:18:42+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I propose to use cv::RNG for it to make it manageable outside:\r\n- User may set seed to get deterministic behaviour\r\n- OpenCV test system fixes cv::RNG seed for each test independently.",
        "pr_file_module": null
      },
      {
        "comment_id": "1917342515",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26773,
        "pr_file": "modules/imgproc/src/shapedescr.cpp",
        "discussion_id": "1915996982",
        "commented_code": "@@ -342,7 +342,9 @@ namespace cv\n \n static inline Point2f getOfs(int i, float eps)\n {\n-    return Point2f(((i & 1)*2 - 1)*eps, ((i & 2) - 1)*eps);\n+    std::mt19937 gen(i);\n+    std::uniform_real_distribution<float> dis(-eps, eps);\n+    return Point2f(dis(gen), dis(gen));",
        "comment_created_at": "2025-01-15T21:14:07+00:00",
        "comment_author": "MaximSmolskiy",
        "comment_body": "Used `cv::RNG`",
        "pr_file_module": null
      }
    ]
  }
]
