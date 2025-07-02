---
title: Pre-compute reused data
description: When data will be accessed multiple times during processing, avoid redundant
  calculations by pre-computing values upfront rather than using lazy evaluation.
  This pattern significantly improves performance in iterative operations like machine
  learning training, inference, or repeated data transformations.
repository: apache/mxnet
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 20801
---

When data will be accessed multiple times during processing, avoid redundant calculations by pre-computing values upfront rather than using lazy evaluation. This pattern significantly improves performance in iterative operations like machine learning training, inference, or repeated data transformations.

For example, in data processing pipelines:

```python
# Performance optimization:
# Pre-compute transformations when data will be accessed repeatedly
transformer = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=rgb_mean, std=rgb_std)
])

# Use lazy=False to prepare data upfront when it will be used multiple times
data_loader = DataLoader(dataset.transform_first(transformer, lazy=False))
```

By preparing data once rather than on-demand, you reduce computational overhead and improve overall execution speed, especially in performance-critical sections of code.


[
  {
    "discussion_id": "954886448",
    "pr_number": 21127,
    "pr_file": "example/quantization_inc/resnet_measurment.py",
    "created_at": "2022-08-25T12:10:41+00:00",
    "commented_code": "# Licensed to the Apache Software Foundation (ASF) under one\n# or more contributor license agreements.  See the NOTICE file\n# distributed with this work for additional information\n# regarding copyright ownership.  The ASF licenses this file\n# to you under the Apache License, Version 2.0 (the\n# \"License\"); you may not use this file except in compliance\n# with the License.  You may obtain a copy of the License at\n#\n#   http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing,\n# software distributed under the License is distributed on an\n# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n# KIND, either express or implied.  See the License for the\n# specific language governing permissions and limitations\n# under the License.\n\nimport mxnet as mx\nfrom mxnet.gluon.data.vision import transforms\nimport time\nimport glob\n\n\ndef test_accuracy(net, data_loader, description):\n  count = 0\n  acc_top1 = mx.gluon.metric.Accuracy()\n  acc_top5 = mx.gluon.metric.TopKAccuracy(5)\n  start = time.time()\n  for x, label in data_loader:\n    output = net(x)\n    acc_top1.update(label, output)\n    acc_top5.update(label, output)\n    count += 1\n  time_spend = time.time() - start\n  _, top1 = acc_top1.get()\n  _, top5 = acc_top5.get()\n  print('{:21} Top1 Accuracy: {:.4f} Top5 Accuracy: {:.4f} from {:4} batches in {:8.2f}s'\n        .format(description, top1, top5, count, time_spend))\n\n# Preparing input data\nrgb_mean = (0.485, 0.456, 0.406)\nrgb_std = (0.229, 0.224, 0.225)\nbatch_size = 64\n\nstart = time.time()\n# Set below proper path to ImageNet data set\ndataset = mx.gluon.data.vision.ImageRecordDataset('../imagenet/rec/val.rec')\ntransformer = transforms.Compose([transforms.Resize(256),\n                                  transforms.CenterCrop(224),\n                                  transforms.ToTensor(),\n                                  transforms.Normalize(mean=rgb_mean, std=rgb_std)])\n# Note: As the input data are used many times it is better to prepared data once,\n#       so lazy parameter for transform_first is set to False",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "954886448",
        "repo_full_name": "apache/mxnet",
        "pr_number": 21127,
        "pr_file": "example/quantization_inc/resnet_measurment.py",
        "discussion_id": "954886448",
        "commented_code": "@@ -0,0 +1,68 @@\n+# Licensed to the Apache Software Foundation (ASF) under one\n+# or more contributor license agreements.  See the NOTICE file\n+# distributed with this work for additional information\n+# regarding copyright ownership.  The ASF licenses this file\n+# to you under the Apache License, Version 2.0 (the\n+# \"License\"); you may not use this file except in compliance\n+# with the License.  You may obtain a copy of the License at\n+#\n+#   http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing,\n+# software distributed under the License is distributed on an\n+# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+# KIND, either express or implied.  See the License for the\n+# specific language governing permissions and limitations\n+# under the License.\n+\n+import mxnet as mx\n+from mxnet.gluon.data.vision import transforms\n+import time\n+import glob\n+\n+\n+def test_accuracy(net, data_loader, description):\n+  count = 0\n+  acc_top1 = mx.gluon.metric.Accuracy()\n+  acc_top5 = mx.gluon.metric.TopKAccuracy(5)\n+  start = time.time()\n+  for x, label in data_loader:\n+    output = net(x)\n+    acc_top1.update(label, output)\n+    acc_top5.update(label, output)\n+    count += 1\n+  time_spend = time.time() - start\n+  _, top1 = acc_top1.get()\n+  _, top5 = acc_top5.get()\n+  print('{:21} Top1 Accuracy: {:.4f} Top5 Accuracy: {:.4f} from {:4} batches in {:8.2f}s'\n+        .format(description, top1, top5, count, time_spend))\n+\n+# Preparing input data\n+rgb_mean = (0.485, 0.456, 0.406)\n+rgb_std = (0.229, 0.224, 0.225)\n+batch_size = 64\n+\n+start = time.time()\n+# Set below proper path to ImageNet data set\n+dataset = mx.gluon.data.vision.ImageRecordDataset('../imagenet/rec/val.rec')\n+transformer = transforms.Compose([transforms.Resize(256),\n+                                  transforms.CenterCrop(224),\n+                                  transforms.ToTensor(),\n+                                  transforms.Normalize(mean=rgb_mean, std=rgb_std)])\n+# Note: As the input data are used many times it is better to prepared data once,\n+#       so lazy parameter for transform_first is set to False",
        "comment_created_at": "2022-08-25T12:10:41+00:00",
        "comment_author": "bartekkuncer",
        "comment_body": "```suggestion\r\n# Note: as the input data is used many times it is better to prepare it once.\r\n#       Therefore, lazy parameter for transform_first is set to False.\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "954888778",
    "pr_number": 21127,
    "pr_file": "example/quantization_inc/resnet_mse.py",
    "created_at": "2022-08-25T12:13:13+00:00",
    "commented_code": "# Licensed to the Apache Software Foundation (ASF) under one\n# or more contributor license agreements.  See the NOTICE file\n# distributed with this work for additional information\n# regarding copyright ownership.  The ASF licenses this file\n# to you under the Apache License, Version 2.0 (the\n# \"License\"); you may not use this file except in compliance\n# with the License.  You may obtain a copy of the License at\n#\n#   http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing,\n# software distributed under the License is distributed on an\n# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n# KIND, either express or implied.  See the License for the\n# specific language governing permissions and limitations\n# under the License.\n\nimport mxnet as mx\nfrom mxnet.gluon.model_zoo.vision import resnet50_v2\nfrom mxnet.gluon.data.vision import transforms\nfrom mxnet.contrib.quantization import quantize_net\n\n# Preparing input data\nrgb_mean = (0.485, 0.456, 0.406)\nrgb_std = (0.229, 0.224, 0.225)\nbatch_size = 64\nnum_calib_batches = 9\n# Set below proper path to ImageNet data set\ndataset = mx.gluon.data.vision.ImageRecordDataset('../imagenet/rec/val.rec')\n# Tuning in INC on whole data set takes too long time so we take only part of the whole data set\n# as representative part of it:\ndataset = dataset.take(num_calib_batches * batch_size)\ntransformer = transforms.Compose([transforms.Resize(256),\n                                  transforms.CenterCrop(224),\n                                  transforms.ToTensor(),\n                                  transforms.Normalize(mean=rgb_mean, std=rgb_std)])\n# Note: as input data are used many times during tuning it is better to prepared data earlier,\n#       so lazy parameter for transform_first is set to False",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "954888778",
        "repo_full_name": "apache/mxnet",
        "pr_number": 21127,
        "pr_file": "example/quantization_inc/resnet_mse.py",
        "discussion_id": "954888778",
        "commented_code": "@@ -0,0 +1,65 @@\n+# Licensed to the Apache Software Foundation (ASF) under one\n+# or more contributor license agreements.  See the NOTICE file\n+# distributed with this work for additional information\n+# regarding copyright ownership.  The ASF licenses this file\n+# to you under the Apache License, Version 2.0 (the\n+# \"License\"); you may not use this file except in compliance\n+# with the License.  You may obtain a copy of the License at\n+#\n+#   http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing,\n+# software distributed under the License is distributed on an\n+# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+# KIND, either express or implied.  See the License for the\n+# specific language governing permissions and limitations\n+# under the License.\n+\n+import mxnet as mx\n+from mxnet.gluon.model_zoo.vision import resnet50_v2\n+from mxnet.gluon.data.vision import transforms\n+from mxnet.contrib.quantization import quantize_net\n+\n+# Preparing input data\n+rgb_mean = (0.485, 0.456, 0.406)\n+rgb_std = (0.229, 0.224, 0.225)\n+batch_size = 64\n+num_calib_batches = 9\n+# Set below proper path to ImageNet data set\n+dataset = mx.gluon.data.vision.ImageRecordDataset('../imagenet/rec/val.rec')\n+# Tuning in INC on whole data set takes too long time so we take only part of the whole data set\n+# as representative part of it:\n+dataset = dataset.take(num_calib_batches * batch_size)\n+transformer = transforms.Compose([transforms.Resize(256),\n+                                  transforms.CenterCrop(224),\n+                                  transforms.ToTensor(),\n+                                  transforms.Normalize(mean=rgb_mean, std=rgb_std)])\n+# Note: as input data are used many times during tuning it is better to prepared data earlier,\n+#       so lazy parameter for transform_first is set to False",
        "comment_created_at": "2022-08-25T12:13:13+00:00",
        "comment_author": "bartekkuncer",
        "comment_body": "```suggestion\r\n# Note: as input data is used many times during tuning it is better to have it prepared earlier.\r\n#       Therefore, lazy parameter for transform_first is set to False.\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
