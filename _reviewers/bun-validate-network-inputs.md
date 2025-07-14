---
title: Validate network inputs
description: 'Network code must validate all inputs and handle error conditions properly
  to prevent security vulnerabilities and reliability issues. This includes:

  '
repository: oven-sh/bun
label: Networking
language: C++
comments_count: 2
repository_stars: 79093
---

Network code must validate all inputs and handle error conditions properly to prevent security vulnerabilities and reliability issues. This includes:

1. Reset state between repeated network operations - especially in event loops where state changes with each iteration
2. Use safe type conversions with explicit error handling
3. Check buffer boundaries and protocol state

Example for select loops:
```c
while (true) {
    // Reset state at beginning of each iteration
    FD_ZERO(&read_set);
    FD_SET(kqueue_fd, &read_set);
    for (size_t i = 0; i < fds_len; i++) {
        FD_SET(fds[i], &read_set);
    }
    
    int rv = select(max_fd + 1, &read_set, NULL, NULL, NULL);
    // Handle errors...
}
```

Example for type conversions in protocol handling:
```cpp
// Use safe conversion with error handling
llhttp_type_t type = static_cast<llhttp_type_t>(typeValue.toNumber(globalObject));
RETURN_IF_EXCEPTION(scope, {});
```

Failing to properly validate network inputs can lead to subtle bugs like missed events in event loops, crashed servers due to unexpected input formats, or even security vulnerabilities that could be exploited by malicious actors.