---
title: REST API conventions
description: Follow standard REST API conventions for HTTP methods, status codes,
  endpoint structure, and response completeness. Use appropriate access controls and
  implement proper pagination patterns.
repository: SigNoz/signoz
label: API
language: Go
comments_count: 4
repository_stars: 23369
---

Follow standard REST API conventions for HTTP methods, status codes, endpoint structure, and response completeness. Use appropriate access controls and implement proper pagination patterns.

Key principles:
- Use standard HTTP methods with correct status codes (POST → 201 Created, GET → 200 OK, DELETE → 204 No Content)
- Structure endpoints following REST conventions: `POST /api/v1/orgs/me/resource` for creation, `GET /api/v1/orgs/me/resource/:id` for retrieval
- Apply appropriate access controls (viewAccess vs openAccess) - avoid openAccess for endpoints that should require authentication
- Return complete objects in responses, including mandatory fields like ID
- Implement cursor/token-based pagination instead of limit-only approaches

Example of proper REST endpoint structure:
```go
// Good: Standard REST conventions
traceFunnelsRouter.HandleFunc("", am.ViewAccess(aH.Create)).Methods(http.MethodPost)     // POST /api/v1/orgs/me/trace-funnels
traceFunnelsRouter.HandleFunc("", am.ViewAccess(aH.List)).Methods(http.MethodGet)       // GET /api/v1/orgs/me/trace-funnels  
traceFunnelsRouter.HandleFunc("/{id}", am.ViewAccess(aH.Get)).Methods(http.MethodGet)   // GET /api/v1/orgs/me/trace-funnels/:id
traceFunnelsRouter.HandleFunc("/{id}", am.ViewAccess(aH.Update)).Methods(http.MethodPut) // PUT /api/v1/orgs/me/trace-funnels/:id

// Bad: Non-standard endpoints
router.HandleFunc("/api/v1/export", am.OpenAccess(ah.Export)).Methods(http.MethodGet)  // Should use viewAccess
traceFunnelsRouter.HandleFunc("/new", am.ViewAccess(aH.New)).Methods(http.MethodPost)  // Should be POST to base path
```

This ensures APIs are predictable, secure, and follow industry standards that developers expect.