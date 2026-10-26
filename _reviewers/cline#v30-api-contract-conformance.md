---
title: API contract conformance
description: 'Ensure API behavior matches the declared contract end-to-end: conform
  to spec gating, forward payload fields through every projection/handler path, and
  avoid silent semantic changes.'
repository: cline/cline#v30
label: API
language: TypeScript
comments_count: 5
repository_stars: 70894
---

Ensure API behavior matches the declared contract end-to-end: conform to spec gating, forward payload fields through every projection/handler path, and avoid silent semantic changes.

Apply this checklist when changing request/response shapes or host/plugin/tool exposure:
1) **Spec gating is unconditional**: If the spec says the host *must not* expose certain items (e.g., tool visibility excludes `