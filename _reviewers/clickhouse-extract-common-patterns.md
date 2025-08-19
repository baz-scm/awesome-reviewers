---
title: Extract common patterns
description: Identify and extract repeated code patterns into reusable functions or
  methods to improve maintainability and reduce duplication. When you notice similar
  logic appearing in multiple places, create a common utility function or method that
  can be shared.
repository: ClickHouse/ClickHouse
label: Code Style
language: C++
comments_count: 5
repository_stars: 42425
---

Identify and extract repeated code patterns into reusable functions or methods to improve maintainability and reduce duplication. When you notice similar logic appearing in multiple places, create a common utility function or method that can be shared.

Examples of patterns to extract:

**Callback pattern extraction:**
```cpp
// Instead of repeating this pattern everywhere:
settings.path.push_back(substream);
callback(settings.path);
settings.path.pop_back();

// Extract to a common method:
const auto call_callback_for_substream = [&](const auto substream) {
    settings.path.push_back(substream);
    callback(settings.path);
    settings.path.pop_back();
};
```

**String joining patterns:**
```cpp
// Instead of manual loops:
for (const auto & column_name : copy_query->column_names) {
    // manual concatenation logic
}

// Use existing utilities:
boost::algorithm::join(copy_query->column_names, ", ");
```

**Reuse existing functions:**
```cpp
// Instead of duplicating similar logic:
for (const auto & command : commands) {
    // duplicate partition ID extraction logic
}

// Reuse existing functionality:
MergeTreeData::getPartitionIdsAffectedByCommands(commands);
```

This approach reduces maintenance burden, prevents bugs from inconsistent implementations, and makes the codebase more cohesive. Always check if similar functionality already exists before implementing new logic.