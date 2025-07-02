---
title: Validate tensor dimensions
description: When implementing AI model inference code, always validate tensor dimensions
  and shapes before manipulating them. Neural network outputs often have complex multi-dimensional
  structures that require careful handling. Adding explicit dimension checks prevents
  subtle runtime errors, improves code robustness, and makes debugging easier.
repository: opencv/opencv
label: AI
language: C++
comments_count: 3
repository_stars: 82865
---

When implementing AI model inference code, always validate tensor dimensions and shapes before manipulating them. Neural network outputs often have complex multi-dimensional structures that require careful handling. Adding explicit dimension checks prevents subtle runtime errors, improves code robustness, and makes debugging easier.

Before reshaping tensors or extracting specific values:
1. Check that the tensor has the expected number of dimensions
2. Verify tensor shapes match your expectations
3. Add defensive assertions for critical assumptions

Example:
```cpp
// Before tensor manipulation, add validation
CV_CheckEQ(outs[0].dims, 3, "Expected 3D tensor output");
CV_CheckEQ((outs[0].size[2] == nc + 5 || outs[0].size[2] == nc + 4), true, "Invalid output shape");

// Then proceed with manipulation
vector<Mat> channels;
for (int i = 0; i < 3; ++i) {
    channels.push_back(Mat(output_transposed.size[1], output_transposed.size[2], CV_32F,
                           output_transposed.ptr<float>(i)));
}
```

For parameters derived from tensor shapes, consider whether they should be computed or passed as parameters based on the model's architecture. Always document your assumptions about tensor shapes, especially when working with different AI model formats or versions.


