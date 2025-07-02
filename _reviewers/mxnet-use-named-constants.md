---
title: Use named constants
description: In AI model implementations, avoid using magic numbers directly in code
  as they reduce readability and make maintenance difficult. Always define constants
  with meaningful names, especially for values related to tensor dimensions, indices,
  and type identifiers.
repository: apache/mxnet
label: AI
language: Other
comments_count: 2
repository_stars: 20801
---

In AI model implementations, avoid using magic numbers directly in code as they reduce readability and make maintenance difficult. Always define constants with meaningful names, especially for values related to tensor dimensions, indices, and type identifiers.

For dimension limits:
```cpp
// Instead of this:
if (shape.ndim() >= 1 && shape.ndim() <= 12) {
  // Process shape
}

// Use this:
const int MAX_ONEDNN_DIMS = 12;
if (shape.ndim() >= 1 && shape.ndim() <= MAX_ONEDNN_DIMS) {
  // Process shape
}
```

For array indices representing specific tensor components:
```cpp
// Instead of this:
if (n->inputs[2].node->is_variable()) {
  // Process bias
}

// Use this:
const int BIAS_INDEX = 2;  // Or better, use enum or named constant
if (n->inputs[BIAS_INDEX].node->is_variable()) {
  // Process bias
}
```

This practice makes code more maintainable as dimensions and tensor layouts evolve during AI model optimization efforts.


