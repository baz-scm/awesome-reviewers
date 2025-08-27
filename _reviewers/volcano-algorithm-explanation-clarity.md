---
title: Algorithm explanation clarity
description: When documenting algorithms, provide detailed explanations of the underlying
  logic with concrete examples and clear process flows. Abstract algorithmic descriptions
  should be accompanied by specific scenarios that illustrate how the algorithm behaves
  in practice.
repository: volcano-sh/volcano
label: Algorithms
language: Markdown
comments_count: 6
repository_stars: 4899
---

When documenting algorithms, provide detailed explanations of the underlying logic with concrete examples and clear process flows. Abstract algorithmic descriptions should be accompanied by specific scenarios that illustrate how the algorithm behaves in practice.

Key requirements:
1. **Explain the "why"** - Don't just describe what the algorithm does, but explain why it works and what problems it solves
2. **Provide concrete scenarios** - Use specific examples like "PyTorch job: master pod using CPU should disperse to avoid hot node while worker pods using GPU should aggregate to reduce resource fragment"
3. **Document process flows** - Arrange explanations according to the logical flow of the algorithm, potentially with diagrams
4. **Include implementation details** - Cover callback functions, data structures, and key algorithmic steps

Example of good algorithm documentation:
```
## Resource Allocation Algorithm

### Problem
Different resource types require different allocation strategies to optimize cluster utilization.

### Solution
The ResourceStrategyFit algorithm applies different strategies per resource type:

1. **CPU resources**: Use LeastRequestedPriority to disperse tasks and avoid hotspots
2. **GPU resources**: Use MostRequestedPriority to aggregate tasks and reduce fragmentation

### Process Flow
1. Identify resource types in the pod specification
2. For each resource type, apply the configured strategy:
   - If CPU: Calculate dispersion score = (capacity - allocated) / capacity
   - If GPU: Calculate aggregation score = allocated / capacity
3. Combine scores using weighted priorities
```

This approach ensures that algorithmic concepts are accessible to both implementers and reviewers, reducing confusion and enabling better code quality.