---
title: Abstract traversal patterns
description: When implementing algorithms that operate on complex data structures
  (trees, graphs, dominator structures), abstract the traversal mechanism from the
  operation performed at each node. Use visitor patterns or callbacks to separate
  concerns, making algorithms more maintainable and reusable.
repository: dotnet/runtime
label: Algorithms
language: C++
comments_count: 5
repository_stars: 16578
---

When implementing algorithms that operate on complex data structures (trees, graphs, dominator structures), abstract the traversal mechanism from the operation performed at each node. Use visitor patterns or callbacks to separate concerns, making algorithms more maintainable and reusable.

For example, instead of directly traversing a data structure and performing operations:

```cpp
// Tightly coupled approach
void ScaleLoopBlocks(BasicBlock* begBlk, BasicBlock* endBlk)
{
    for (BasicBlock* const curBlk : BasicBlockRangeList(begBlk, endBlk))
    {
        // Direct operations on curBlk mixed with traversal logic
        if (curBlk->hasProfileWeight()) continue;
        if (curBlk->isRunRarely()) continue;
        if (!m_reachabilitySets->GetDfsTree()->Contains(curBlk)) continue;
        
        // More operations...
    }
}
```

Abstract the traversal pattern to separate it from node operations:

```cpp
// Decoupled approach
void ScaleLoopBlocks(FlowGraphNaturalLoop* loop)
{
    loop->VisitLoopBlocks([&](BasicBlock* curBlk) -> BasicBlockVisit {
        if (curBlk->hasProfileWeight()) return BasicBlockVisit::Continue;
        if (curBlk->isRunRarely()) return BasicBlockVisit::Continue;
        
        // Operations on curBlk without traversal concerns
        
        return BasicBlockVisit::Continue;
    });
}
```

This approach offers several benefits:
1. Traversal logic is centralized and maintained in one place
2. Algorithm implementations become clearer and more focused
3. Traversal strategies can be optimized independently
4. Testing becomes easier with separated concerns
5. Reuse becomes natural for similar algorithms on the same structures
