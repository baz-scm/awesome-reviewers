---
title: design extensible APIs
description: When designing APIs, prioritize extensibility and backwards compatibility
  over convenience. Avoid modifying existing response types or interfaces in ways
  that could break existing clients. Instead, create new dedicated types, methods,
  or optional parameters.
repository: argoproj/argo-cd
label: API
language: Go
comments_count: 4
repository_stars: 20149
---

When designing APIs, prioritize extensibility and backwards compatibility over convenience. Avoid modifying existing response types or interfaces in ways that could break existing clients. Instead, create new dedicated types, methods, or optional parameters.

Key principles:
- Create dedicated response objects instead of adding fields to existing types that could introduce breaking changes
- Add new interface methods or create separate interfaces rather than extending existing ones inappropriately  
- Use optional parameters and configuration objects to support customization without breaking existing usage
- Consider the impact on existing clients when modifying API contracts

Examples:
```go
// Instead of modifying existing ApplicationList
type ApplicationList struct {
    Items []Application `json:"items"`
    Stats ApplicationListStats `json:"stats,omitempty"` // Breaking change!
}

// Create a dedicated response object
type ApplicationListResponse struct {
    Applications ApplicationList `json:"applications"`
    Stats ApplicationListStats `json:"stats,omitempty"`
}

// Instead of extending existing interface inappropriately
type Provider interface {
    Verify(tokenString string) (*gooidc.IDToken, error)
    VerifyJWT(tokenString string) (*jwtgo.Token, error) // Mixing concerns
}

// Create separate interfaces or new implementations
type JWTProvider interface {
    VerifyJWT(tokenString string) (*jwtgo.Token, error)
}

// Support optional parameters for extensibility
func NewClient(repoURL string, creds Creds, opts ...ClientOpts) (Client, error) {
    // Allows adding new options without breaking existing calls
}
```

This approach ensures APIs can evolve gracefully while maintaining compatibility with existing integrations.