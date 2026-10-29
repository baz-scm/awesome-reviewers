---
title: Team-based access control
description: 'Authorization to repositories and organizations must follow the principle
  of least privilege and be as auditable and revocable as possible. Prefer managing
  permissions through GitHub Teams rather than granting access to individual accounts:
  assign a role (e.g., Technical Committee, Triage) to a team, then add/remove members
  from that team to grant or revoke...'
repository: expressjs/Express
label: Security
language: Markdown
comments_count: 1
repository_stars: 69579
---

Authorization to repositories and organizations must follow the principle of least privilege and be as auditable and revocable as possible. Prefer managing permissions through GitHub Teams rather than granting access to individual accounts: assign a role (e.g., Technical Committee, Triage) to a team, then add/remove members from that team to grant or revoke access in one step. Reserve manual, per-user permission grants (e.g., ad hoc Committer or Project Captain access scoped to specific repos) only for cases where a homogeneous team-based role doesn't fit, and explicitly document which repos/permissions were granted to whom. Any manually granted access must be tracked (e.g., in an access log or README) and periodically reviewed so that stale or unnecessary permissions are promptly revoked, reducing the risk of privilege creep and unauthorized access.</description>
</invoke>
