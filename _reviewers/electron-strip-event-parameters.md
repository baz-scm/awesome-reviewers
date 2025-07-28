---
title: strip event parameters
description: When exposing IPC event handlers through contextBridge in Electron applications,
  always strip the event parameter before calling renderer callbacks to prevent security
  vulnerabilities. The event object contains `event.sender` which can be exploited
  by malicious code in the renderer process to send arbitrary IPC messages, leading
  to privilege escalation.
repository: electron/electron
label: Security
language: JavaScript
comments_count: 1
repository_stars: 117644
---

When exposing IPC event handlers through contextBridge in Electron applications, always strip the event parameter before calling renderer callbacks to prevent security vulnerabilities. The event object contains `event.sender` which can be exploited by malicious code in the renderer process to send arbitrary IPC messages, leading to privilege escalation.

Instead of directly passing the callback:
```js
onWindowFocus: (callback) => ipcRenderer.on('window-focus', callback)
```

Strip the event parameter by wrapping the callback:
```js
onWindowFocus: (callback) => ipcRenderer.on('window-focus', () => callback())
```

This security practice prevents the renderer process from accessing the event object and its potentially dangerous properties, maintaining proper isolation between the main and renderer processes.