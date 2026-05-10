---
title: Stable Interface Contracts
description: When designing or extending APIs, treat existing “core” interface contracts
  as stable and enforce exact compatibility (method signature + parameter semantics
  + return shapes) across base classes and all implementations. If you need different
  inputs/behavior for a subset of modules, add an adapter/compatibility layer in the
  business layer instead of changing...
repository: eosphoros-ai/DB-GPT
label: API
language: Python
comments_count: 6
repository_stars: 18703
---

When designing or extending APIs, treat existing “core” interface contracts as stable and enforce exact compatibility (method signature + parameter semantics + return shapes) across base classes and all implementations. If you need different inputs/behavior for a subset of modules, add an adapter/compatibility layer in the business layer instead of changing the core interface.

Practical rules:
- Don’t change core interface signatures unless you can update every caller/implementation; prefer compatibility logic in higher-level/business code.
- Ensure subclass methods match the base class contract exactly (number/order/names of parameters and tuple return formats). Positional-argument mismatches should be prevented by consistent signatures.
- Prefer defining base methods with broad but explicit typing (e.g., `retrieve(self, input: Any) -> Tuple[Graph, Any]`) so implementations can accept different input forms while still conforming to the contract.

Example: adapter-based compatibility (don’t modify core)
```python
# Core interface (unchanged)
class ChatPromptTemplate:
    def generate_input_values(self, *, question: str, **kwargs):
        ...

# Business-layer adapter
class ChatDashboardPromptTemplate(ChatPromptTemplate):
    def generate_input_values(self, *, input: str, **kwargs):
        # map new variable name to old core contract
        return super().generate_input_values(question=input, **kwargs)
```

Example: contract-consistent retriever base
```python
from typing import Any, Tuple

class GraphRetrieverBase:
    async def retrieve(self, input: Any) -> Tuple["Graph", Any]:
        raise NotImplementedError

# Implementation conforms to the base signature
class DocumentGraphRetriever(GraphRetrieverBase):
    async def retrieve(self, input):
        # input can be Union[Graph, List[str], List[List[float]]] in practice
        graph = ...
        extra = None
        return graph, extra
```

This prevents runtime failures like “takes N positional arguments but M were given” and avoids breaking unrelated modules that depend on the core contract.