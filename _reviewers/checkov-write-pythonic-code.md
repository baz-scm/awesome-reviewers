---
title: Write pythonic code
description: 'Embrace Python''s idiomatic programming style to make your code more
  readable, concise, and maintainable. Follow these Pythonic patterns:


  1. **Use truthiness checks** instead of explicit length comparisons:'
repository: bridgecrewio/checkov
label: Code Style
language: Python
comments_count: 8
repository_stars: 7668
---

Embrace Python's idiomatic programming style to make your code more readable, concise, and maintainable. Follow these Pythonic patterns:

1. **Use truthiness checks** instead of explicit length comparisons:
   ```python
   # Instead of this:
   if len(mod['Key']):
   
   # Do this:
   if mod['Key']:
   ```

2. **Access dictionaries directly** without unnecessary calls:
   ```python
   # Instead of this:
   if 'source_arn' in conf.keys():
   
   # Do this:
   if 'source_arn' in conf:
   ```

3. **Use dictionary comprehensions** for building mappings:
   ```python
   # Instead of this:
   for vertex in self.tf_graph.vertices:
       if vertex.block_type == BlockType.RESOURCE:
           self._address_to_tf_vertex_map[vertex.attributes[TF_PLAN_RESOURCE_ADDRESS]] = vertex
   
   # Do this:
   self._address_to_tf_vertex_map = {
       vertex.attributes[TF_PLAN_RESOURCE_ADDRESS]: vertex
       for vertex in self.tf_graph.vertices
       if vertex.block_type == BlockType.RESOURCE
   }
   ```

4. **Use context managers** for resource handling:
   ```python
   # Instead of this:
   f = open(f"{sast_policies_dir}/{policy.get('id')}.yaml", "a")
   # ...operations with f...
   f.close()
   
   # Do this:
   with open(f"{sast_policies_dir}/{policy.get('id')}.yaml", "a") as f:
       # ...operations with f...
   ```

5. **Prefer built-in type annotations** over imported ones:
   ```python
   # Instead of this:
   from typing import Dict, List
   def function(param: Dict[str, List[int]]) -> None:
   
   # Do this:
   def function(param: dict[str, list[int]]) -> None:
   ```

6. **Use fail-fast patterns** to avoid deeply nested conditionals:
   ```python
   # Instead of this:
   if source_bc_id:
       ckv_id = self.get_ckv_id_from_bc_id(source_bc_id)
       if ckv_id:
           ckv_ids.append(ckv_id)
   
   # Do this:
   if not source_bc_id:
       continue
   ckv_id = self.get_ckv_id_from_bc_id(source_bc_id)
   if not ckv_id:
       continue
   ckv_ids.append(ckv_id)
   ```

7. **Use static methods appropriately** without unnecessary instantiation:
   ```python
   # Instead of this:
   k8s_validator = K8sValidator()
   if k8s_validator.is_valid_template(t):
   
   # Do this:
   if K8sValidator.is_valid_template(t):
   ```

These practices will result in cleaner, more maintainable code that follows Python's design philosophy of readability and simplicity.