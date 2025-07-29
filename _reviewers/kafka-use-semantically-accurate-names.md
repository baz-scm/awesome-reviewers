---
title: Use semantically accurate names
description: Choose names that accurately reflect the purpose, scope, and semantics
  of variables, methods, and classes. Names should be self-documenting and eliminate
  ambiguity about what the code element represents or does.
repository: apache/kafka
label: Naming Conventions
language: Java
comments_count: 9
repository_stars: 30575
---

Choose names that accurately reflect the purpose, scope, and semantics of variables, methods, and classes. Names should be self-documenting and eliminate ambiguity about what the code element represents or does.

Key principles:
- **Match scope to name**: If functionality expands beyond the original name, update it accordingly (e.g., `updateVoterPeriodTimer` → `updateVoterSetPeriodTimer` when it handles add, remove, and update operations)
- **Use precise terminology**: Avoid vague or ambiguous terms (e.g., `isMarkedArchived` → `isTerminalState` for a boolean indicating no further state transitions)
- **Make purpose explicit**: Method names should clearly indicate their function (e.g., `getInternalTopics` → `getInternalTopicsToBeDeleted` when the intent is deletion)
- **Eliminate confusion**: When similar concepts exist, use distinguishing names (e.g., `boolean isReconfigSupported` instead of generic parameter names)

Example improvements:
```java
// Before: Ambiguous about what "messages" vs "records" means
int maxInFlightMessages;
// After: Consistent with codebase terminology  
int maxInFlightRecords;

// Before: Unclear what constitutes "marked archived"
private boolean isMarkedArchived = false;
// After: Clear semantic meaning - no further transitions allowed
private boolean isTerminalState = false;

// Before: Generic parameter name requiring context to understand
public void testMethod(boolean withKip853Rpc)
// After: Self-documenting parameter name
public void testMethod(boolean isReconfigSupported)
```

Well-chosen names reduce the need for comments and make code intentions immediately clear to readers.