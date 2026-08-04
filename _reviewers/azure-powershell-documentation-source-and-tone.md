---
title: Documentation Source And Tone
description: When updating documentation (assembly metadata, cmdlet HelpMessage, generated
  stubs, etc.), ensure (1) you change the correct source of truth and (2) the text
  is written for users, not for internal implementation.
repository: Azure/azure-powershell
label: Documentation
language: C#
comments_count: 2
repository_stars: 4762
---

When updating documentation (assembly metadata, cmdlet HelpMessage, generated stubs, etc.), ensure (1) you change the correct source of truth and (2) the text is written for users, not for internal implementation.

- Do not manually edit files that are generated during build (e.g., doc/help/example/test stubs). Instead, update the autorest/custom source inputs/config so regenerated outputs are correct.
- In public help/API documentation, describe the observable behavior, not internal transport details (e.g., avoid mentioning the underlying HTTP method like “POST”).

Example (cmdlet HelpMessage):
```csharp
[Parameter(Mandatory = false,
    HelpMessage = "If specified, retrieves the WhatIf result with resource property changes populated.")]
public SwitchParameter WithPropertyChanges { get; set; }
```

If you need to adjust wording for generated artifacts, update the generation inputs (autorest custom folder/README configuration) rather than the generated output files, so the next build doesn’t undo your changes.