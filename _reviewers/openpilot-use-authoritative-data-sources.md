---
title: Use authoritative data sources
description: When working with network-related data, always read from the most direct
  and authoritative source available rather than making assumptions or relying on
  indirect indicators. This ensures accuracy and robustness in network operations.
repository: commaai/openpilot
label: Networking
language: Other
comments_count: 2
repository_stars: 58214
---

When working with network-related data, always read from the most direct and authoritative source available rather than making assumptions or relying on indirect indicators. This ensures accuracy and robustness in network operations.

For network connections, query the active connection state directly instead of inferring properties from adapter information. For data format detection, examine file headers or content signatures rather than relying solely on file extensions that may be absent or misleading.

Example of preferred approach:
```cpp
// Instead of guessing from adapter
bool WifiManager::currentNetworkMetered() {
  // Read from active connection directly
  return getActiveConnectionMeteredStatus();
}

// Instead of relying only on file extensions
if (url.find(".bz2") != std::string::npos) {
  data = decompressBZ2(data, abort);
} else {
  // Also detect from file header like python LogReader
  if (detectBZ2Header(data)) {
    data = decompressBZ2(data, abort);
  }
}
```

This approach prevents issues when indirect indicators (like file extensions) are removed or when adapter properties don't accurately reflect the actual network state.