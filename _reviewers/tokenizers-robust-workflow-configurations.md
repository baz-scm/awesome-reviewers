---
title: Robust workflow configurations
description: 'Ensure CI/CD workflow configuration files follow best practices for
  maintainability and correctness:


  1. Use centralized dependency management approaches like setup tools extras instead
  of hardcoding dependencies in workflow files:'
repository: huggingface/tokenizers
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 9868
---

Ensure CI/CD workflow configuration files follow best practices for maintainability and correctness:

1. Use centralized dependency management approaches like setup tools extras instead of hardcoding dependencies in workflow files:
```python
# Better approach (in setup.py):
extras_require = {
    "dev": ["black==22.3", "click==8.0.4"]
}

# Then in workflow file:
pip install package[dev]

# Instead of:
pip install black==22.3 click==8.0.4
```

2. Always quote numerical values in YAML files to prevent parsing issues, especially for version numbers:
```yaml
# Correct:
python: ["3.7", "3.8", "3.9", "3.10"]

# Problematic:
python: [3.7, 3.8, 3.9, 3.10]  # 3.10 will be parsed as 3.1
```