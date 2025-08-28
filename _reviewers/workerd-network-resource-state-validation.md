---
title: Network resource state validation
description: Always validate the state of network resources (sockets, streams, connections)
  before performing operations to prevent errors, resource leaks, and ensure proper
  connection reuse.
repository: cloudflare/workerd
label: Networking
language: Other
comments_count: 5
repository_stars: 6989
---

Always validate the state of network resources (sockets, streams, connections) before performing operations to prevent errors, resource leaks, and ensure proper connection reuse.

Network resources have complex lifecycles and can be in various states (pending, active, closed, locked, disturbed). Performing operations on resources in invalid states can lead to connection failures, resource leaks, or security issues.

Key validations to perform:

1. **Socket state before conversion**: Check that sockets are not locked, disturbed, or closed before wrapping them in HTTP clients
2. **Stream state before detachment**: Ensure no pending reads/writes are in flight before detaching streams from their JavaScript wrappers  
3. **Connection completion before reuse**: Fully consume response bodies before following redirects to allow connection reuse
4. **Resource ownership during operations**: Prevent destruction of underlying resources (HttpClient, streams) while requests are in progress

Example implementation:
```cpp
kj::Own<kj::AsyncIoStream> Socket::takeConnectionStream(jsg::Lock& js) {
  // Validate no pending operations before detaching
  writable->detach(js);  // Will throw if pending writes
  readable->detach(js);  // Will throw if pending reads
  
  // Update state to prevent further use
  upgraded = true;
  closedResolver.resolve(js);
  return connectionStream->addWrappedRef();
}

// Before creating HTTP client from socket
JSG_ASSERT(!socket->isLocked(), Error, "Socket streams are locked");
JSG_ASSERT(!socket->isClosed(), Error, "Socket is already closed");
```

This validation prevents runtime errors, ensures proper resource cleanup, and maintains connection reuse capabilities essential for network performance.