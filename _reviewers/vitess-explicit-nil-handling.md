---
title: Explicit nil handling
description: 'Always handle nil values explicitly in your code to improve clarity
  and prevent subtle bugs. When a function needs to deal with potentially nil values:'
repository: vitessio/vitess
label: Null Handling
language: Go
comments_count: 4
repository_stars: 19815
---

Always handle nil values explicitly in your code to improve clarity and prevent subtle bugs. When a function needs to deal with potentially nil values:

1. Document the expected behavior when nil values are encountered
2. Use early returns to handle nil cases at the beginning of functions
3. Avoid silent fall-throughs in switch statements when handling nil
4. Know when nil checks are necessary versus when Go handles nil cases automatically

For example, instead of using a switch statement with a fall-through for nil:

```go
func AppendGTIDInPlace(rp Position, gtid GTID) Position {
  switch {
  case gtid == nil:
  case rp.GTIDSet == nil:
    rp.GTIDSet = gtid.GTIDSet()
  default:
    // Handle non-nil case
  }
  // ...
}
```

Prefer explicit handling with early returns:

```go
func AppendGTIDInPlace(rp Position, gtid GTID) Position {
  // If gtid is nil, treat it as a no-op and return the input Position.
  if gtid == nil {
    return rp
  }
  if rp.GTIDSet == nil {
    rp.GTIDSet = gtid.GTIDSet()
  } else {
    // Handle non-nil case
  }
  // ...
}
```

Also, remember that Go has built-in nil handling for some operations. For instance, append works safely with nil slices:

```go
// This is unnecessary
if req.FilterRules != nil {
  bls.Filter.Rules = append(bls.Filter.Rules, req.FilterRules...)
}

// This is sufficient
bls.Filter.Rules = append(bls.Filter.Rules, req.FilterRules...)
```

This approach makes the intention clear, improves code readability, and prevents unexpected behavior.