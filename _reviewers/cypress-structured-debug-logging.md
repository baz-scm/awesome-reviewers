---
title: structured debug logging
description: Use structured logging with object notation instead of string interpolation
  for debug messages to improve readability and provide better structured data. This
  approach makes logs more consistent and easier to parse, while also helping to consolidate
  related information into single log statements.
repository: cypress-io/cypress
label: Logging
language: Other
comments_count: 3
repository_stars: 48850
---

Use structured logging with object notation instead of string interpolation for debug messages to improve readability and provide better structured data. This approach makes logs more consistent and easier to parse, while also helping to consolidate related information into single log statements.

Instead of using string interpolation with multiple parameters:
```coffeescript
debug("plugins file %s is default, check if folder %s exists", pluginsFile, path.dirname(pluginsFile))
```

Use structured logging with objects:
```coffeescript
debug("checking if pluginsFile exists", { pluginsFile, dirName: path.dirname(pluginsFile) })
```

This format groups related data together, reduces the need for multiple debug statements, and makes the logs more readable. When possible, consolidate multiple related debug messages into fewer, more informative structured logs to avoid duplication across modules.