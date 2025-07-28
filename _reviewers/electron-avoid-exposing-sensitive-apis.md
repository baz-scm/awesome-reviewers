---
title: Avoid exposing sensitive APIs
description: 'Do not enable configurations that expose Node.js or Electron APIs to
  untrusted web content in renderer processes. This includes avoiding `nodeIntegration:
  true` for remote content and not directly exposing IPC APIs in preload scripts.'
repository: electron/electron
label: Security
language: Markdown
comments_count: 4
repository_stars: 117644
---

Do not enable configurations that expose Node.js or Electron APIs to untrusted web content in renderer processes. This includes avoiding `nodeIntegration: true` for remote content and not directly exposing IPC APIs in preload scripts.

**Why this matters:**
- Enabling `nodeIntegration: true` disables sandboxing and grants full Node.js access to renderer processes
- Exposing raw APIs like `ipcRenderer.on` gives renderers direct access to the entire IPC event system
- Remote content should never have access to these privileged APIs due to security risks

**Secure approach:**
```js
// ❌ Dangerous - exposes Node.js APIs to remote content
new BrowserWindow({
  webPreferences: {
    nodeIntegration: true, // Disables sandbox, security risk
    contextIsolation: false
  }
})

// ✅ Secure - use sandboxed renderer with controlled API exposure
new BrowserWindow({
  webPreferences: {
    sandbox: true, // Default since Electron 20
    contextIsolation: true, // Default since Electron 20
    preload: path.join(__dirname, 'preload.js')
  }
})

// In preload.js - expose only specific, validated APIs
const { contextBridge, ipcRenderer } = require('electron')

// ❌ Don't expose raw IPC
window.ipcRenderer = ipcRenderer

// ✅ Expose controlled, specific functions
contextBridge.exposeInMainWorld('electronAPI', {
  performAction: (...args) => ipcRenderer.invoke('perform-action', ...args)
})
```

Always validate the origin and content when handling requests from renderer processes, especially when loading remote content. Use the principle of least privilege - only expose the minimum APIs necessary for your application to function.