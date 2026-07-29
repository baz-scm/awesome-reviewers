---
title: Document behavior precisely
description: When updating documentation, ensure every statement about requirements,
  capabilities, and behavior is (1) correct for the current implementation, (2) explicit
  about when the requirement matters (e.g., render-time vs apply-time vs run-time),
  (3) consistent across related doc artifacts, and (4) does not imply unsupported
  configuration paths. Follow house...
repository: maximhq/bifrost
label: Documentation
language: Other
comments_count: 2
repository_stars: 6862
---

When updating documentation, ensure every statement about requirements, capabilities, and behavior is (1) correct for the current implementation, (2) explicit about when the requirement matters (e.g., render-time vs apply-time vs run-time), (3) consistent across related doc artifacts, and (4) does not imply unsupported configuration paths. Follow house style for headings/navigation (e.g., tab names).

How to apply:
- Check “point of impact” phrasing: state prerequisites at the moment they affect the user’s workflow.
- Remove stale/changelog/README prose that no longer matches current guards/behavior; reword to match actual enforcement.
- Keep duplicated sections in sync (if the repo uses byte-identical entries, update all copies identically).
- Don’t add documentation for features that the schema/product doesn’t support (avoid implying a config.json mechanism when it isn’t available).
- Match house style for UI labels and section/tab names.

Example (pattern to follow when prerequisites only matter at apply-time):
- Good:
  “Set `serviceMonitor.enabled: true` to render a `ServiceMonitor` targeting the `http` service port. The `monitoring.coreos.com/v1` CRDs must be present when the manifest is applied; rendering itself does not require them.”
- Avoid:
  “CRDs are required to render,” if rendering succeeds without them.