[
  {
    "discussion_id": "823738415",
    "pr_number": 20913,
    "pr_file": "src/ndarray/ndarray.cc",
    "created_at": "2022-03-10T13:51:24+00:00",
    "commented_code": "dnnl::memory::dims dims;\n  // These are shapes supprted by DNNL.\n  if (shape.ndim() >= 1 && shape.ndim() <= 6) {\n  if (shape.ndim() >= 1 && shape.ndim() <= 12) {",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "823738415",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20913,
        "pr_file": "src/ndarray/ndarray.cc",
        "discussion_id": "823738415",
        "commented_code": "@@ -605,36 +605,14 @@ void NDArray::Chunk::SetMKLMem(const mxnet::TShape& shape, int dtype) {\n \n   dnnl::memory::dims dims;\n   // These are shapes supprted by DNNL.\n-  if (shape.ndim() >= 1 && shape.ndim() <= 6) {\n+  if (shape.ndim() >= 1 && shape.ndim() <= 12) {",
        "comment_created_at": "2022-03-10T13:51:24+00:00",
        "comment_author": "bgawrych",
        "comment_body": "Can '12'  be named by const variable? e.g. \"const int MAX_ONEDNN_DIMS\"",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "669908725",
    "pr_number": 20430,
    "pr_file": "src/operator/quantization/quantize_graph_pass.h",
    "created_at": "2021-07-14T19:53:34+00:00",
    "commented_code": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\n\n/*!\n *  Copyright (c) 2021 by Contributors\n * \\file quantize_graph_pass.h\n * \\brief\n */\n#ifndef MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n#define MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n\n#include <mxnet/op_attr_types.h>\n#include <nnvm/graph.h>\n#include <nnvm/pass.h>\n#include <queue>\n#include <unordered_map>\n#include <unordered_set>\n#include <vector>\n#include <string>\n#include \"quantize_v2-inl.h\"\n#include \"../nn/mkldnn/mkldnn_fully_connected-inl.h\"\n#include \"../../common/utils.h\"\n\nnamespace mxnet {\nnamespace op {\n\nusing nnvm::Symbol;\nusing nnvm::Node;\nusing nnvm::ObjectPtr;\nusing nnvm::NodeEntry;\nusing nnvm::Graph;\n\ninline ObjectPtr CreateNode(std::string op_name, std::string node_name) {\n  ObjectPtr node = Node::Create();\n  node->attrs.name = node_name;\n  if (op_name == \"nullptr\") {\n    node->attrs.op = nullptr;\n    // ugly workaround because VariableParam is not exposed\n    node->attrs.parsed =\n      nnvm::Symbol::CreateVariable(node->attrs.name).outputs[0].node->attrs.parsed;\n  } else {\n    node->attrs.op = Op::Get(op_name);\n  }\n  return node;\n}\n\ntemplate <bool require_bias>\nstatic inline bool IsOneDNNFullyConnected(const ObjectPtr& n) {\n#if MXNET_USE_MKLDNN == 1\n  if (n->op() == Op::Get(\"_sg_mkldnn_fully_connected\")) {\n    auto const& param = nnvm::get<MKLDNNFCFullParam>(n->attrs.parsed);\n    if (!(param.mkldnn_param.channel_wise_quantize.has_value() &&\n          param.mkldnn_param.channel_wise_quantize.value())) {\n      return !require_bias || (param.default_param.no_bias == false &&\n                               n->inputs[2].node->is_variable());",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "669908725",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20430,
        "pr_file": "src/operator/quantization/quantize_graph_pass.h",
        "discussion_id": "669908725",
        "commented_code": "@@ -0,0 +1,155 @@\n+/*\n+ * Licensed to the Apache Software Foundation (ASF) under one\n+ * or more contributor license agreements.  See the NOTICE file\n+ * distributed with this work for additional information\n+ * regarding copyright ownership.  The ASF licenses this file\n+ * to you under the Apache License, Version 2.0 (the\n+ * \"License\"); you may not use this file except in compliance\n+ * with the License.  You may obtain a copy of the License at\n+ *\n+ *   http://www.apache.org/licenses/LICENSE-2.0\n+ *\n+ * Unless required by applicable law or agreed to in writing,\n+ * software distributed under the License is distributed on an\n+ * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+ * KIND, either express or implied.  See the License for the\n+ * specific language governing permissions and limitations\n+ * under the License.\n+ */\n+\n+/*!\n+ *  Copyright (c) 2021 by Contributors\n+ * \\file quantize_graph_pass.h\n+ * \\brief\n+ */\n+#ifndef MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n+#define MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n+\n+#include <mxnet/op_attr_types.h>\n+#include <nnvm/graph.h>\n+#include <nnvm/pass.h>\n+#include <queue>\n+#include <unordered_map>\n+#include <unordered_set>\n+#include <vector>\n+#include <string>\n+#include \"quantize_v2-inl.h\"\n+#include \"../nn/mkldnn/mkldnn_fully_connected-inl.h\"\n+#include \"../../common/utils.h\"\n+\n+namespace mxnet {\n+namespace op {\n+\n+using nnvm::Symbol;\n+using nnvm::Node;\n+using nnvm::ObjectPtr;\n+using nnvm::NodeEntry;\n+using nnvm::Graph;\n+\n+inline ObjectPtr CreateNode(std::string op_name, std::string node_name) {\n+  ObjectPtr node = Node::Create();\n+  node->attrs.name = node_name;\n+  if (op_name == \"nullptr\") {\n+    node->attrs.op = nullptr;\n+    // ugly workaround because VariableParam is not exposed\n+    node->attrs.parsed =\n+      nnvm::Symbol::CreateVariable(node->attrs.name).outputs[0].node->attrs.parsed;\n+  } else {\n+    node->attrs.op = Op::Get(op_name);\n+  }\n+  return node;\n+}\n+\n+template <bool require_bias>\n+static inline bool IsOneDNNFullyConnected(const ObjectPtr& n) {\n+#if MXNET_USE_MKLDNN == 1\n+  if (n->op() == Op::Get(\"_sg_mkldnn_fully_connected\")) {\n+    auto const& param = nnvm::get<MKLDNNFCFullParam>(n->attrs.parsed);\n+    if (!(param.mkldnn_param.channel_wise_quantize.has_value() &&\n+          param.mkldnn_param.channel_wise_quantize.value())) {\n+      return !require_bias || (param.default_param.no_bias == false &&\n+                               n->inputs[2].node->is_variable());",
        "comment_created_at": "2021-07-14T19:53:34+00:00",
        "comment_author": "anko-intel",
        "comment_body": "instead of \"2\" it could be idx.bias",
        "pr_file_module": null
      },
      {
        "comment_id": "670386574",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20430,
        "pr_file": "src/operator/quantization/quantize_graph_pass.h",
        "discussion_id": "669908725",
        "commented_code": "@@ -0,0 +1,155 @@\n+/*\n+ * Licensed to the Apache Software Foundation (ASF) under one\n+ * or more contributor license agreements.  See the NOTICE file\n+ * distributed with this work for additional information\n+ * regarding copyright ownership.  The ASF licenses this file\n+ * to you under the Apache License, Version 2.0 (the\n+ * \"License\"); you may not use this file except in compliance\n+ * with the License.  You may obtain a copy of the License at\n+ *\n+ *   http://www.apache.org/licenses/LICENSE-2.0\n+ *\n+ * Unless required by applicable law or agreed to in writing,\n+ * software distributed under the License is distributed on an\n+ * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+ * KIND, either express or implied.  See the License for the\n+ * specific language governing permissions and limitations\n+ * under the License.\n+ */\n+\n+/*!\n+ *  Copyright (c) 2021 by Contributors\n+ * \\file quantize_graph_pass.h\n+ * \\brief\n+ */\n+#ifndef MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n+#define MXNET_OPERATOR_QUANTIZATION_QUANTIZE_GRAPH_PASS_H_\n+\n+#include <mxnet/op_attr_types.h>\n+#include <nnvm/graph.h>\n+#include <nnvm/pass.h>\n+#include <queue>\n+#include <unordered_map>\n+#include <unordered_set>\n+#include <vector>\n+#include <string>\n+#include \"quantize_v2-inl.h\"\n+#include \"../nn/mkldnn/mkldnn_fully_connected-inl.h\"\n+#include \"../../common/utils.h\"\n+\n+namespace mxnet {\n+namespace op {\n+\n+using nnvm::Symbol;\n+using nnvm::Node;\n+using nnvm::ObjectPtr;\n+using nnvm::NodeEntry;\n+using nnvm::Graph;\n+\n+inline ObjectPtr CreateNode(std::string op_name, std::string node_name) {\n+  ObjectPtr node = Node::Create();\n+  node->attrs.name = node_name;\n+  if (op_name == \"nullptr\") {\n+    node->attrs.op = nullptr;\n+    // ugly workaround because VariableParam is not exposed\n+    node->attrs.parsed =\n+      nnvm::Symbol::CreateVariable(node->attrs.name).outputs[0].node->attrs.parsed;\n+  } else {\n+    node->attrs.op = Op::Get(op_name);\n+  }\n+  return node;\n+}\n+\n+template <bool require_bias>\n+static inline bool IsOneDNNFullyConnected(const ObjectPtr& n) {\n+#if MXNET_USE_MKLDNN == 1\n+  if (n->op() == Op::Get(\"_sg_mkldnn_fully_connected\")) {\n+    auto const& param = nnvm::get<MKLDNNFCFullParam>(n->attrs.parsed);\n+    if (!(param.mkldnn_param.channel_wise_quantize.has_value() &&\n+          param.mkldnn_param.channel_wise_quantize.value())) {\n+      return !require_bias || (param.default_param.no_bias == false &&\n+                               n->inputs[2].node->is_variable());",
        "comment_created_at": "2021-07-15T11:45:23+00:00",
        "comment_author": "sfraczek",
        "comment_body": "ok",
        "pr_file_module": null
      }
    ]
  }
]
