---
title: mark experimental configuration features
description: Always mark experimental and deprecated configuration options with appropriate
  stability indicators in documentation. Use `_Experimental_` for features under active
  development and `_Deprecated_` for features being phased out. This helps developers
  make informed decisions about which configuration options are safe for production
  use.
repository: electron/electron
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 117644
---

Always mark experimental and deprecated configuration options with appropriate stability indicators in documentation. Use `_Experimental_` for features under active development and `_Deprecated_` for features being phased out. This helps developers make informed decisions about which configuration options are safe for production use.

For experimental features, consider including additional context about stability expectations:

```markdown
* `windowStateRestoreOptions` [WindowStateRestoreOptions](window-state-restore-options.md?inline) (optional) - Options for saving and restoring window state: position, size, maximized state, etc. _Experimental_

* `deprecatedPasteEnabled` boolean (optional) - Whether to enable the `paste` [execCommand](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand). Default is `false`. _Deprecated_

* `frozenIntrinsics` boolean (optional) - Experimental option for passing [`--frozen-intrinsics`](https://nodejs.org/api/cli.html#--frozen-intrinsics) to Node.js.
```

For command-line switches marked as experimental in Node.js docs, maintain consistency by flagging them appropriately in Electron documentation as well. This practice ensures developers understand the maturity and support level of configuration options they're considering.