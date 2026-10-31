---
title: Secure session lifecycle management
description: Session destroy, regenerate, and state-tracking logic must fully and
  correctly invalidate or update session state to prevent fixation/hijacking vulnerabilities.
  Never implement destroy/regenerate as a no-op in a shared base class — any class
  managing session storage must ensure that destroying a session clears both the client-side
  token (e.g., cookie) and...
repository: pallets/flask
label: Security
language: Python
comments_count: 2
repository_stars: 75022
---

Session destroy, regenerate, and state-tracking logic must fully and correctly invalidate or update session state to prevent fixation/hijacking vulnerabilities. Never implement destroy/regenerate as a no-op in a shared base class — any class managing session storage must ensure that destroying a session clears both the client-side token (e.g., cookie) and the corresponding server-side store entry. Leaving either one intact lets an attacker reuse a captured cookie to access a session the user believes was invalidated (e.g., after logout). Similarly, internal flags that drive security-relevant behavior (such as whether a session is "new," which can affect fixation protections or regeneration logic) must be updated precisely on every relevant state transition — e.g., reading data from a session does not make it non-new, only writing/modifying should. When adding session-related methods, verify end-to-end that all paths (cookie + backing store) are invalidated together and that state flags accurately reflect the session's true lifecycle stage before relying on them for security decisions.