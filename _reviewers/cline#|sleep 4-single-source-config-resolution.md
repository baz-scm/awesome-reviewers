---
title: Single-source config resolution
description: When a value depends on environment or backend configuration (API base
  URLs, app URLs, host names, default remotes, derived flags), resolve it exactly
  once from a single authoritative source and reuse that resolved value everywhere
  instead of letting each call site re-derive it with its own logic. Independent resolution
  paths drift apart over time and cause...
repository: cline/cline#|sleep 4
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70979
---

When a value depends on environment or backend configuration (API base URLs, app URLs, host names, default remotes, derived flags), resolve it exactly once from a single authoritative source and reuse that resolved value everywhere instead of letting each call site re-derive it with its own logic. Independent resolution paths drift apart over time and cause real bugs, e.g. a privacy-settings link computed from `appBaseUrl` while the account API was resolved from a provider `baseUrl` override, so a staging backend linked to production; or a sidecar command re-reading provider settings on every call instead of using the value resolved once at startup; or two different "pick the primary remote" rules in different modules that could end up targeting different repositories. Prefer resolving configuration once during initialization (e.g. at startup, or once per session) and threading the resolved value through context/state rather than recomputing it per request. If duplicate resolution logic cannot be unified immediately, document why and ensure both paths are exercised by the same user-visible confirmation so they cannot silently diverge. When a derived default and an explicit caller-supplied value can both apply, let the explicit value always win, using a pattern like `caller.value ?? derivedDefault`, so environment-derived defaults never override settings a caller deliberately set. Add targeted tests that pin the resolved value for each environment/override combination (e.g. staging override resolves to the staging URL, an unrecognized backend resolves to `undefined` and hides the dependent UI, an explicit flag beats the derived default).