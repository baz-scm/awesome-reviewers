---
title: Check before access
description: Always verify that objects, attributes, and variables are not None before
  accessing their properties, calling their methods, or using them in operations.
  This prevents common runtime errors like TypeError, AttributeError, or UnboundLocalError
  when working with optional values.
repository: vllm-project/vllm
label: Null Handling
language: Python
comments_count: 7
repository_stars: 51730
---

Always verify that objects, attributes, and variables are not None before accessing their properties, calling their methods, or using them in operations. This prevents common runtime errors like TypeError, AttributeError, or UnboundLocalError when working with optional values.

For optional attributes or dictionary keys:
```python
# Before - may raise AttributeError or TypeError if token_type_ids is None
token_type_embeddings = self.token_type_embeddings(token_type_ids)

# After - safely checks before access
if self.token_type_ids is not None:
    model_kwargs["token_type_ids"] = cast(torch.Tensor, self.token_type_ids)[:num_scheduled_tokens]
```

For conditional variables:
```python
# Before - may cause UnboundLocalError if condition is false
if is_v1_kv_transfer_group():
    invalid_block_ids = connector.get_block_ids_with_load_errors()
# Later code uses invalid_block_ids regardless of condition

# After - initialize before conditional assignment
invalid_block_ids: Optional[set[int]] = None
if is_v1_kv_transfer_group():
    invalid_block_ids = connector.get_block_ids_with_load_errors()
```

For optional containers:
```python
# Before - raises TypeError if finished_sending is None
for req_id in kv_connector_metadata.finished_sending:
    self._done_sending_count[req_id] += 1

# After - safely handles None case
for req_id in kv_connector_metadata.finished_sending or []:
    self._done_sending_count[req_id] += 1
```

Always match return values with declared types:
```python
# Before - implicitly returns None instead of declared tuple type
if not model_runner_output.kv_connector_metadata:
    return

# After - explicitly returns correct type
if not model_runner_output.kv_connector_metadata:
    return None, None
```