---
title: extensible parameter design
description: Design API parameters to support future extension without breaking changes.
  Use string enums instead of boolean flags when the parameter might need additional
  values later, implement comprehensive parameter forwarding with **kwargs, and avoid
  overly specific parameter designs that limit future flexibility.
repository: Unstructured-IO/unstructured
label: API
language: Python
comments_count: 5
repository_stars: 12116
---

Design API parameters to support future extension without breaking changes. Use string enums instead of boolean flags when the parameter might need additional values later, implement comprehensive parameter forwarding with **kwargs, and avoid overly specific parameter designs that limit future flexibility.

Key patterns to follow:

1. **String enums over booleans**: Instead of `contains_ontology_schema: bool = False`, use `html_parser: str = "v1"` to allow future parser versions without new parameters.

2. **Comprehensive parameter forwarding**: Use `**kwargs` to forward all parameters to delegate functions rather than explicitly listing each one:
```python
# Preferred approach
elements = _partition_doc(filename, file=file, **kwargs)

# Avoid this maintenance-heavy pattern  
elements = _partition_doc(
    filename=filename,
    file=file,
    infer_table_structure=infer_table_structure,
    languages=languages,
    strategy=strategy,
    **kwargs,
)
```

3. **Flexible interface design**: Accept the most general form of input (e.g., always expect text rather than having separate file/text/stdin branches) to reduce conditional complexity.

This approach ensures APIs can evolve gracefully, reduces maintenance overhead when adding new parameters, and provides a consistent experience for API consumers. All partitioners automatically receive new parameters through kwargs without requiring explicit updates to forwarding logic.