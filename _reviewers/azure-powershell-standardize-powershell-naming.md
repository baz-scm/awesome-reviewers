---
title: Standardize PowerShell Naming
description: 'Apply consistent, semantic naming to generated cmdlets, parameters,
  and help/docs.


  - Cmdlet verb semantics: name sync operations with `Invoke-*` rather than `Start-*`/job-style
  verbs.'
repository: Azure/azure-powershell
label: Naming Conventions
language: Markdown
comments_count: 11
repository_stars: 4762
---

Apply consistent, semantic naming to generated cmdlets, parameters, and help/docs.

- Cmdlet verb semantics: name sync operations with `Invoke-*` rather than `Start-*`/job-style verbs.
  - Example: if an operation is synchronous, prefer `Invoke-AzNetworkCloudStorageApplianceReadCommand` over `Start-*`.

- Parameter readability: avoid overly hierarchical/verbose parameter names produced by AutoRest (e.g., `InvitedUserDetailAuthType`). Use AutoRest’s parameter rename directive to shorten/clarify names.
  - Also validate directive fields (e.g., use `verb`, not `werb`).

- Keep help/docs type references aligned with the current generator: after migrating (e.g., AutoRest v4), update output type namespaces to the expected flat model types (e.g., `Models.IFileSystemResource` instead of `Models.Api20221012Preview.IFileSystemResource`).

- Be conservative with generation directives that affect cmdlet naming: follow established cmdlet pairing patterns (e.g., `Set`/`New` typically map to the same PUT API) unless you have a clear, verified reason to change generation behavior.

These checks prevent misleading cmdlet names, awkward parameter UX, and incorrect documentation/type references when the generator or swagger surface changes.