---
title: Cache Scope and Keys
description: 'When adding or modifying caching/deduplication, ensure the cache identity
  (routing + key + scope) matches the exact contract where reuse is valid.


  Key rules:'
repository: nousresearch/hermes-agent
label: Caching
language: Python
comments_count: 7
repository_stars: 221948
---

When adding or modifying caching/deduplication, ensure the cache identity (routing + key + scope) matches the exact contract where reuse is valid.

Key rules:
- Don’t misroute payloads/data into the wrong cache class (it breaks downstream assumptions). Validate/type-separate before caching.
- Gate dedupe logic to the correct mode/contract; never let a shared dedupe path change a different caller’s behavior.
- Make cache bypass/partition decisions at cache construction time (so the boundary can’t be bypassed by earlier history narrowing).
- Avoid stale fast-path reuse: when you detect an execution path that can desynchronize state (e.g., UI/tab rebinds), mark “possibly diverged” and skip the fast cached result until an authoritative signal updates the cache.
- Cache keys/signatures must encode the real compatibility scope. Don’t collapse distinct variants into one identity (e.g., using only “key present” instead of stable key identity).
- Bound and scope caches: use LRU/eviction, and scope process-global caches by active profile/config signature to prevent cross-profile leakage.

Example (mode-gated dedupe key):
```python
def should_dedupe(event_guid: str, *, use_socketio: bool) -> bool:
    # Dedupe only applies to Socket.IO duplicate suppression.
    return use_socketio and bool(event_guid)
```

Example (scoped config cache):
```python
_config_cache_by_home = {}

def load_audit_config_scoped(hermes_home: str) -> dict:
    key = hermes_home
    if key in _config_cache_by_home:
        return dict(_config_cache_by_home[key])
    cfg = compute_cfg(hermes_home)
    _config_cache_by_home[key] = cfg
    return dict(cfg)
```

Example (signature compatibility without secret material):
- Include stable, non-secret identity fields in the cache signature (e.g., a hashed/derived key identity), not only “key exists”. Ensure the signature changes when runtime auth/session compatibility changes.

Apply these checks during code review: “Is this cache used by multiple call paths/modes? If so, is reuse gated correctly and does the key include all compatibility dimensions? Is the cache bounded and scoped to the correct profile/lifecycle?”