---
title: Document connection scope
description: When documenting network connection operations, clearly specify the scope
  of when operations are supported and their limitations. Include information about
  initial connection requirements, fallback behaviors, and unsupported scenarios to
  help users understand operational boundaries.
repository: neovim/neovim
label: Networking
language: Txt
comments_count: 2
repository_stars: 91433
---

When documenting network connection operations, clearly specify the scope of when operations are supported and their limitations. Include information about initial connection requirements, fallback behaviors, and unsupported scenarios to help users understand operational boundaries.

For connection management commands, document:
- Prerequisites (e.g., "This only works if the UI started the server initially")
- Fallback behaviors (e.g., "this command is equivalent to |:detach|")
- Unsupported scenarios (e.g., "If the UI connected to some random remote endpoint, that is out of scope")

Example:
```
:connect {address}
                Detaches the UI from the server it is currently attached to
                and attaches it to the server at {address} instead.

                Note: If the current UI hasn't implemented the "connect" UI
                event, this command is equivalent to |:detach|.
```

This prevents user confusion and sets proper expectations about connection operation capabilities and constraints.