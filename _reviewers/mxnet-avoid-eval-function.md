---
title: Avoid eval function
description: Never use the `eval()` function in Python code as it creates serious
  security vulnerabilities by executing arbitrary code at runtime. This can lead to
  code injection attacks when processing user inputs or data from untrusted sources.
repository: apache/mxnet
label: Security
language: Python
comments_count: 1
repository_stars: 20801
---

Never use the `eval()` function in Python code as it creates serious security vulnerabilities by executing arbitrary code at runtime. This can lead to code injection attacks when processing user inputs or data from untrusted sources.

Instead of using `eval()` to convert strings to booleans or other types, use explicit type conversion or conditional logic:

```python
# INSECURE - vulnerable to code injection:
def setting_ctx(use_gpu):
    if eval(use_gpu):
        # code that uses GPU
        
# SECURE - using explicit boolean conversion:
def setting_ctx(use_gpu):
    if isinstance(use_gpu, str):
        use_gpu = use_gpu.lower() in ('true', 'yes', '1', 'y')
    if use_gpu:
        # code that uses GPU
```

For other type conversions, use appropriate functions like `int()`, `float()`, or `json.loads()` to safely parse data without executing code.


[
  {
    "discussion_id": "250018330",
    "pr_number": 13735,
    "pr_file": "example/gluon/wavenet/trainer.py",
    "created_at": "2019-01-23T00:46:51+00:00",
    "commented_code": "# Licensed to the Apache Software Foundation (ASF) under one\n# or more contributor license agreements.  See the NOTICE file\n# distributed with this work for additional information\n# regarding copyright ownership.  The ASF licenses this file\n# to you under the Apache License, Version 2.0 (the\n# \"License\"); you may not use this file except in compliance\n# with the License.  You may obtain a copy of the License at\n#\n#   http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing,\n# software distributed under the License is distributed on an\n# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n# KIND, either express or implied.  See the License for the\n# specific language governing permissions and limitations\n# under the License.\n\"\"\"\nModule: WaveNet trainer modulep\n\"\"\"\nimport sys\nimport numpy as np\nimport mxnet as mx\nfrom mxnet import gluon, autograd, nd\nfrom tqdm import trange\n\nfrom models import WaveNet\nfrom utils import decode_mu_law\nfrom data_loader import load_wav, data_generation, data_generation_sample\n# pylint: disable=invalid-name, too-many-arguments, too-many-instance-attributes, no-member, no-self-use\n# set gpu count\ndef setting_ctx(use_gpu):\n    \"\"\"\n    Description : setting cpu/gpu\n    \"\"\"\n    if eval(use_gpu):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "250018330",
        "repo_full_name": "apache/mxnet",
        "pr_number": 13735,
        "pr_file": "example/gluon/wavenet/trainer.py",
        "discussion_id": "250018330",
        "commented_code": "@@ -0,0 +1,130 @@\n+# Licensed to the Apache Software Foundation (ASF) under one\n+# or more contributor license agreements.  See the NOTICE file\n+# distributed with this work for additional information\n+# regarding copyright ownership.  The ASF licenses this file\n+# to you under the Apache License, Version 2.0 (the\n+# \"License\"); you may not use this file except in compliance\n+# with the License.  You may obtain a copy of the License at\n+#\n+#   http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing,\n+# software distributed under the License is distributed on an\n+# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+# KIND, either express or implied.  See the License for the\n+# specific language governing permissions and limitations\n+# under the License.\n+\"\"\"\n+Module: WaveNet trainer modulep\n+\"\"\"\n+import sys\n+import numpy as np\n+import mxnet as mx\n+from mxnet import gluon, autograd, nd\n+from tqdm import trange\n+\n+from models import WaveNet\n+from utils import decode_mu_law\n+from data_loader import load_wav, data_generation, data_generation_sample\n+# pylint: disable=invalid-name, too-many-arguments, too-many-instance-attributes, no-member, no-self-use\n+# set gpu count\n+def setting_ctx(use_gpu):\n+    \"\"\"\n+    Description : setting cpu/gpu\n+    \"\"\"\n+    if eval(use_gpu):",
        "comment_created_at": "2019-01-23T00:46:51+00:00",
        "comment_author": "ThomasDelteil",
        "comment_body": "please do not use eval here",
        "pr_file_module": null
      },
      {
        "comment_id": "252286024",
        "repo_full_name": "apache/mxnet",
        "pr_number": 13735,
        "pr_file": "example/gluon/wavenet/trainer.py",
        "discussion_id": "250018330",
        "commented_code": "@@ -0,0 +1,130 @@\n+# Licensed to the Apache Software Foundation (ASF) under one\n+# or more contributor license agreements.  See the NOTICE file\n+# distributed with this work for additional information\n+# regarding copyright ownership.  The ASF licenses this file\n+# to you under the Apache License, Version 2.0 (the\n+# \"License\"); you may not use this file except in compliance\n+# with the License.  You may obtain a copy of the License at\n+#\n+#   http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing,\n+# software distributed under the License is distributed on an\n+# \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+# KIND, either express or implied.  See the License for the\n+# specific language governing permissions and limitations\n+# under the License.\n+\"\"\"\n+Module: WaveNet trainer modulep\n+\"\"\"\n+import sys\n+import numpy as np\n+import mxnet as mx\n+from mxnet import gluon, autograd, nd\n+from tqdm import trange\n+\n+from models import WaveNet\n+from utils import decode_mu_law\n+from data_loader import load_wav, data_generation, data_generation_sample\n+# pylint: disable=invalid-name, too-many-arguments, too-many-instance-attributes, no-member, no-self-use\n+# set gpu count\n+def setting_ctx(use_gpu):\n+    \"\"\"\n+    Description : setting cpu/gpu\n+    \"\"\"\n+    if eval(use_gpu):",
        "comment_created_at": "2019-01-30T14:46:27+00:00",
        "comment_author": "seujung",
        "comment_body": "delete eval and change the use_gpu mode",
        "pr_file_module": null
      }
    ]
  }
]
