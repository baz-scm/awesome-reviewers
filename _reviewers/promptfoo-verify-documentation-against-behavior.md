---
title: Verify documentation against behavior
description: Every factual claim in documentation—links, API endpoints, default behaviors,
  required vs. optional settings, supported capabilities, and setup commands—must
  be verified against the actual running system (built site, source code, or live
  execution) before publishing, not assumed. Precisely scope statements to the environment
  or configuration they apply to,...
repository: promptfoo/promptfoo
label: Documentation
language: Markdown
comments_count: 11
repository_stars: 26565
---

Every factual claim in documentation—links, API endpoints, default behaviors, required vs. optional settings, supported capabilities, and setup commands—must be verified against the actual running system (built site, source code, or live execution) before publishing, not assumed. Precisely scope statements to the environment or configuration they apply to, since behavior often differs (e.g., on-prem vs. cloud deployments, local files vs. remote URLs, rootless vs. standard Docker). Concretely:

- Build and click-test generated links/routes rather than guessing them (e.g., confirm a Docusaurus asset link resolves to `/img/...` and not a literal `pathname://...` string; confirm TypeDoc-generated pages resolve to `/reference/` and not `/reference/README`).
- Verify "check" or "health" commands actually exercise the claimed functionality—e.g., prefer `/api/version` with a `currentVersion` field over `/version`, which can fall through to a SPA catch-all and return HTTP 200 without confirming anything.
- Confirm whether a field, endpoint, or config option is actually required or merely optional with a default, and word the docs accordingly (don't present an optional `service_tier` as mandatory).
- Describe default behavior by reading the implementation, not assumption—e.g., disabling external media storage still writes files to a local filesystem path (`FilesystemBlobStorageProvider`), it does not keep everything "in the database," so persistence/backup guidance must reflect that.
- Point environment-specific instructions (API specs, OpenAPI documents, endpoints) at the artifact that matches the deployment being documented—on-prem operators should be directed to their installation's spec, not the public cloud spec, when contracts can diverge.
- Ensure setup commands are complete and account for common variants: include prerequisite steps (e.g., `mkdir -p` before `chown`), and call out edge cases such as rootless Docker or user-namespace remapping that change expected values.
- Qualify capability or usage statements to their actual scope (e.g., `outputPath` format-detection rules apply to local files; remote destinations like Google Sheets URLs behave differently and should be documented separately).

Treat documentation inaccuracies as bugs: reproduce the documented command/link/config against the real system and correct the text to match observed behavior, not the other way around.