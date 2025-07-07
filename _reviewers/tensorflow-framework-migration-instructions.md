---
title: Framework migration instructions
description: 'When documenting AI framework migrations (like TensorFlow/Keras version
  changes), provide complete instructions covering both installation and code modifications.
  Include:'
repository: tensorflow/tensorflow
label: AI
language: Markdown
comments_count: 2
repository_stars: 190625
---

When documenting AI framework migrations (like TensorFlow/Keras version changes), provide complete instructions covering both installation and code modifications. Include:

1. Specific package installation commands with version constraints
2. Required import statement changes with before/after examples
3. Environment variable configurations if applicable
4. Edge cases and compatibility considerations

Example for Keras 2 to 3 migration:
```python
# Installation
# pip install tf-keras~=2.16

# Import changes - Before:
import tensorflow.keras as keras
# or
import keras

# Import changes - After:
import tf_keras as keras

# OR to continue using Keras 2
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
# then use original imports
```

This practice ensures AI developers can smoothly transition between framework versions without disrupting their workflows or introducing subtle bugs.