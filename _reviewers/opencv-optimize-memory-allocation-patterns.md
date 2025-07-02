---
title: Optimize memory allocation patterns
description: 'Prefer efficient memory allocation patterns to improve performance.
  Key practices:


  1. Use RAII containers (like Mat) instead of raw pointers to prevent memory leaks'
repository: opencv/opencv
label: Performance Optimization
language: C++
comments_count: 5
repository_stars: 82865
---

Prefer efficient memory allocation patterns to improve performance. Key practices:

1. Use RAII containers (like Mat) instead of raw pointers to prevent memory leaks
2. Pre-allocate containers when size is known
3. Use stack allocation for small, fixed-size objects
4. Avoid unnecessary dynamic allocation

Example - Before:
```cpp
// Inefficient allocation patterns
char* get_raw_data() {
    return new char[size];  // Raw pointer, potential memory leak
}

std::vector<Mat> img_vec;
img_vec.push_back(img);  // Potential reallocation

fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];  // Unnecessary heap allocation
```

Example - After:
```cpp
// Efficient allocation patterns
Mat get_data() {
    return Mat(size);  // RAII handles cleanup
}

std::vector<Mat> img_vec(1, img);  // Pre-allocated size

fcvPyramidLevel_v2 framePyr[2];  // Stack allocation for small arrays
```

Benefits:
- Prevents memory leaks
- Reduces allocation overhead
- Improves cache utilization
- More predictable performance


