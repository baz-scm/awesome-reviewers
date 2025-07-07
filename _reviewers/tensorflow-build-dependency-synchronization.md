---
title: Build dependency synchronization
description: 'When adding new imports to code files, always synchronize by updating
  the corresponding dependencies in BUILD files. Different build environments enforce
  dependency rules with varying strictness, so proper configuration is essential even
  if local builds succeed. This helps prevent errors like:'
repository: tensorflow/tensorflow
label: Configurations
language: Python
comments_count: 2
repository_stars: 190625
---

When adding new imports to code files, always synchronize by updating the corresponding dependencies in BUILD files. Different build environments enforce dependency rules with varying strictness, so proper configuration is essential even if local builds succeed. This helps prevent errors like:

```
ERROR: Strict deps violations: //tensorflow/python/client:device_lib
  In tensorflow/python/client/device_lib.py, no direct deps found for imports:
    line 21: from tensorflow.python.platform import tf_logging as logging: Module "tensorflow.python.platform" not provided by a direct dep
```

When adding a new import like `from tensorflow.python.platform import tf_logging as logging`, ensure you also update the appropriate BUILD file to include this dependency, even if your local environment doesn't immediately flag the missing dependency.