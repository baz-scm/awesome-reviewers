---
title: API extensibility parameters
description: Always design API functions with extensible parameter structures to accommodate
  future feature expansion without breaking changes. Use `Dict opts` parameters instead
  of individual boolean or primitive parameters, unless you are absolutely certain
  no expansion will ever be needed (which is usually wrong).
repository: neovim/neovim
label: API
language: C
comments_count: 2
repository_stars: 91433
---

Always design API functions with extensible parameter structures to accommodate future feature expansion without breaking changes. Use `Dict opts` parameters instead of individual boolean or primitive parameters, unless you are absolutely certain no expansion will ever be needed (which is usually wrong).

This approach prevents the need for API versioning or breaking changes when new functionality is added. Even if the initial implementation doesn't use all possible options, the extensible structure allows for seamless feature additions.

Example of preferred API design:
```c
// Good: Extensible with opts parameter
Tabpage nvim_open_tabpage(Buffer buffer, Boolean enter, Dict opts, Error *err)

// Avoid: Fixed parameters that may need expansion later  
Tabpage nvim_open_tabpage(Buffer buffer, Boolean enter, Error *err)
```

The `opts` dictionary can initially be empty or contain basic options, but provides a clear path for adding features like positioning (`after` parameter mirroring `[count]tabnew`), styling options, or behavioral flags without requiring new API endpoints or breaking existing client code.

This principle applies even when the API seems simple initially - consider future use cases like custom commands (`:restart +qall`) or additional configuration options that users might request.