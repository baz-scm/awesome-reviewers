---
title: Optimize data structures
description: When implementing algorithms, prioritize data structure choices that
  minimize resource usage while maintaining functionality. Consider if a simpler approach
  with counters, efficient state tracking, or built-in functions can replace complex
  custom implementations.
repository: neondatabase/neon
label: Algorithms
language: C
comments_count: 3
repository_stars: 19015
---

When implementing algorithms, prioritize data structure choices that minimize resource usage while maintaining functionality. Consider if a simpler approach with counters, efficient state tracking, or built-in functions can replace complex custom implementations.

For hierarchical or nested data:
1. Track levels with counters instead of creating redundant objects
2. Store relationship information in fewer objects to reduce allocation costs
3. Use appropriate memory contexts for your allocation pattern

For example, instead of creating one structure per level like this:
```c
/* Creates one structure per level - O(n) space complexity */
while (SubtransDdlLevel != 0)
{
    DdlHashTable *new_table = MemoryContextAlloc(TopTransactionContext, sizeof(DdlHashTable));
    new_table->prev_table = CurrentDdlTable;
    CurrentDdlTable = new_table;
    SubtransDdlLevel -= 1;
}
```

Consider storing level information in the structure itself:
```c
/* Creates structures only when needed - O(1) space complexity for most cases */
if (need_new_table)
{
    DdlHashTable *new_table = MemoryContextAlloc(TopTransactionContext, sizeof(DdlHashTable));
    new_table->prev_table = CurrentDdlTable;
    new_table->subtrans_level = SubtransDdlLevel - 1;
    CurrentDdlTable = new_table;
}
```

Similarly, for string parsing operations, prefer standard library functions over custom implementations:
```c
/* More efficient and clearer than manual parsing */
int pos;
if (sscanf(safekeepers_list, "g#%u:%n", generation, &pos) == 1) { 
     return safekeepers_list + pos;
} else {
     return safekeepers_list;
}
```