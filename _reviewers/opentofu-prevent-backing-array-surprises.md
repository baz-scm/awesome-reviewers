---
title: Prevent backing array surprises
description: When modifying slices in Go, be aware that appending to a slice with
  available capacity will modify the backing array, potentially affecting other slices
  that share the same backing storage. This can lead to subtle bugs where one operation
  unexpectedly affects seemingly unrelated variables.
repository: opentofu/opentofu
label: Algorithms
language: Go
comments_count: 4
repository_stars: 25901
---

When modifying slices in Go, be aware that appending to a slice with available capacity will modify the backing array, potentially affecting other slices that share the same backing storage. This can lead to subtle bugs where one operation unexpectedly affects seemingly unrelated variables.

For example, this code has a potential issue:

```go
encryptCommand := append(cmd, "--encrypt") 
decryptCommand := append(cmd, "--decrypt")
```

If `cmd` has spare capacity, both slices will share the same backing array, and the second append will overwrite the last element of the first slice.

To avoid this problem:
1. Use `slices.Clip()` to ensure a fresh backing array before appending:
```go
cmd = slices.Clip(cmd)
encryptCommand := append(cmd, "--encrypt")
decryptCommand := append(cmd, "--decrypt")
```

2. Or explicitly create independent copies:
```go
encryptCommand := make([]string, len(cmd)+1)
copy(encryptCommand, cmd)
encryptCommand[len(cmd)] = "--encrypt"
```

This principle applies to other operations where deterministic behavior is crucial, such as:
- Map iteration (use sorted keys for consistency)
- Merging collections (consider equality semantics)
- Boolean expressions (apply transformations consistently)

By understanding the memory model of your data structures, you'll create more predictable, stable algorithms less prone to subtle side effects.