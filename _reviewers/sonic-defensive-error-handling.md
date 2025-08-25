---
title: Defensive error handling
description: Implement defensive checks when managing error state to prevent overwriting
  existing errors and add safeguards even when theoretically unnecessary. This approach
  helps avoid subtle bugs and makes code more robust against future modifications.
repository: bytedance/sonic
label: Error Handling
language: Go
comments_count: 2
repository_stars: 8532
---

Implement defensive checks when managing error state to prevent overwriting existing errors and add safeguards even when theoretically unnecessary. This approach helps avoid subtle bugs and makes code more robust against future modifications.

Key practices:
- Check if an error already exists before setting a new one
- Add defensive checks in error-prone scenarios even if the underlying implementation already handles them
- Prioritize code safety over theoretical optimization

Example from the codebase:
```go
// Before: Risk of overwriting existing error
if self.readMore() {
    goto try_skip
} else {
    err = SyntaxError{e, self.s, types.ParsingError(-s), ""}
    self.setErr(err)
    return
}

// After: Defensive check prevents overwriting
if self.readMore() {
    goto try_skip
}
if self.err == nil {
    self.setErr(SyntaxError{e, self.s, types.ParsingError(-s), ""})
}
return self.err
```

This defensive approach prevents losing important error context and makes the code more maintainable as it evolves.