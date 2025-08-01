---
title: network service identification
description: Use descriptive string identifiers instead of numeric ports or generic
  IDs when designing network services to avoid conflicts and improve maintainability.
  Different network services should have clearly distinguishable communication channels.
repository: LMCache/LMCache
label: Networking
language: Python
comments_count: 2
repository_stars: 3800
---

Use descriptive string identifiers instead of numeric ports or generic IDs when designing network services to avoid conflicts and improve maintainability. Different network services should have clearly distinguishable communication channels.

When multiple network services operate within the same system, relying solely on numeric ports can lead to conflicts and configuration complexity. Instead, incorporate descriptive service names and contextual information into network identifiers.

Example of problematic approach:
```python
# Unclear what each port is for, potential conflicts
rpc_port = 0  # lookup service
rpc_port = 100  # offload service
socket_path = f"ipc://{base_url}/lmcache_rpc_port_{rpc_port}"
```

Improved approach with descriptive identifiers:
```python
# Clear service identification, no port conflicts
def get_zmq_rpc_path_lmcache(engine_id, service_name, tp_rank):
    return f"ipc://{base_url}/engine_{engine_id}_service_{service_name}_tp_rank_{tp_rank}"

# Usage:
lookup_path = get_zmq_rpc_path_lmcache(engine_id, "lookup", tp_rank)
offload_path = get_zmq_rpc_path_lmcache(engine_id, "offload", tp_rank)
```

This approach eliminates the need for users to configure ports manually, reduces the risk of service conflicts, and makes the system's network architecture self-documenting. The descriptive identifiers make it immediately clear which service each communication channel serves, improving debugging and maintenance.