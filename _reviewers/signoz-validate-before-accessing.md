---
title: validate before accessing
description: Always validate bounds, nil pointers, and other potentially unsafe conditions
  before accessing values to prevent runtime panics and undefined behavior. This includes
  checking array/slice bounds, validating pointer references, and ensuring data structures
  are in expected states before use.
repository: SigNoz/signoz
label: Null Handling
language: Go
comments_count: 2
repository_stars: 23369
---

Always validate bounds, nil pointers, and other potentially unsafe conditions before accessing values to prevent runtime panics and undefined behavior. This includes checking array/slice bounds, validating pointer references, and ensuring data structures are in expected states before use.

Key validation patterns:
- **Bounds checking**: Verify indices are within valid ranges before array/slice access
- **Nil pointer validation**: Check pointers are not nil before dereferencing
- **State validation**: Ensure objects are in expected states before operations

Example from bounds checking:
```go
size := ts.Size()
for i := start; i <= stop && i >= 0 && i < size; i++ {
    if tok := ts.Get(i); tok != nil && tok.GetTokenType() != antlr.TokenEOF {
        b.WriteString(tok.GetText())
    }
}
```

Example from pointer validation:
```go
func ValidatePointer(dest any, caller string) error {
    rv := reflect.ValueOf(dest)
    if rv.Kind() != reflect.Pointer || rv.IsNil() {
        return WrapCacheableErrors(reflect.TypeOf(dest), caller)
    }
    return nil
}
```

This proactive validation approach prevents common sources of runtime errors and makes code more robust by catching potential issues before they cause panics or undefined behavior.