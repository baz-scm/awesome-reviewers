---
title: Documentation quality standards
description: Ensure all documentation comments follow proper formatting conventions
  and are placed where developers will most likely read them. Documentation should
  use correct grammar, complete sentences, and end with periods. Additionally, place
  documentation at the most relevant location - typically at interface definitions
  rather than implementation details, since...
repository: golang/go
label: Documentation
language: Go
comments_count: 2
repository_stars: 129599
---

Ensure all documentation comments follow proper formatting conventions and are placed where developers will most likely read them. Documentation should use correct grammar, complete sentences, and end with periods. Additionally, place documentation at the most relevant location - typically at interface definitions rather than implementation details, since developers read interface documentation when implementing methods.

Example of proper formatting:
```go
// ErrTimeout is a fake timeout error.
var ErrTimeout = errors.New("timeout")
```

Example of proper placement:
Place WriteTo documentation at the WriterTo interface definition, not at Copy function implementation, because developers implementing WriteTo will read the interface documentation, not the Copy function documentation.