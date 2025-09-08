---
title: Comprehensive function documentation
description: Functions, methods, and non-trivial constants should include comprehensive
  documentation that explains their purpose, behavior, parameters, and relationships
  to similar functionality. Documentation should be precise about what the code does
  and when errors may occur, avoiding misleading statements.
repository: gravitational/teleport
label: Documentation
language: Go
comments_count: 6
repository_stars: 19109
---

Functions, methods, and non-trivial constants should include comprehensive documentation that explains their purpose, behavior, parameters, and relationships to similar functionality. Documentation should be precise about what the code does and when errors may occur, avoiding misleading statements.

Key documentation elements to include:
- **Purpose**: What the function does and why it exists
- **Parameters**: What input/output parameters represent, especially for complex types
- **Error conditions**: When and what types of errors may be returned (use "may return" rather than "returns" for conditional errors)
- **Relationships**: How the function relates to similar or alternative functions
- **Context**: Additional context that helps developers understand usage

Example of comprehensive documentation:
```go
// fromWhereExpr translates a WhereExpr to a database filter expression.
// The condFilterParams serves as both input and output, where attrValues 
// maps placeholder names to their values and attrNames maps field names 
// to their database column equivalents.
func fromWhereExpr(cond *types.WhereExpr, params *condFilterParams) (string, error) {
    // implementation
}

// yamuxTunnelALPN is the ALPN (Application-Layer Protocol Negotiation) 
// identifier used for Yamux multiplexed tunnel connections in Teleport's 
// relay tunnel protocol.
const yamuxTunnelALPN = "teleport-relaytunnel"
```

For deprecated functions, include specific migration guidance and deletion timelines when available. Focus documentation on explaining what problems the code solves rather than just describing implementation details.