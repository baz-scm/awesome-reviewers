---
title: Process configurations consistently
description: 'Ensure that configuration data is processed consistently and correctly
  throughout the codebase. This includes:


  1. **Use proper serialization methods** for configuration dictionaries. Prefer `json.dumps()`
  over `str()` when converting dictionaries to strings:'
repository: vllm-project/vllm
label: Configurations
language: Python
comments_count: 6
repository_stars: 51730
---

Ensure that configuration data is processed consistently and correctly throughout the codebase. This includes:

1. **Use proper serialization methods** for configuration dictionaries. Prefer `json.dumps()` over `str()` when converting dictionaries to strings:

```python
# Wrong: Using str() produces invalid JSON
if isinstance(self.ep_config, dict):
    self.ep_config = EPConfig.from_cli(str(self.ep_config))

# Correct: Use json.dumps() for proper serialization
if isinstance(self.ep_config, dict):
    self.ep_config = EPConfig.from_cli(json.dumps(self.ep_config))
```

2. **Process configurations consistently in all code paths**. Don't skip processing steps conditionally unless absolutely necessary:

```python
# Wrong: Only calling adapt_config_dict in one branch
if max_position_embeddings is None:
    max_position_embeddings = _maybe_retrieve_max_pos_from_hf()
    config_dict["max_position_embeddings"] = max_position_embeddings
    config = adapt_config_dict(config_dict)

# Correct: Call processing function in all cases
if max_position_embeddings is None:
    max_position_embeddings = _maybe_retrieve_max_pos_from_hf()
    config_dict["max_position_embeddings"] = max_position_embeddings
config = adapt_config_dict(config_dict)
```

3. **Handle nested configurations recursively** when transforming configuration structures:

```python
# Process nested dictionaries recursively
def _recursive_remap(elem: Any) -> Any:
    if not isinstance(elem, dict):
        return elem
    
    new_dict = {}
    for key, value in elem.items():
        new_key = config_mapping.get(key, key)
        new_dict[new_key] = _recursive_remap(value)
    return new_dict
```

4. **Verify that default values are sensible** and documented correctly in docstrings, ensuring the implementation matches the documentation.

5. **Avoid changing default configurations** that can break backward compatibility. When defaults must change, document the change and provide a migration path.