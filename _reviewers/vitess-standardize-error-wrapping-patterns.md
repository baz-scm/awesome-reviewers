---
title: Standardize error wrapping patterns
description: 'Use consistent error wrapping patterns to preserve error context and
  ensure proper error code propagation. Always:

  1. Use vterrors.New/Errorf when creating new errors to include error codes'
repository: vitessio/vitess
label: Error Handling
language: Go
comments_count: 4
repository_stars: 19815
---

Use consistent error wrapping patterns to preserve error context and ensure proper error code propagation. Always:
1. Use vterrors.New/Errorf when creating new errors to include error codes
2. Use vterrors.Wrapf when wrapping existing errors to maintain the error chain
3. Use errors.As for type checking to handle error wrapping chains
4. Apply specific error codes (e.g. VT13001) for known error categories

Example:

```go
// Don't do this:
if err != nil {
    return fmt.Errorf("failed to delete workflow %s: %v", name, err)
}

// Do this instead:
if err != nil {
    return vterrors.Wrapf(err, "failed to delete workflow %s", name)
}

// Don't do this:
if _, ok := err.(ConfigFileNotFoundError); ok {
    return true
}

// Do this instead:
var configErr ConfigFileNotFoundError
if errors.As(err, &configErr) {
    return true
}

// Don't do this:
return nil, fmt.Errorf("opcode: %v not supported", opcode)

// Do this instead:
return nil, vterrors.VT13001(fmt.Sprintf("opcode: %v not supported", opcode))
```