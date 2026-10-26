---
title: Handle async failures explicitly
description: When composing state from multiple async calls (parallel fetches, follow-up
  probes, or secondary enrichment requests), always check the response status explicitly
  rather than assuming success. A failure in a secondary or optional call must never
  silently corrupt or override state already established by a more authoritative call
  — e.g. an `installed` flag...
repository: Decolua/9Router
label: Error Handling
language: JavaScript
comments_count: 4
repository_stars: 31414
---

When composing state from multiple async calls (parallel fetches, follow-up probes, or secondary enrichment requests), always check the response status explicitly rather than assuming success. A failure in a secondary or optional call must never silently corrupt or override state already established by a more authoritative call — e.g. an `installed` flag derived from a CLI probe should not be flipped to `false` just because a dependent `pip list`/extras lookup failed.

On any failure path (non-ok response, thrown exception, or empty/invalid payload), don't leave the UI or local state in a stale or inconsistent condition: either surface a clear error to the user, clear the affected state, or rehydrate it from a known-good source (e.g. re-run a status check) so client state matches server state. For example, in `saveModels`, check `res.ok` before assuming the save succeeded; on a 400 (e.g. "no models selected"), show the error and call `checkStatus()` to resync instead of leaving the UI showing an empty selection while the server still has the old config.

When error handling involves interpreting HTTP status codes (e.g. validating a provider connection), be precise about which codes represent genuine failures versus transient/retryable conditions. Treat `429`/`5xx`-style responses as transient (still "valid"/retryable) and only treat auth/config errors (e.g. `401`, `403`, `404` for missing resources) as real failures, with explicit test coverage for each classification. Avoid blanket catch-and-ignore patterns (`catch { /* silent */ }`) that swallow errors without resetting dependent state.