---
title: Clean network resources
description: Always properly close and clean up network connections to prevent memory
  leaks and resource exhaustion. When establishing WebSocket connections or other
  network resources, ensure they are explicitly closed and event listeners are removed
  when no longer needed. Additionally, implement resilient error handling strategies
  for network operations by using...
repository: vitejs/vite
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 74031
---

Always properly close and clean up network connections to prevent memory leaks and resource exhaustion. When establishing WebSocket connections or other network resources, ensure they are explicitly closed and event listeners are removed when no longer needed. Additionally, implement resilient error handling strategies for network operations by using approaches like `Promise.allSettled()` instead of `Promise.all()` to handle partial failures gracefully.

Example:
```javascript
// Bad practice - potential memory leak
async function pingServer(socketProtocol, hostAndPath) {
  const socket = new WebSocket(
    `${socketProtocol}://${hostAndPath}`,
    'vite-ping'
  )
  return new Promise((resolve) => {
    socket.addEventListener('open', () => resolve(true))
    socket.addEventListener('error', () => resolve(false))
  })
}

// Good practice - properly managed resources
async function pingServer(socketProtocol, hostAndPath) {
  const socket = new WebSocket(
    `${socketProtocol}://${hostAndPath}`,
    'vite-ping'
  )
  return new Promise((resolve) => {
    const onOpen = () => {
      cleanup()
      resolve(true)
    }
    const onError = () => {
      cleanup()
      resolve(false)
    }
    
    socket.addEventListener('open', onOpen)
    socket.addEventListener('error', onError)
    
    function cleanup() {
      socket.removeEventListener('open', onOpen)
      socket.removeEventListener('error', onError)
      socket.close()
    }
  })
}

// Use Promise.allSettled for resilient multi-request handling
async function loadResources(urls) {
  // Will continue even if some requests fail
  const results = await Promise.allSettled(
    urls.map(url => fetch(url))
  )
  // Process successful results, handle failures gracefully
  return results.filter(r => r.status === 'fulfilled').map(r => r.value)
}
```