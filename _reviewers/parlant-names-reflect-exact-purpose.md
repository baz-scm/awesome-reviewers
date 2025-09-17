---
title: Names reflect exact purpose
description: Choose names that precisely reflect the component's purpose and behavior,
  avoiding ambiguous terms or shortcuts. Names should be self-documenting and consistent
  with related components.
repository: emcie-co/parlant
label: Naming Conventions
language: Python
comments_count: 5
repository_stars: 12205
---

Choose names that precisely reflect the component's purpose and behavior, avoiding ambiguous terms or shortcuts. Names should be self-documenting and consistent with related components.

Key guidelines:
1. Use exact technical terms (e.g., 'identity_loader' not 'noop_loader' for a function that returns its input)
2. Maintain semantic precision (e.g., 'metadata_collection' not 'meta_collection' since it stores data about data)
3. Ensure component names match their behavior (e.g., 'SchematicGenerator' not 'JSONGenerator' if JSON is just an implementation detail)
4. Use consistent terminology within related components

Example:
```python
# Incorrect - ambiguous or imprecise names
class JSONGenerator:
    def generate(self, data: dict) -> dict:
        pass

meta_collection = db.get_collection("meta")
def noop_loader(doc: dict) -> dict:
    return doc

# Correct - precise, semantic names
class SchematicGenerator:
    def generate(self, data: dict) -> dict:
        pass

metadata_collection = db.get_collection("metadata")
def identity_loader(doc: dict) -> dict:
    return doc
```