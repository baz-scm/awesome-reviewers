---
title: Maintain code readability
description: 'Ensure code remains readable and maintainable by following these practices:


  1. **Combine case statements with identical outcomes** to reduce duplication. When
  multiple cases have identical code blocks, group them together:'
repository: influxdata/influxdb
label: Code Style
language: Go
comments_count: 5
repository_stars: 30268
---

Ensure code remains readable and maintainable by following these practices:

1. **Combine case statements with identical outcomes** to reduce duplication. When multiple cases have identical code blocks, group them together:

```go
// GOOD
switch planType {
case tsm1.PT_Standard, tsm1.PT_SmartOptimize:
    return common
case tsm1.PT_NoOptimize:
    return testLevelResults{}
}

// AVOID
switch planType {
case tsm1.PT_Standard:
    return common
case tsm1.PT_SmartOptimize:
    return common
case tsm1.PT_NoOptimize:
    return testLevelResults{}
}
```

2. **Extract common values** to avoid repetition, especially in maps or switch statements:

```go
// GOOD
common := testLevelResults{
    level4Groups: []tsm1.PlannedCompactionGroup{
        {
            tsm1.CompactionGroup{"01-05.tsm", "02-05.tsm", "03-05.tsm", "04-04.tsm"},
            tsdb.DefaultMaxPointsPerBlock,
        },
    },
}

switch planType {
case tsm1.PT_Standard, tsm1.PT_SmartOptimize, tsm1.PT_NoOptimize:
    return common
}
```

3. **Use named constants instead of magic numbers**. Operations between constants should also be assigned to named constants:

```go
// GOOD
const AggressiveMaxPointsPerBlock = DefaultMaxPointsPerBlock * 100

// AVOID
e.Compactor.Size = tsdb.DefaultMaxPointsPerBlock * 100
```

4. **Simplify nested conditionals** where possible:

```go
// GOOD
var loaded bool
if f, loaded = m.fields.LoadOrStore(newField.Name, newField); f.Type != typ {
    return f, !loaded, ErrFieldTypeConflict
} 
return f, !loaded, nil

// AVOID
if f, loaded := m.fields.LoadOrStore(newField.Name, newField); loaded {
    if f.Type != typ {
        return f, false, ErrFieldTypeConflict
    }
    return f, false, nil
} else {
    return f, true, nil
}
```

These practices make code easier to understand, maintain, and reduce bugs from copy-paste errors or inconsistencies.