[
  {
    "discussion_id": "2137760658",
    "pr_number": 27349,
    "pr_file": "samples/dnn/deblurring.cpp",
    "created_at": "2025-06-10T12:25:20+00:00",
    "commented_code": "/*\nThis file is part of OpenCV project.\nIt is subject to the license terms in the LICENSE file found in the top-level directory\nof this distribution and at http://opencv.org/license.html.\n\nThis sample deblurs the given blurry image.\n\nCopyright (C) 2025, Bigvision LLC.\n\nHow to use:\n    Sample command to run:\n        `./example_dnn_deblurring`\n\n    You can download NAFNet deblurring model using\n        `python download_models.py NAFNet`\n\n    References:\n      Github: https://github.com/megvii-research/NAFNet\n      PyTorch model: https://drive.google.com/file/d/14D4V4raNYIOhETfcuuLI3bGLB-OYIv6X/view\n\n      PyTorch model was converted to ONNX and then ONNX model was further quantized using block quantization from [opencv_zoo](https://github.com/opencv/opencv_zoo/blob/main/tools/quantize/block_quantize.py)\n\n    Set environment variable OPENCV_DOWNLOAD_CACHE_DIR to point to the directory where models are downloaded. Also, point OPENCV_SAMPLES_DATA_PATH to opencv/samples/data.\n*/\n\n#include <iostream>\n#include <fstream>\n\n#include <opencv2/imgproc.hpp>\n#include <opencv2/highgui.hpp>\n#include <opencv2/dnn.hpp>\n\n#include \"common.hpp\"\n\nusing namespace cv;\nusing namespace dnn;\nusing namespace std;\n\nconst string about = \"Use this script for image deblurring using OpenCV. \\n\\n\"\n        \"Firstly, download required models i.e. NAFNet using `download_models.py` (if not already done). Set environment variable OPENCV_DOWNLOAD_CACHE_DIR to point to the directory where models are downloaded. Also, point OPENCV_SAMPLES_DATA_PATH to opencv/samples/data.\\n\"\n        \"To run:\\n\"\n        \"\\t Example: ./example_dnn_deblurring [--input=<image_name>] \\n\\n\"\n        \"Deblurring model path can also be specified using --model argument.\\n\\n\";\n\nconst string param_keys =\n    \"{ help    h  |                           | show help message}\"\n    \"{ @alias     |           NAFNet          | An alias name of model to extract preprocessing parameters from models.yml file. }\"\n    \"{ zoo        |     ../dnn/models.yml     | An optional path to file with preprocessing parameters }\"\n    \"{ input   i  |  licenseplate_motion.jpg  | image file path}\";\n\nconst string backend_keys = format(\n    \"{ backend | default | Choose one of computation backends: \"\n    \"default: automatically (by default), \"\n    \"openvino: Intel's Deep Learning Inference Engine (https://software.intel.com/openvino-toolkit), \"\n    \"opencv: OpenCV implementation, \"\n    \"vkcom: VKCOM, \"\n    \"cuda: CUDA, \"\n    \"webnn: WebNN }\");\n\nconst string target_keys = format(\n    \"{ target | cpu | Choose one of target computation devices: \"\n    \"cpu: CPU target (by default), \"\n    \"opencl: OpenCL, \"\n    \"opencl_fp16: OpenCL fp16 (half-float precision), \"\n    \"vpu: VPU, \"\n    \"vulkan: Vulkan, \"\n    \"cuda: CUDA, \"\n    \"cuda_fp16: CUDA fp16 (half-float preprocess) }\");\n\nstring keys = param_keys + backend_keys + target_keys;\n\n\nint main(int argc, char **argv)\n{\n    CommandLineParser parser(argc, argv, keys);\n\n    if (!parser.has(\"@alias\") || parser.has(\"help\"))\n    {\n        cout<<about<<endl;\n        parser.printMessage();\n        return 0;\n    }\n    string modelName = parser.get<String>(\"@alias\");\n    string zooFile = findFile(parser.get<String>(\"zoo\"));\n    keys += genPreprocArguments(modelName, zooFile);\n    parser = CommandLineParser(argc, argv, keys);\n    parser.about(\"Use this script to run image deblurring using OpenCV.\");\n\n    const string sha1 = parser.get<String>(\"sha1\");\n    const string modelPath = findModel(parser.get<String>(\"model\"), sha1);\n    string imgPath = parser.get<String>(\"input\");\n    const string backend = parser.get<String>(\"backend\");\n    const string target = parser.get<String>(\"target\");\n    float scale = parser.get<float>(\"scale\");\n    bool swapRB = parser.get<bool>(\"rgb\");\n    Scalar mean_v = parser.get<Scalar>(\"mean\");\n\n    EngineType engine = ENGINE_AUTO;\n    if (backend != \"default\" || target != \"cpu\"){\n        engine = ENGINE_CLASSIC;\n    }\n\n    Net net = readNetFromONNX(modelPath, engine);\n    net.setPreferableBackend(getBackendID(backend));\n    net.setPreferableTarget(getTargetID(target));\n\n    Mat inputImage = imread(findFile(imgPath));\n    if (inputImage.empty()) {\n        cerr << \"Error: Input image could not be loaded.\" << endl;\n        return -1;\n    }\n    Mat image = inputImage.clone();\n\n    Mat image_blob = blobFromImage(image, scale, Size(image.cols, image.rows), mean_v, swapRB, false);\n\n    net.setInput(image_blob);\n    Mat output = net.forward();\n\n    // Post Processing\n    Mat output_transposed(3, &output.size[1], CV_32F, output.ptr<float>());\n\n    vector<Mat> channels;\n    for (int i = 0; i < 3; ++i) {\n        channels.push_back(Mat(output_transposed.size[1], output_transposed.size[2], CV_32F,\n                                    output_transposed.ptr<float>(i)));\n    }",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2137760658",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27349,
        "pr_file": "samples/dnn/deblurring.cpp",
        "discussion_id": "2137760658",
        "commented_code": "@@ -0,0 +1,136 @@\n+/*\n+This file is part of OpenCV project.\n+It is subject to the license terms in the LICENSE file found in the top-level directory\n+of this distribution and at http://opencv.org/license.html.\n+\n+This sample deblurs the given blurry image.\n+\n+Copyright (C) 2025, Bigvision LLC.\n+\n+How to use:\n+    Sample command to run:\n+        `./example_dnn_deblurring`\n+\n+    You can download NAFNet deblurring model using\n+        `python download_models.py NAFNet`\n+\n+    References:\n+      Github: https://github.com/megvii-research/NAFNet\n+      PyTorch model: https://drive.google.com/file/d/14D4V4raNYIOhETfcuuLI3bGLB-OYIv6X/view\n+\n+      PyTorch model was converted to ONNX and then ONNX model was further quantized using block quantization from [opencv_zoo](https://github.com/opencv/opencv_zoo/blob/main/tools/quantize/block_quantize.py)\n+\n+    Set environment variable OPENCV_DOWNLOAD_CACHE_DIR to point to the directory where models are downloaded. Also, point OPENCV_SAMPLES_DATA_PATH to opencv/samples/data.\n+*/\n+\n+#include <iostream>\n+#include <fstream>\n+\n+#include <opencv2/imgproc.hpp>\n+#include <opencv2/highgui.hpp>\n+#include <opencv2/dnn.hpp>\n+\n+#include \"common.hpp\"\n+\n+using namespace cv;\n+using namespace dnn;\n+using namespace std;\n+\n+const string about = \"Use this script for image deblurring using OpenCV. \\n\\n\"\n+        \"Firstly, download required models i.e. NAFNet using `download_models.py` (if not already done). Set environment variable OPENCV_DOWNLOAD_CACHE_DIR to point to the directory where models are downloaded. Also, point OPENCV_SAMPLES_DATA_PATH to opencv/samples/data.\\n\"\n+        \"To run:\\n\"\n+        \"\\t Example: ./example_dnn_deblurring [--input=<image_name>] \\n\\n\"\n+        \"Deblurring model path can also be specified using --model argument.\\n\\n\";\n+\n+const string param_keys =\n+    \"{ help    h  |                           | show help message}\"\n+    \"{ @alias     |           NAFNet          | An alias name of model to extract preprocessing parameters from models.yml file. }\"\n+    \"{ zoo        |     ../dnn/models.yml     | An optional path to file with preprocessing parameters }\"\n+    \"{ input   i  |  licenseplate_motion.jpg  | image file path}\";\n+\n+const string backend_keys = format(\n+    \"{ backend | default | Choose one of computation backends: \"\n+    \"default: automatically (by default), \"\n+    \"openvino: Intel's Deep Learning Inference Engine (https://software.intel.com/openvino-toolkit), \"\n+    \"opencv: OpenCV implementation, \"\n+    \"vkcom: VKCOM, \"\n+    \"cuda: CUDA, \"\n+    \"webnn: WebNN }\");\n+\n+const string target_keys = format(\n+    \"{ target | cpu | Choose one of target computation devices: \"\n+    \"cpu: CPU target (by default), \"\n+    \"opencl: OpenCL, \"\n+    \"opencl_fp16: OpenCL fp16 (half-float precision), \"\n+    \"vpu: VPU, \"\n+    \"vulkan: Vulkan, \"\n+    \"cuda: CUDA, \"\n+    \"cuda_fp16: CUDA fp16 (half-float preprocess) }\");\n+\n+string keys = param_keys + backend_keys + target_keys;\n+\n+\n+int main(int argc, char **argv)\n+{\n+    CommandLineParser parser(argc, argv, keys);\n+\n+    if (!parser.has(\"@alias\") || parser.has(\"help\"))\n+    {\n+        cout<<about<<endl;\n+        parser.printMessage();\n+        return 0;\n+    }\n+    string modelName = parser.get<String>(\"@alias\");\n+    string zooFile = findFile(parser.get<String>(\"zoo\"));\n+    keys += genPreprocArguments(modelName, zooFile);\n+    parser = CommandLineParser(argc, argv, keys);\n+    parser.about(\"Use this script to run image deblurring using OpenCV.\");\n+\n+    const string sha1 = parser.get<String>(\"sha1\");\n+    const string modelPath = findModel(parser.get<String>(\"model\"), sha1);\n+    string imgPath = parser.get<String>(\"input\");\n+    const string backend = parser.get<String>(\"backend\");\n+    const string target = parser.get<String>(\"target\");\n+    float scale = parser.get<float>(\"scale\");\n+    bool swapRB = parser.get<bool>(\"rgb\");\n+    Scalar mean_v = parser.get<Scalar>(\"mean\");\n+\n+    EngineType engine = ENGINE_AUTO;\n+    if (backend != \"default\" || target != \"cpu\"){\n+        engine = ENGINE_CLASSIC;\n+    }\n+\n+    Net net = readNetFromONNX(modelPath, engine);\n+    net.setPreferableBackend(getBackendID(backend));\n+    net.setPreferableTarget(getTargetID(target));\n+\n+    Mat inputImage = imread(findFile(imgPath));\n+    if (inputImage.empty()) {\n+        cerr << \"Error: Input image could not be loaded.\" << endl;\n+        return -1;\n+    }\n+    Mat image = inputImage.clone();\n+\n+    Mat image_blob = blobFromImage(image, scale, Size(image.cols, image.rows), mean_v, swapRB, false);\n+\n+    net.setInput(image_blob);\n+    Mat output = net.forward();\n+\n+    // Post Processing\n+    Mat output_transposed(3, &output.size[1], CV_32F, output.ptr<float>());\n+\n+    vector<Mat> channels;\n+    for (int i = 0; i < 3; ++i) {\n+        channels.push_back(Mat(output_transposed.size[1], output_transposed.size[2], CV_32F,\n+                                    output_transposed.ptr<float>(i)));\n+    }",
        "comment_created_at": "2025-06-10T12:25:20+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "```\r\nvector<Mat> channels = {\r\n    Mat(output_transposed.size[1], output_transposed.size[2], CV_32F, output_transposed.ptr<float>(0)),\r\n    Mat(output_transposed.size[1], output_transposed.size[2], CV_32F, output_transposed.ptr<float>(1)),\r\n    Mat(output_transposed.size[1], output_transposed.size[2], CV_32F, output_transposed.ptr<float>(2))\r\n};\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1648004283",
    "pr_number": 25794,
    "pr_file": "samples/dnn/yolo_detector.cpp",
    "created_at": "2024-06-20T18:51:56+00:00",
    "commented_code": "// remove the second element\n        outs.pop_back();\n        // unsqueeze the first dimension\n        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});\n    }\n\n    // assert if last dim is 85 or 84\n    CV_CheckEQ((outs[0].size[2] == nc + 5 || outs[0].size[2] == 80 + 4), true, \"Invalid output shape: \");",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1648004283",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648004283",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});\n     }\n \n+    // assert if last dim is 85 or 84\n+    CV_CheckEQ((outs[0].size[2] == nc + 5 || outs[0].size[2] == 80 + 4), true, \"Invalid output shape: \");",
        "comment_created_at": "2024-06-20T18:51:56+00:00",
        "comment_author": "dkurt",
        "comment_body": "Check also that `outs[0].dims == 2` before.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1648007571",
    "pr_number": 25794,
    "pr_file": "samples/dnn/yolo_detector.cpp",
    "created_at": "2024-06-20T18:55:17+00:00",
    "commented_code": "// remove the second element\n        outs.pop_back();\n        // unsqueeze the first dimension\n        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1648007571",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-20T18:55:17+00:00",
        "comment_author": "dkurt",
        "comment_body": "8400 is also depends on number of classes? So should it be `(nc + 4) * 100` or not?",
        "pr_file_module": null
      },
      {
        "comment_id": "1648011078",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-20T18:58:57+00:00",
        "comment_author": "dkurt",
        "comment_body": "`nc` seems redundant as it can be computed from original shape:\r\n```cpp\r\nint nc = outs[0].total() / 8400 - 4;\r\n```\r\nor, if 8400 is also depends on `nc`:\r\n```cpp\r\nint nc = sqrt(outs[0].total() / 100) - 4;\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1648490438",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-21T06:45:46+00:00",
        "comment_author": "Abdurrahheem",
        "comment_body": "> 8400 is also depends on number of classes? So should it be `(nc + 4) * 100` or not?\r\n\r\n8400 depends on number of anchors only and has nothing to do with `nc`. \r\n`nc` depends on which dataset detector what trained. On `COCO` dataset `nc = 80`. For other datasets it might be different. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1648498046",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-21T06:54:18+00:00",
        "comment_author": "dkurt",
        "comment_body": "Got it, thanks! So do you mind to compute `nc` from total number of `outs[0]` elements?",
        "pr_file_module": null
      },
      {
        "comment_id": "1650834099",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-24T11:06:30+00:00",
        "comment_author": "Abdurrahheem",
        "comment_body": "I strongly believe that it should stay as a papermeter. As this is a parameter during traning. Computing it via `outs[0]` is kind of hack. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1654471328",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-26T09:36:20+00:00",
        "comment_author": "dkurt",
        "comment_body": "The corner case is a background class. Some training utils may include this as a separate class - some not. So even if you trained model for 80 real classes, there is a variation nc=80 nc=81 and it may confuse even more.",
        "pr_file_module": null
      },
      {
        "comment_id": "1654779677",
        "repo_full_name": "opencv/opencv",
        "pr_number": 25794,
        "pr_file": "samples/dnn/yolo_detector.cpp",
        "discussion_id": "1648007571",
        "commented_code": "@@ -131,25 +133,28 @@ void yoloPostProcessing(\n         // remove the second element\n         outs.pop_back();\n         // unsqueeze the first dimension\n-        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, 84});\n+        outs[0] = outs[0].reshape(0, std::vector<int>{1, 8400, nc + 4});",
        "comment_created_at": "2024-06-26T12:59:39+00:00",
        "comment_author": "Abdurrahheem",
        "comment_body": "Computing `nc` using number of anchor points is not good since number of anchors depens on the image size. Inference can happen on different image resolutons, depending on use case. ",
        "pr_file_module": null
      }
    ]
  }
]
