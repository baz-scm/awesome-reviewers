---
title: Follow GoDoc conventions
description: 'Document code following Go''s official documentation style guide (https://tip.golang.org/doc/comment).
  All exported functions, types, interfaces, and struct fields should have descriptive
  comments. '
repository: ollama/ollama
label: Documentation
language: Go
comments_count: 8
repository_stars: 145704
---

Document code following Go's official documentation style guide (https://tip.golang.org/doc/comment). All exported functions, types, interfaces, and struct fields should have descriptive comments. 

Function documentation should start with the function name and a verb describing what it does:

```go
// addContent returns the thinking content and the normal content that should be
// immediately sent to the user. It will internally buffer if it needs to see
// more content to disambiguate
func (s *thinkingParser) addContent(content string) (string, string) {
    // Implementation
}
```

For struct fields, place comments on the line above each field:

```go
type ErrorResponse struct {
    // Err is the error from the server. It helps with debugging the code-path
    Err  string `json:"error"`

    // Hint is a user-friendly message about what went wrong, with suggested troubleshooting
    Hint string `json:"hint"`
}
```

Document interfaces thoroughly, especially when they serve as implementation guides for different backends:

```go
// ScaledDotProductAttention defines operations for attention computation
// that must be implemented by backend providers
type ScaledDotProductAttention interface {
    // Methods...
}
```

Include parameter descriptions when their purpose isn't obvious:

```go
// parseJSONToolCalls attempts to parse a JSON string into a slice of ToolCalls.
// It first checks for balanced braces before attempting to parse.
// Parameters:
//   - s: The JSON string to parse
//   - name: The field name representing the tool name in the JSON
//   - arguments: The field name representing the tool arguments in the JSON
// Returns:
//   - []api.ToolCall: The parsed tool calls if successful
//   - error: ErrAccumulateMore if braces unbalanced, ErrInvalidToolCall if invalid, or nil if successful
func parseJSONToolCalls(s string, name, arguments string) ([]api.ToolCall, error) {
```

Always explain non-obvious behaviors or design decisions:

```go
// topK limits the number of tokens considered to the k highest logits.
// The slice is passed by pointer because its length will be modified to k.
func topK(ts *[]token, k int) {
    // Implementation
}
```