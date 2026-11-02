---
title: Complete session invalidation
description: 'When destroying or logging out a session, you must invalidate it both
  client-side and server-side. Clearing the in-memory session object''s contents (e.g.
  `session.clear()`) is not sufficient: if the underlying store (database, cache,
  etc.) still retains the session data keyed by the session id, an attacker who has
  captured the session cookie can replay it...'
repository: pallets/flask#x
label: Security
language: Python
comments_count: 1
repository_stars: 75163
---

When destroying or logging out a session, you must invalidate it both client-side and server-side. Clearing the in-memory session object's contents (e.g. `session.clear()`) is not sufficient: if the underlying store (database, cache, etc.) still retains the session data keyed by the session id, an attacker who has captured the session cookie can replay it and regain access even after the legitimate user "logged out". Never add a default implementation in a base/abstract session interface that only performs the partial, client-side clear—this gives a false sense of security. Instead, require concrete session interfaces to explicitly implement full destruction: delete the server-side store entry for the session id and expire/clear the client cookie. If a generic implementation cannot safely do both, raise `NotImplementedError` in the base class rather than providing a seemingly safe but incomplete default.

Example of the risk:
```python
def destroy_session(self, app, session):
    # Only clears local session dict - underlying store entry still exists!
    session.clear()
```
Correct approach: remove the entry from the backing store and ensure the session cookie is expired/invalidated, e.g.:
```python
def destroy_session(self, app, session):
    store.delete(session.sid)
    session.clear()
    # ensure response expires the session cookie
```