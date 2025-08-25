---
title: Configuration parameter documentation
description: Ensure all configuration parameters have explicit default values and
  are thoroughly documented. When using argparse with `action='store_true'`, always
  pair it with `default=False`. Document parameter purposes, valid values, and default
  behaviors in README files. For dependency management, separate conflicting requirements
  into different files to avoid...
repository: QwenLM/Qwen3
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 24226
---

Ensure all configuration parameters have explicit default values and are thoroughly documented. When using argparse with `action='store_true'`, always pair it with `default=False`. Document parameter purposes, valid values, and default behaviors in README files. For dependency management, separate conflicting requirements into different files to avoid version incompatibilities.

Example:
```python
# Good: Explicit default value
parser.add_argument('--use_modelscope', action='store_true', default=False, 
                   help='Whether to use ModelScope; if False, HuggingFace is used')
parser.add_argument('--generate_length', type=int, default=2048,
                   help='Number of tokens to generate (default: 2048)')
```

In README documentation:
```markdown
Parameters:
- `--use_modelscope`: Whether to use ModelScope; if False, HuggingFace is used; default is False
- `--generate_length`: Number of tokens to generate; default is 2048
```

For dependencies, use separate requirement files:
```
requirements/perf_transformer.txt  # For transformer-specific dependencies
requirements/perf_vllm.txt        # For vLLM-specific dependencies
```