---
title: Protocol-Safe Encoding
description: Any data placed into connection URIs or transmitted over the network
  (e.g., JSON payloads/headers) must be encoded/serialized according to the protocol’s
  rules.
repository: celery/celery
label: Networking
language: Other
comments_count: 2
repository_stars: 28464
---

Any data placed into connection URIs or transmitted over the network (e.g., JSON payloads/headers) must be encoded/serialized according to the protocol’s rules.

- URIs (userinfo: username/password): Percent-encode all characters in the username/password except RFC “unreserved” (`A-Z a-z 0-9 - . _ ~`) and “sub-delims” (`! $ & ' ( ) * + , ; =`).
- JSON/network metadata: Ensure values are JSON-serializable; don’t emit raw `UUID` objects—convert to a string representation (commonly `.hex` or `str(uuid)`).

Example:
```python
from uuid import uuid4
from urllib.parse import quote

user = quote('alice+team', safe='')
password = quote('p@ss:word', safe='')
uri = f"amqp://{user}:{password}@host/vhost"

# For JSON/headers:
monitoring_id = uuid4().hex  # not uuid4() directly
headers = {"monitoring_id": monitoring_id}
```