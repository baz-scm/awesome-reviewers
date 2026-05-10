---
title: Configurable Search Parameters
description: All retrieval/exploration code (graph + vector/ANN) must be implemented
  as a staged algorithm with explicit, configurable search hyperparameters, and with
  correct graph element semantics.
repository: eosphoros-ai/DB-GPT
label: Algorithms
language: Python
comments_count: 3
repository_stars: 18703
---

All retrieval/exploration code (graph + vector/ANN) must be implemented as a staged algorithm with explicit, configurable search hyperparameters, and with correct graph element semantics.

Apply these rules:
1) Make ANN/graph search hyperparameters explicit
- Do not rely on silent defaults for critical knobs (e.g., top_k, ef_search).
- Put them behind config/env/arguments and log the effective values.
- Use the smallest fan-out necessary; review the relevance/structure impact when increasing top_k.

2) Limit at the right stage (two-step retrieval)
- First retrieve a constrained “one-hop”/local set (e.g., entity-nearby chunks) with the limit.
- Then expand to the required upstream structure (e.g., directory/path) after the limited set is chosen, preserving document integrity.

3) Ensure graph element types are unambiguous
- Do not infer edges via “not vertex”; explicitly enumerate valid edge types so traversal logic is correct.

Example pattern (staged retrieval + explicit params):
```python
def search_with_two_stage_explore(graph_store, keywords, *, top_k, ef_search, one_hop_limit):
    # Stage 1: constrained exploration (local units)
    subgraph = graph_store.explore(
        subs=keywords,
        limit=one_hop_limit,
        search_method="entity_search",
        # explicit ANN/graph knobs
        top_k=top_k,
        hnsw_ef_search=ef_search,
    )

    # Stage 2: deterministic expansion (structure completion)
    chunks = [v.name for v in subgraph.vertices()]
    full_structure = graph_store.explore(
        subs=chunks,
        limit=one_hop_limit,
        search_method="path_completion",
    )
    return full_structure
```

If implementing graph element classification used by traversal, ensure edge/vertex semantics are explicit:
```python
class GraphElemType(Enum):
    # ...
    def is_vertex(self):
        return self in {GraphElemType.DOCUMENT, GraphElemType.CHUNK, GraphElemType.ENTITY}
    def is_edge(self):
        return self in {GraphElemType.INCLUDE, GraphElemType.NEXT, ...}  # enumerate
```

Outcome: predictable performance, controllable quality/relevance, and correct traversal behavior for algorithms/search over graphs and vector indexes.