[
  {
    "discussion_id": "2151339001",
    "pr_number": 27449,
    "pr_file": "modules/dnn/src/onnx/onnx_graph_simplifier.cpp",
    "created_at": "2025-06-17T05:16:02+00:00",
    "commented_code": "simplifySubgraphs(Ptr<ImportGraphWrapper>(new ONNXGraphWrapper(net)), subgraphs);\n}\n\nMat getMatFromTensor(const opencv_onnx::TensorProto& tensor_proto, bool uint8ToInt8)\n\n\nchar* get_raw_data(const opencv_onnx::TensorProto& tensor_proto, const std::string base_path = \"\"){",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2151339001",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27449,
        "pr_file": "modules/dnn/src/onnx/onnx_graph_simplifier.cpp",
        "discussion_id": "2151339001",
        "commented_code": "@@ -1704,29 +1704,63 @@ void simplifySubgraphs(opencv_onnx::GraphProto& net)\n     simplifySubgraphs(Ptr<ImportGraphWrapper>(new ONNXGraphWrapper(net)), subgraphs);\n }\n \n-Mat getMatFromTensor(const opencv_onnx::TensorProto& tensor_proto, bool uint8ToInt8)\n+\n+\n+char* get_raw_data(const opencv_onnx::TensorProto& tensor_proto, const std::string base_path = \"\"){",
        "comment_created_at": "2025-06-17T05:16:02+00:00",
        "comment_author": "vpisarev",
        "comment_body": "I'd suggest to modify this function (and probably rename it) to return `Mat` instead of plain pointer. This way we can track memory allocations properly. Currently, I suspect, there are memory leaks.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2053540731",
    "pr_number": 27177,
    "pr_file": "modules/dnn/src/llm/gguf_parser.cpp",
    "created_at": "2025-04-22T07:49:08+00:00",
    "commented_code": "#include \"../precomp.hpp\"\n#include \"gguf_parser.hpp\"\n//#include \"gguf_buffer.hpp\"\n#include <fstream>\n#include \"opencv2/core.hpp\"\n\nnamespace cv { namespace dnn {\nCV__DNN_INLINE_NS_BEGIN\nusing namespace dnn;\n\ntensor_role get_tensor_role(std::string name) {\n    if (name == \"attn_norm\") return tensor_role::attn_norm;\n    if (name == \"attn_norm_2\") return tensor_role::attn_norm_2;\n    if (name == \"attn_qkv\") return tensor_role::attn_qkv;\n    if (name == \"attn_q\") return tensor_role::attn_q;\n    if (name == \"attn_k\") return tensor_role::attn_k;\n    if (name == \"attn_v\") return tensor_role::attn_v;\n    if (name == \"attn_output\") return tensor_role::attn_output;\n    if (name == \"ffn_norm\") return tensor_role::ffn_norm;\n    if (name == \"ffn_up\") return tensor_role::ffn_up;\n    if (name == \"ffn_gate\") return tensor_role::ffn_gate;\n    if (name == \"ffn_down\") return tensor_role::ffn_down;\n    if (name == \"ffn_gate_inp\") return tensor_role::ffn_gate_inp;\n    if (name == \"ffn_gate_exp\") return tensor_role::ffn_gate_exp;\n    if (name == \"ffn_down_exp\") return tensor_role::ffn_down_exp;\n    if (name == \"ffn_up_exp\") return tensor_role::ffn_up_exp;\n    throw std::runtime_error(\"Unknown tensor role: \" + name);\n}\n\nMat TensorMetadata::getMat(Ptr<GGUFBufferReader> tensor_reader) {\n    if (type != GGML_TYPE_F32) {\n        throw std::runtime_error(\"Unsupported tensor type: \" + std::to_string(type));\n    }\n    if (dims.size() == 2) \n        return tensor_reader->read2DMat(\n            GGML_TYPE_F32, dims[0],dims[1], data_offset\n        );\n    if (dims.size() == 1) \n        return tensor_reader->read1DMat(\n            GGML_TYPE_F32, dims[0], data_offset\n        );\n\n    throw std::runtime_error(\n        \"Unsupported tensor dimension: \" + std::to_string(dims.size()));\n};\n\nstd::string GGUFParser::get_architecture(){\n    return getStringMetadata(\"architecture\");\n};\n\nMatShape BlockMetadata::getInputShape() \n{\n    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n    if (t.size() == 0) {\n        throw std::runtime_error(\"No input tensors found\");\n    }\n\n    MatShape inputShape(3);\n    inputShape[0] = 1; inputShape[1] = -1;\n    inputShape[2] = t[0].dims[1];\n    return inputShape;\n}\n\nint BlockMetadata::getDhidden() \n{\n    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n    if (t.size() == 0) {\n        throw std::runtime_error(\"No input tensors found\");\n    }\n    return t[0].dims[0] / 3;\n}\n\nMatShape BlockMetadata::getOutputShape() \n{\n    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n    if (t.size() == 0) {\n        throw std::runtime_error(\"No input tensors found\");\n    }\n\n    MatShape outputShape(3);\n    outputShape[0] = 1; outputShape[1] = -1;\n    outputShape[2] = t[0].dims[1];\n    return outputShape;\n}\n\nvoid BlockMetadata::getAttentionLayerParams(Ptr<GGUFBufferReader> tensor_reader, LayerParams& layerParams) \n{\n    layerParams.type = \"Attention\";\n    layerParams.name = \"attention_block\";\n    layerParams.set(\"num_heads\", n_heads);\n    layerParams.set(\"blockn\", blockn);\n    int d_hidden = getDhidden();\n    std::vector<int> qkv_hidden_sizes = {d_hidden, d_hidden, d_hidden};\n    layerParams.set(\"qkv_hidden_sizes\", DictValue::arrayInt(&qkv_hidden_sizes[0], 3));\n    Mat qkv_weight = getTensorMetadata(tensor_role::attn_qkv, false, false)[0].getMat(tensor_reader);\n    Mat qkv_bias = getTensorMetadata(tensor_role::attn_qkv, true, false)[0].getMat(tensor_reader);\n    layerParams.blobs.push_back(qkv_weight.t());\n    layerParams.blobs.push_back(qkv_bias);\n}\n\nstd::vector<TensorMetadata> BlockMetadata::getTensorMetadata(tensor_role role, bool is_bias, bool allow_multiple) {\n    std::vector<TensorMetadata> result;\n    for (const auto & tensor : tensors) {\n        if (tensor.role == role && tensor.is_bias == is_bias) {\n            result.push_back(tensor);\n        }\n    }\n    return result;\n    if (!allow_multiple && result.size() > 1) {\n        throw std::runtime_error(\"Multiple tensors found for role: \" + std::to_string(role));\n    }\n    return result;\n}\n\nvoid GGUFParser::addTensorMetadata() {\n    auto tensor = TensorMetadata();\n\n    std::string tensor_name = reader.readString();\n    std::regex layerRegex(R\"(^blk\\.(\\d+)\\.([a-zA-Z0-9_]+)\\.(weight|bias)$)\");\n    std::smatch match;\n    std::string layerName, paramType;\n\n    int blockn;\n\n    if (std::regex_match(tensor_name, match, layerRegex)) {\n        blockn = std::stoi(match[1].str());\n        layerName = match[2].str();\n        paramType = match[3].str();\n        if (paramType == \"weight\") {\n            tensor.is_bias = false;\n        } else if (paramType == \"bias\") {\n            tensor.is_bias = true;\n        } else {\n            throw std::runtime_error(\"Unknown parameter type: \" + paramType);\n        }\n        tensor.role = get_tensor_role(layerName);\n        tensor.n_block = blockn;\n    } else {\n        throw std::runtime_error(\"Invalid tensor name format: \" + tensor_name);\n    }\n\n    int dim_count = reader.readSingleValueInt<uint32_t>();\n    tensor.dims = MatShape(dim_count);\n    std::vector<int> dims;\n    for (uint32_t i = 0; i < dim_count; ++i) {\n        dims.push_back(reader.readSingleValueInt<int64_t>());    \n    }",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "2053540731",
        "repo_full_name": "opencv/opencv",
        "pr_number": 27177,
        "pr_file": "modules/dnn/src/llm/gguf_parser.cpp",
        "discussion_id": "2053540731",
        "commented_code": "@@ -0,0 +1,235 @@\n+#include \"../precomp.hpp\"\n+#include \"gguf_parser.hpp\"\n+//#include \"gguf_buffer.hpp\"\n+#include <fstream>\n+#include \"opencv2/core.hpp\"\n+\n+namespace cv { namespace dnn {\n+CV__DNN_INLINE_NS_BEGIN\n+using namespace dnn;\n+\n+tensor_role get_tensor_role(std::string name) {\n+    if (name == \"attn_norm\") return tensor_role::attn_norm;\n+    if (name == \"attn_norm_2\") return tensor_role::attn_norm_2;\n+    if (name == \"attn_qkv\") return tensor_role::attn_qkv;\n+    if (name == \"attn_q\") return tensor_role::attn_q;\n+    if (name == \"attn_k\") return tensor_role::attn_k;\n+    if (name == \"attn_v\") return tensor_role::attn_v;\n+    if (name == \"attn_output\") return tensor_role::attn_output;\n+    if (name == \"ffn_norm\") return tensor_role::ffn_norm;\n+    if (name == \"ffn_up\") return tensor_role::ffn_up;\n+    if (name == \"ffn_gate\") return tensor_role::ffn_gate;\n+    if (name == \"ffn_down\") return tensor_role::ffn_down;\n+    if (name == \"ffn_gate_inp\") return tensor_role::ffn_gate_inp;\n+    if (name == \"ffn_gate_exp\") return tensor_role::ffn_gate_exp;\n+    if (name == \"ffn_down_exp\") return tensor_role::ffn_down_exp;\n+    if (name == \"ffn_up_exp\") return tensor_role::ffn_up_exp;\n+    throw std::runtime_error(\"Unknown tensor role: \" + name);\n+}\n+\n+Mat TensorMetadata::getMat(Ptr<GGUFBufferReader> tensor_reader) {\n+    if (type != GGML_TYPE_F32) {\n+        throw std::runtime_error(\"Unsupported tensor type: \" + std::to_string(type));\n+    }\n+    if (dims.size() == 2) \n+        return tensor_reader->read2DMat(\n+            GGML_TYPE_F32, dims[0],dims[1], data_offset\n+        );\n+    if (dims.size() == 1) \n+        return tensor_reader->read1DMat(\n+            GGML_TYPE_F32, dims[0], data_offset\n+        );\n+\n+    throw std::runtime_error(\n+        \"Unsupported tensor dimension: \" + std::to_string(dims.size()));\n+};\n+\n+std::string GGUFParser::get_architecture(){\n+    return getStringMetadata(\"architecture\");\n+};\n+\n+MatShape BlockMetadata::getInputShape() \n+{\n+    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n+    if (t.size() == 0) {\n+        throw std::runtime_error(\"No input tensors found\");\n+    }\n+\n+    MatShape inputShape(3);\n+    inputShape[0] = 1; inputShape[1] = -1;\n+    inputShape[2] = t[0].dims[1];\n+    return inputShape;\n+}\n+\n+int BlockMetadata::getDhidden() \n+{\n+    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n+    if (t.size() == 0) {\n+        throw std::runtime_error(\"No input tensors found\");\n+    }\n+    return t[0].dims[0] / 3;\n+}\n+\n+MatShape BlockMetadata::getOutputShape() \n+{\n+    std::vector<TensorMetadata> t = getTensorMetadata( tensor_role::attn_qkv, false, false);\n+    if (t.size() == 0) {\n+        throw std::runtime_error(\"No input tensors found\");\n+    }\n+\n+    MatShape outputShape(3);\n+    outputShape[0] = 1; outputShape[1] = -1;\n+    outputShape[2] = t[0].dims[1];\n+    return outputShape;\n+}\n+\n+void BlockMetadata::getAttentionLayerParams(Ptr<GGUFBufferReader> tensor_reader, LayerParams& layerParams) \n+{\n+    layerParams.type = \"Attention\";\n+    layerParams.name = \"attention_block\";\n+    layerParams.set(\"num_heads\", n_heads);\n+    layerParams.set(\"blockn\", blockn);\n+    int d_hidden = getDhidden();\n+    std::vector<int> qkv_hidden_sizes = {d_hidden, d_hidden, d_hidden};\n+    layerParams.set(\"qkv_hidden_sizes\", DictValue::arrayInt(&qkv_hidden_sizes[0], 3));\n+    Mat qkv_weight = getTensorMetadata(tensor_role::attn_qkv, false, false)[0].getMat(tensor_reader);\n+    Mat qkv_bias = getTensorMetadata(tensor_role::attn_qkv, true, false)[0].getMat(tensor_reader);\n+    layerParams.blobs.push_back(qkv_weight.t());\n+    layerParams.blobs.push_back(qkv_bias);\n+}\n+\n+std::vector<TensorMetadata> BlockMetadata::getTensorMetadata(tensor_role role, bool is_bias, bool allow_multiple) {\n+    std::vector<TensorMetadata> result;\n+    for (const auto & tensor : tensors) {\n+        if (tensor.role == role && tensor.is_bias == is_bias) {\n+            result.push_back(tensor);\n+        }\n+    }\n+    return result;\n+    if (!allow_multiple && result.size() > 1) {\n+        throw std::runtime_error(\"Multiple tensors found for role: \" + std::to_string(role));\n+    }\n+    return result;\n+}\n+\n+void GGUFParser::addTensorMetadata() {\n+    auto tensor = TensorMetadata();\n+\n+    std::string tensor_name = reader.readString();\n+    std::regex layerRegex(R\"(^blk\\.(\\d+)\\.([a-zA-Z0-9_]+)\\.(weight|bias)$)\");\n+    std::smatch match;\n+    std::string layerName, paramType;\n+\n+    int blockn;\n+\n+    if (std::regex_match(tensor_name, match, layerRegex)) {\n+        blockn = std::stoi(match[1].str());\n+        layerName = match[2].str();\n+        paramType = match[3].str();\n+        if (paramType == \"weight\") {\n+            tensor.is_bias = false;\n+        } else if (paramType == \"bias\") {\n+            tensor.is_bias = true;\n+        } else {\n+            throw std::runtime_error(\"Unknown parameter type: \" + paramType);\n+        }\n+        tensor.role = get_tensor_role(layerName);\n+        tensor.n_block = blockn;\n+    } else {\n+        throw std::runtime_error(\"Invalid tensor name format: \" + tensor_name);\n+    }\n+\n+    int dim_count = reader.readSingleValueInt<uint32_t>();\n+    tensor.dims = MatShape(dim_count);\n+    std::vector<int> dims;\n+    for (uint32_t i = 0; i < dim_count; ++i) {\n+        dims.push_back(reader.readSingleValueInt<int64_t>());    \n+    }",
        "comment_created_at": "2025-04-22T07:49:08+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "It's more efficient to use  std::vector<int> dims(dim_count); and assign values, rather than call push_back and trigger reallocations.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1930098040",
    "pr_number": 26844,
    "pr_file": "modules/imgcodecs/src/grfmt_jpegxl.cpp",
    "created_at": "2025-01-27T07:51:19+00:00",
    "commented_code": "bool JpegXLDecoder::readHeader()\n{\n    // Open file\n    if (!m_f) {\n        m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n        if (!m_f)\n            return false;\n    if (m_buf.empty()) {\n        // Open file\n        if (!m_f) {\n            m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n            if (!m_f) {\n                return false;\n            }\n        }\n        // Create buffer for reading file\n        constexpr size_t read_buffer_size = 16384;  // 16KB chunks\n        if (m_read_buffer.capacity() < read_buffer_size) {\n            m_read_buffer.resize(read_buffer_size);\n        }",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1930098040",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26844,
        "pr_file": "modules/imgcodecs/src/grfmt_jpegxl.cpp",
        "discussion_id": "1930098040",
        "commented_code": "@@ -91,11 +93,19 @@ ImageDecoder JpegXLDecoder::newDecoder() const\n \n bool JpegXLDecoder::readHeader()\n {\n-    // Open file\n-    if (!m_f) {\n-        m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n-        if (!m_f)\n-            return false;\n+    if (m_buf.empty()) {\n+        // Open file\n+        if (!m_f) {\n+            m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n+            if (!m_f) {\n+                return false;\n+            }\n+        }\n+        // Create buffer for reading file\n+        constexpr size_t read_buffer_size = 16384;  // 16KB chunks\n+        if (m_read_buffer.capacity() < read_buffer_size) {\n+            m_read_buffer.resize(read_buffer_size);\n+        }",
        "comment_created_at": "2025-01-27T07:51:19+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "If I understood correctly, The m_read_buffer is resized only once here ant it's size is always 16k. The `m_read_buffer` is used in ::read() only. M.b. it's better to make it local variable there. If you need the buffer shared between readHeader and readData then it makes sense to initialize the buffer in decoder constructor.",
        "pr_file_module": null
      },
      {
        "comment_id": "1930290856",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26844,
        "pr_file": "modules/imgcodecs/src/grfmt_jpegxl.cpp",
        "discussion_id": "1930098040",
        "commented_code": "@@ -91,11 +93,19 @@ ImageDecoder JpegXLDecoder::newDecoder() const\n \n bool JpegXLDecoder::readHeader()\n {\n-    // Open file\n-    if (!m_f) {\n-        m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n-        if (!m_f)\n-            return false;\n+    if (m_buf.empty()) {\n+        // Open file\n+        if (!m_f) {\n+            m_f.reset(fopen(m_filename.c_str(), \"rb\"));\n+            if (!m_f) {\n+                return false;\n+            }\n+        }\n+        // Create buffer for reading file\n+        constexpr size_t read_buffer_size = 16384;  // 16KB chunks\n+        if (m_read_buffer.capacity() < read_buffer_size) {\n+            m_read_buffer.resize(read_buffer_size);\n+        }",
        "comment_created_at": "2025-01-27T10:22:45+00:00",
        "comment_author": "Kumataro",
        "comment_body": "Thank you for your comment, `m_read_buffer` should be kept accrossing 'readHeader()' and 'readData()'. So I will move it to constructor.\r\n\r\n```\r\nJXLDecoder::JxlDecoder()\r\n  m_decoder = nullptr;\r\n\r\nJXLDecoder::readHeader()\r\n  m_decoder = JxlDecoderMake(nullptr);\r\n\r\n  read()\r\n    JxlDecoderReleaseInput() // no effects because no input buffer is set\r\n    JxlDecoderSetInput() ---- Input Buffer is locked.\r\n                               |\r\nJXLDecoder::readData()         |\r\n  read()                       |\r\n    JxlDecoderReleaseInput()- Input Buffer is unlocked.\r\n    JxlDecoderSetInput() ---- Input Buffer is locked.\r\n                               |\r\nJXLDecoder::~JxlDecoder()      |\r\n  close()                      |\r\n    m_decoder.reset() ------- Input buffer is unlocked\r\n  destory m_decoder\r\n```\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1890435483",
    "pr_number": 26619,
    "pr_file": "3rdparty/fastcv/src/fastcv_hal_imgproc.cpp",
    "created_at": "2024-12-18T15:31:56+00:00",
    "commented_code": "CV_HAL_RETURN_NOT_IMPLEMENTED(cv::format(\"Src type:%s is not supported\", cv::typeToString(src_type).c_str()));\n\n    CV_HAL_RETURN(status, hal_warpPerspective);\n}\n\nclass FcvPyrLoop_Invoker : public cv::ParallelLoopBody\n{\npublic:\n\n    FcvPyrLoop_Invoker(cv::Mat src_, int width_, int height_, cv::Mat dst_, int bdr_, int knl_, int stripeHeight_, int nStripes_) :\n        cv::ParallelLoopBody(), src(src_), width(width_), height(height_), dst(dst_), bdr(bdr_), knl(knl_), stripeHeight(stripeHeight_), nStripes(nStripes_)\n    {\n    }\n\n    virtual void operator()(const cv::Range& range) const CV_OVERRIDE\n    {\n        int height_ = stripeHeight * (range.end - range.start);\n        int width_  = width;\n        cv::Mat src_;\n        int n = knl/2;\n\n        if(range.end == nStripes)\n            height_ += (height - range.end * stripeHeight);\n\n        src_ = cv::Mat(height_ + 2*n, width_ + 2*n, CV_8U);\n\n        if(range.start == 0 && range.end == nStripes)\n            cv::copyMakeBorder(src(cv::Rect(0, 0, width, height)), src_, n, n, n, n, bdr);\n        else if(range.start == 0)\n            cv::copyMakeBorder(src(cv::Rect(0, 0, width_, height_ + n)), src_, n, 0, n, n, bdr);\n        else if(range.end == nStripes)\n            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + n)), src_, 0, n, n, n, bdr);\n        else\n            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + 2*n)), src_, 0, 0, n, n, bdr);\n\n        int dstHeight_, dstWidth_, origDstHeight_, origDstWidth_;\n        dstHeight_ = (height_ + 2*n + 1)/2;\n        dstWidth_ = (width_ + 2*n + 1)/2;\n        origDstHeight_ = (height_ + 1)/2;\n        origDstWidth_ = (width_ + 1)/2;\n\n        cv::Mat dst_padded = cv::Mat(dstHeight_, dstWidth_, CV_8U);\n\n        fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1890435483",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26619,
        "pr_file": "3rdparty/fastcv/src/fastcv_hal_imgproc.cpp",
        "discussion_id": "1890435483",
        "commented_code": "@@ -743,4 +743,253 @@ int fastcv_hal_warpPerspective(\n         CV_HAL_RETURN_NOT_IMPLEMENTED(cv::format(\"Src type:%s is not supported\", cv::typeToString(src_type).c_str()));\n \n     CV_HAL_RETURN(status, hal_warpPerspective);\n+}\n+\n+class FcvPyrLoop_Invoker : public cv::ParallelLoopBody\n+{\n+public:\n+\n+    FcvPyrLoop_Invoker(cv::Mat src_, int width_, int height_, cv::Mat dst_, int bdr_, int knl_, int stripeHeight_, int nStripes_) :\n+        cv::ParallelLoopBody(), src(src_), width(width_), height(height_), dst(dst_), bdr(bdr_), knl(knl_), stripeHeight(stripeHeight_), nStripes(nStripes_)\n+    {\n+    }\n+\n+    virtual void operator()(const cv::Range& range) const CV_OVERRIDE\n+    {\n+        int height_ = stripeHeight * (range.end - range.start);\n+        int width_  = width;\n+        cv::Mat src_;\n+        int n = knl/2;\n+\n+        if(range.end == nStripes)\n+            height_ += (height - range.end * stripeHeight);\n+\n+        src_ = cv::Mat(height_ + 2*n, width_ + 2*n, CV_8U);\n+\n+        if(range.start == 0 && range.end == nStripes)\n+            cv::copyMakeBorder(src(cv::Rect(0, 0, width, height)), src_, n, n, n, n, bdr);\n+        else if(range.start == 0)\n+            cv::copyMakeBorder(src(cv::Rect(0, 0, width_, height_ + n)), src_, n, 0, n, n, bdr);\n+        else if(range.end == nStripes)\n+            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + n)), src_, 0, n, n, n, bdr);\n+        else\n+            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + 2*n)), src_, 0, 0, n, n, bdr);\n+\n+        int dstHeight_, dstWidth_, origDstHeight_, origDstWidth_;\n+        dstHeight_ = (height_ + 2*n + 1)/2;\n+        dstWidth_ = (width_ + 2*n + 1)/2;\n+        origDstHeight_ = (height_ + 1)/2;\n+        origDstWidth_ = (width_ + 1)/2;\n+\n+        cv::Mat dst_padded = cv::Mat(dstHeight_, dstWidth_, CV_8U);\n+\n+        fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];",
        "comment_created_at": "2024-12-18T15:31:56+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I propose to use local variable on stack. new is redundant here. Also it's not deleted afterwards.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1890437308",
    "pr_number": 26619,
    "pr_file": "3rdparty/fastcv/src/fastcv_hal_imgproc.cpp",
    "created_at": "2024-12-18T15:33:11+00:00",
    "commented_code": "CV_HAL_RETURN_NOT_IMPLEMENTED(cv::format(\"Src type:%s is not supported\", cv::typeToString(src_type).c_str()));\n\n    CV_HAL_RETURN(status, hal_warpPerspective);\n}\n\nclass FcvPyrLoop_Invoker : public cv::ParallelLoopBody\n{\npublic:\n\n    FcvPyrLoop_Invoker(cv::Mat src_, int width_, int height_, cv::Mat dst_, int bdr_, int knl_, int stripeHeight_, int nStripes_) :\n        cv::ParallelLoopBody(), src(src_), width(width_), height(height_), dst(dst_), bdr(bdr_), knl(knl_), stripeHeight(stripeHeight_), nStripes(nStripes_)\n    {\n    }\n\n    virtual void operator()(const cv::Range& range) const CV_OVERRIDE\n    {\n        int height_ = stripeHeight * (range.end - range.start);\n        int width_  = width;\n        cv::Mat src_;\n        int n = knl/2;\n\n        if(range.end == nStripes)\n            height_ += (height - range.end * stripeHeight);\n\n        src_ = cv::Mat(height_ + 2*n, width_ + 2*n, CV_8U);\n\n        if(range.start == 0 && range.end == nStripes)\n            cv::copyMakeBorder(src(cv::Rect(0, 0, width, height)), src_, n, n, n, n, bdr);\n        else if(range.start == 0)\n            cv::copyMakeBorder(src(cv::Rect(0, 0, width_, height_ + n)), src_, n, 0, n, n, bdr);\n        else if(range.end == nStripes)\n            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + n)), src_, 0, n, n, n, bdr);\n        else\n            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + 2*n)), src_, 0, 0, n, n, bdr);\n\n        int dstHeight_, dstWidth_, origDstHeight_, origDstWidth_;\n        dstHeight_ = (height_ + 2*n + 1)/2;\n        dstWidth_ = (width_ + 2*n + 1)/2;\n        origDstHeight_ = (height_ + 1)/2;\n        origDstWidth_ = (width_ + 1)/2;\n\n        cv::Mat dst_padded = cv::Mat(dstHeight_, dstWidth_, CV_8U);\n\n        fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];\n        framePyr[0].ptr = NULL;\n        framePyr[1].ptr = dst_padded.data;\n        framePyr[1].stride = dstWidth_;\n\n        fcvPyramidCreateu8_v4(src_.data, width_ + 2*n, height_ + 2*n,\n                                 width_ + 2*n, 2, FASTCV_PYRAMID_SCALE_HALF,\n                                 framePyr, FASTCV_BORDER_UNDEFINED, 0);\n\n        int start_val = stripeHeight * range.start;\n        cv::Mat dst_temp1 = dst_padded(cv::Rect(n/2, n/2, origDstWidth_, origDstHeight_));\n        cv::Mat dst_temp2 = dst(cv::Rect(0, start_val/2, origDstWidth_, origDstHeight_));\n        dst_temp1.copyTo(dst_temp2);\n    }\n\nprivate:\n    cv::Mat src;\n    const int width;\n    const int height;\n    cv::Mat dst;\n    const int bdr;\n    const int knl;\n    const int stripeHeight;\n    const int nStripes;\n\n    FcvPyrLoop_Invoker(const FcvPyrLoop_Invoker &);  // = delete;\n    const FcvPyrLoop_Invoker& operator= (const FcvPyrLoop_Invoker &);  // = delete;\n};\n\nint fastcv_hal_pyrdown(\n    const uchar*     src_data,\n    size_t           src_step,\n    int              src_width,\n    int              src_height,\n    uchar*           dst_data,\n    size_t           dst_step,\n    int              dst_width,\n    int              dst_height,\n    int              depth,\n    int              cn,\n    int              border_type)\n{\n    if(depth != CV_8U || cn!= 1)\n    {\n        CV_HAL_RETURN_NOT_IMPLEMENTED(\"src type not supported\");\n    }\n\n    int dstW = (src_width & 1)  == 1 ? ((src_width + 1)  >> 1) : ((src_width) >> 1);\n    int dstH = (src_height & 1) == 1 ? ((src_height + 1) >> 1) : ((src_height) >> 1);\n\n    if((dstW > dst_width) || (dstH > dst_height))\n    {\n        CV_HAL_RETURN_NOT_IMPLEMENTED(\"dst size needs to be atleast half of the src size\");\n    }\n\n    INITIALIZATION_CHECK;\n\n    fcvBorderType bdr;\n    uint8_t bVal = 0;\n    int nThreads = cv::getNumThreads();\n    if(nThreads <= 1)\n    {\n        switch(border_type)\n        {\n            case cv::BORDER_REPLICATE:\n                bdr = FASTCV_BORDER_REPLICATE;\n                break;\n            case cv::BORDER_REFLECT:\n                bdr = FASTCV_BORDER_REFLECT;\n                break;\n            case cv::BORDER_REFLECT101:    // cv::BORDER_REFLECT_101, BORDER_DEFAULT\n                bdr = FASTCV_BORDER_REFLECT_V2;\n                break;\n            default:\n                CV_HAL_RETURN_NOT_IMPLEMENTED(\"border type not supported\");\n        }\n\n        fcvPyramidLevel_v2 *frame1Pyr = new fcvPyramidLevel_v2[2];\n        frame1Pyr[0].ptr = NULL;\n        frame1Pyr[1].ptr = dst_data;\n        frame1Pyr[1].stride = dst_step;",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1890437308",
        "repo_full_name": "opencv/opencv",
        "pr_number": 26619,
        "pr_file": "3rdparty/fastcv/src/fastcv_hal_imgproc.cpp",
        "discussion_id": "1890437308",
        "commented_code": "@@ -743,4 +743,253 @@ int fastcv_hal_warpPerspective(\n         CV_HAL_RETURN_NOT_IMPLEMENTED(cv::format(\"Src type:%s is not supported\", cv::typeToString(src_type).c_str()));\n \n     CV_HAL_RETURN(status, hal_warpPerspective);\n+}\n+\n+class FcvPyrLoop_Invoker : public cv::ParallelLoopBody\n+{\n+public:\n+\n+    FcvPyrLoop_Invoker(cv::Mat src_, int width_, int height_, cv::Mat dst_, int bdr_, int knl_, int stripeHeight_, int nStripes_) :\n+        cv::ParallelLoopBody(), src(src_), width(width_), height(height_), dst(dst_), bdr(bdr_), knl(knl_), stripeHeight(stripeHeight_), nStripes(nStripes_)\n+    {\n+    }\n+\n+    virtual void operator()(const cv::Range& range) const CV_OVERRIDE\n+    {\n+        int height_ = stripeHeight * (range.end - range.start);\n+        int width_  = width;\n+        cv::Mat src_;\n+        int n = knl/2;\n+\n+        if(range.end == nStripes)\n+            height_ += (height - range.end * stripeHeight);\n+\n+        src_ = cv::Mat(height_ + 2*n, width_ + 2*n, CV_8U);\n+\n+        if(range.start == 0 && range.end == nStripes)\n+            cv::copyMakeBorder(src(cv::Rect(0, 0, width, height)), src_, n, n, n, n, bdr);\n+        else if(range.start == 0)\n+            cv::copyMakeBorder(src(cv::Rect(0, 0, width_, height_ + n)), src_, n, 0, n, n, bdr);\n+        else if(range.end == nStripes)\n+            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + n)), src_, 0, n, n, n, bdr);\n+        else\n+            cv::copyMakeBorder(src(cv::Rect(0, range.start * stripeHeight - n, width_, height_ + 2*n)), src_, 0, 0, n, n, bdr);\n+\n+        int dstHeight_, dstWidth_, origDstHeight_, origDstWidth_;\n+        dstHeight_ = (height_ + 2*n + 1)/2;\n+        dstWidth_ = (width_ + 2*n + 1)/2;\n+        origDstHeight_ = (height_ + 1)/2;\n+        origDstWidth_ = (width_ + 1)/2;\n+\n+        cv::Mat dst_padded = cv::Mat(dstHeight_, dstWidth_, CV_8U);\n+\n+        fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];\n+        framePyr[0].ptr = NULL;\n+        framePyr[1].ptr = dst_padded.data;\n+        framePyr[1].stride = dstWidth_;\n+\n+        fcvPyramidCreateu8_v4(src_.data, width_ + 2*n, height_ + 2*n,\n+                                 width_ + 2*n, 2, FASTCV_PYRAMID_SCALE_HALF,\n+                                 framePyr, FASTCV_BORDER_UNDEFINED, 0);\n+\n+        int start_val = stripeHeight * range.start;\n+        cv::Mat dst_temp1 = dst_padded(cv::Rect(n/2, n/2, origDstWidth_, origDstHeight_));\n+        cv::Mat dst_temp2 = dst(cv::Rect(0, start_val/2, origDstWidth_, origDstHeight_));\n+        dst_temp1.copyTo(dst_temp2);\n+    }\n+\n+private:\n+    cv::Mat src;\n+    const int width;\n+    const int height;\n+    cv::Mat dst;\n+    const int bdr;\n+    const int knl;\n+    const int stripeHeight;\n+    const int nStripes;\n+\n+    FcvPyrLoop_Invoker(const FcvPyrLoop_Invoker &);  // = delete;\n+    const FcvPyrLoop_Invoker& operator= (const FcvPyrLoop_Invoker &);  // = delete;\n+};\n+\n+int fastcv_hal_pyrdown(\n+    const uchar*     src_data,\n+    size_t           src_step,\n+    int              src_width,\n+    int              src_height,\n+    uchar*           dst_data,\n+    size_t           dst_step,\n+    int              dst_width,\n+    int              dst_height,\n+    int              depth,\n+    int              cn,\n+    int              border_type)\n+{\n+    if(depth != CV_8U || cn!= 1)\n+    {\n+        CV_HAL_RETURN_NOT_IMPLEMENTED(\"src type not supported\");\n+    }\n+\n+    int dstW = (src_width & 1)  == 1 ? ((src_width + 1)  >> 1) : ((src_width) >> 1);\n+    int dstH = (src_height & 1) == 1 ? ((src_height + 1) >> 1) : ((src_height) >> 1);\n+\n+    if((dstW > dst_width) || (dstH > dst_height))\n+    {\n+        CV_HAL_RETURN_NOT_IMPLEMENTED(\"dst size needs to be atleast half of the src size\");\n+    }\n+\n+    INITIALIZATION_CHECK;\n+\n+    fcvBorderType bdr;\n+    uint8_t bVal = 0;\n+    int nThreads = cv::getNumThreads();\n+    if(nThreads <= 1)\n+    {\n+        switch(border_type)\n+        {\n+            case cv::BORDER_REPLICATE:\n+                bdr = FASTCV_BORDER_REPLICATE;\n+                break;\n+            case cv::BORDER_REFLECT:\n+                bdr = FASTCV_BORDER_REFLECT;\n+                break;\n+            case cv::BORDER_REFLECT101:    // cv::BORDER_REFLECT_101, BORDER_DEFAULT\n+                bdr = FASTCV_BORDER_REFLECT_V2;\n+                break;\n+            default:\n+                CV_HAL_RETURN_NOT_IMPLEMENTED(\"border type not supported\");\n+        }\n+\n+        fcvPyramidLevel_v2 *frame1Pyr = new fcvPyramidLevel_v2[2];\n+        frame1Pyr[0].ptr = NULL;\n+        frame1Pyr[1].ptr = dst_data;\n+        frame1Pyr[1].stride = dst_step;",
        "comment_created_at": "2024-12-18T15:33:11+00:00",
        "comment_author": "asmorkalov",
        "comment_body": "I propose to use local variable on stack. new is redundant here. Also it's not deleted afterwards.",
        "pr_file_module": null
      }
    ]
  }
]
