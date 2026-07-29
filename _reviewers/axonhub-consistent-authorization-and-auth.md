---
title: Consistent Authorization and Auth
description: 'When changing or adding security-sensitive functionality, keep authorization
  semantics stable and use project-wide shared validation/auth plumbing.


  Apply this standard:'
repository: looplj/axonhub
label: Security
language: Go
comments_count: 5
repository_stars: 4808
---

When changing or adding security-sensitive functionality, keep authorization semantics stable and use project-wide shared validation/auth plumbing.

Apply this standard:
1) Preserve existing access contracts
- If legacy data can’t map to new roles/permissions, keep the “null/legacy” behavior unless you intentionally migrate it with explicit tests for resulting scopes.
2) Validate authorization inputs during permission granting
- When a new permission relies on an external/related entity (e.g., Role tied to an invitation), confirm the role still exists and belongs to the expected project before granting.
3) Don’t introduce partial input-validation patterns
- For identity parameters (e.g., GUIDs), follow the existing project-wide convention; if type validation is desired, implement it once (e.g., in ConvertGUIDToInt or middleware/shared resolver wrapper), not ad-hoc in a subset of mutations.
4) Use shared token/auth providers and correct auth methods
- Prefer the shared OAuth TokenProvider abstraction; let the HttpClient derive headers from `httpReq.Auth` rather than manually mixing header logic. Ensure OAuth always uses the expected auth type (e.g., bearer) and API key auth uses the expected API-key mechanism.
5) Make security posture changes uniformly
- If you want to enforce HTTPS (or similar network security requirements), implement it across all external integrations/checkers consistently rather than patching one client.

Example pattern (authorization contract + validation) inspired by the discussions:

```go
// Preserve legacy behavior by only validating/applying role when role_id exists.
roleID := invitationRow.RoleID
if roleID != nil {
    if _, err := client.Role.Query().Where(
        role.IDEQ(*roleID),
        role.ProjectIDEQ(invitationRow.ProjectID),
    ).Only(ctx); err != nil {
        return fmt.Errorf("invitation role is no longer available")
    }
}
// Otherwise: keep null/legacy semantics to avoid privilege escalation.
```

Net effect: fewer privilege-escalation surprises, fewer auth-header mismatches, and consistent security behavior across the codebase.