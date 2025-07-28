---
title: Protocol-specific network handling
description: When implementing custom network protocol behavior, ensure that modifications
  are properly scoped to only the intended protocol types and include upstream context
  documentation. Avoid applying protocol-specific changes broadly across all network
  protocols, as this can break assumptions and cause unintended side effects.
repository: electron/electron
label: Networking
language: Other
comments_count: 2
repository_stars: 117644
---

When implementing custom network protocol behavior, ensure that modifications are properly scoped to only the intended protocol types and include upstream context documentation. Avoid applying protocol-specific changes broadly across all network protocols, as this can break assumptions and cause unintended side effects.

Key principles:
1. **Scope restrictions appropriately**: Limit custom behavior to specific protocol types that require it, rather than applying changes universally
2. **Document upstream context**: Include references to upstream changes and their motivations in patch files for future maintainability
3. **Align with upstream behavior**: Keep behavior consistent with upstream implementations except where explicitly needed for specific protocols

Example from streaming protocol handling:
```cpp
// Good: Scoped to streaming custom protocols only
if (IsStreamingCustomProtocol(url)) {
  destination_url_data->set_range_supported();
}

// Avoid: Broad application that could break other protocols
destination_url_data->set_range_supported(); // Applied to all protocols
```

When modifying network service initialization, ensure proper guards are in place:
```cpp
SystemNetworkContextManager* SystemNetworkContextManager::GetInstance() {
  if (!g_system_network_context_manager) {
    content::GetNetworkService();
    DCHECK(g_system_network_context_manager);
  }
  return g_system_network_context_manager;
}
```

This approach prevents breaking buffering assumptions for protocols like file:// URLs while enabling the required functionality for custom streaming protocols that support range requests.