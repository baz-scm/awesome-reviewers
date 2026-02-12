---
title: centralize sentinel names
description: 'Define and use named constants for special sentinel identifiers (e.g.,
  "local", "connected") and add semantic methods on domain types near their definitions
  to encapsulate boolean checks (e.g., RemoteType.IsLocal()). Motivation: magic strings
  and scattered boolean logic reduce clarity and increase risk of inconsistent checks.
  Placing constants and small...'
repository: wavetermdev/waveterm
label: Naming Conventions
language: Go
comments_count: 2
repository_stars: 17328
---

Define and use named constants for special sentinel identifiers (e.g., "local", "connected") and add semantic methods on domain types near their definitions to encapsulate boolean checks (e.g., RemoteType.IsLocal()). Motivation: magic strings and scattered boolean logic reduce clarity and increase risk of inconsistent checks. Placing constants and small predicates next to the type that owns the concept creates a single source of truth and improves identifier semantics.

How to apply:
- Replace literal sentinel strings with package-scoped constants with clear names. Put them in a file close to related resolver/constants (or the type they relate to). Example:
  // in resolver.go (or near R_Remote definitions)
  const (
      SentinelLocal     = "local"
      SentinelConnected = "connected"
  )
  // Use SentinelLocal instead of "local" throughout code.

- Add semantic helper methods on the domain type that perform common checks instead of repeating boolean expressions. Place these methods beside the type declaration (e.g., sstore.go next to RemoteType):
  func (r RemoteType) IsLocal() bool {
      // encapsulate the precise logic once
      return r.Local && !r.IsSudo()
  }

- Use the constants and helpers where previously ad-hoc logic occurred. Example replacement from discussion:
  // before: if ids.Remote.DisplayName == "local" { ... }
  // after:
  if ids.Remote.DisplayName == SentinelLocal || ids.Remote.IsLocal() {
      // consistent handling for local remote
  }

Rules summary:
- Never scatter sentinel string literals across code; declare named constants.
- Place constants near related resolver/type definitions for discoverability.
- Encapsulate repeated boolean checks in clearly named methods on the owning type (IsLocal, IsSudo, etc.).
- Prefer calling the helper methods (r.IsLocal()) rather than repeating the boolean expression.

Benefits: improves readability, ensures consistency, reduces bugs from divergent checks, and makes future changes (e.g., renaming sentinel values or changing local-ness rules) much simpler.