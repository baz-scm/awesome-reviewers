---
title: Prefer team-based access control
description: When defining authorization models for repositories or organizations,
  prefer granting permissions to GitHub Teams rather than to individual accounts.
  Team-based access lets you grant and revoke a whole set of permissions by simply
  adding or removing a member from the team, which is far less error-prone and easier
  to audit than manually setting bespoke...
repository: Expressjs/Express
label: Security
language: Markdown
comments_count: 1
repository_stars: 69580
---

When defining authorization models for repositories or organizations, prefer granting permissions to GitHub Teams rather than to individual accounts. Team-based access lets you grant and revoke a whole set of permissions by simply adding or removing a member from the team, which is far less error-prone and easier to audit than manually setting bespoke permissions per repo per user. Reserve individual/manual permission grants only for roles with inherently ad hoc, non-uniform access (e.g., a Project Captain who needs admin on a single repo, or a Committer with write access to a subset of repos), and even then create a team to track membership even if the actual permission bits must still be applied manually. Always document the access hierarchy explicitly (e.g., Technical Committee > Project Captain > Committer), making clear that each level is a superset of the ones below, and specify exactly how each role's permissions are applied and revoked so that stale or orphaned access doesn't accumulate. Before approving new access tiers or roles, verify that the simplest, most auditable mechanism (team-based) is used wherever the permission set is homogeneous, falling back to manual/individual management only when GitHub's permission model requires it.</description>
</invoke>
