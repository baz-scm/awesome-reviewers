---
title: Return errors explicitly
description: Functions should return errors explicitly to callers rather than terminating
  the program, hiding errors in boolean returns, or using implicit error handling.
  This allows higher-level code to make appropriate decisions about error handling,
  recovery, and program flow.
repository: istio/istio
label: Error Handling
language: Go
comments_count: 6
repository_stars: 37192
---

Functions should return errors explicitly to callers rather than terminating the program, hiding errors in boolean returns, or using implicit error handling. This allows higher-level code to make appropriate decisions about error handling, recovery, and program flow.

**Key principles:**
1. **Avoid fatal calls in library code** - Use `return fmt.Errorf(...)` instead of `log.Fatalf()` or `t.Fatalf()`
2. **Return errors alongside other values** - Don't hide error conditions in boolean returns; make them explicit
3. **Make error handling decisions explicit** - Avoid implicit defaults that could mask important error conditions

**Example of problematic pattern:**
```go
func fileExists(filename string) bool {
    _, err := os.Stat(filename)
    if err != nil && !os.IsNotExist(err) {
        log.Warnf("Unexpected error checking file %s: %v", filename, err)
    }
    return err == nil
}

func initBpfObjects() {
    if err := os.Mkdir(MapsPinpath, os.ModePerm); err != nil {
        log.Fatalf("unable to create ambient bpf mount directory: %v", err)
    }
}
```

**Improved pattern:**
```go
func fileExists(filename string) (bool, error) {
    if filename == "" {
        return false, nil
    }
    _, err := os.Stat(filename)
    if err != nil && !os.IsNotExist(err) {
        return false, fmt.Errorf("unexpected error checking file %s: %v", filename, err)
    }
    return err == nil, nil
}

func initBpfObjects() error {
    if err := os.Mkdir(MapsPinpath, os.ModePerm); err != nil {
        return fmt.Errorf("unable to create ambient bpf mount directory: %v", err)
    }
    return nil
}
```

This approach provides callers with the flexibility to implement appropriate error handling strategies, retry logic, or graceful degradation based on their specific context and requirements.