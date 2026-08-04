---
title: Validate Security Inputs
description: 'Apply security validation and gating at the boundaries of security-sensitive
  behavior:


  - Validate identifiers and API-version-like parameters during cmdlet/argument binding
  (e.g., GUIDs, strict date patterns) so malformed inputs can’t flow into authorization/resource
  construction.'
repository: Azure/azure-powershell
label: Security
language: C#
comments_count: 6
repository_stars: 4762
---

Apply security validation and gating at the boundaries of security-sensitive behavior:

- Validate identifiers and API-version-like parameters during cmdlet/argument binding (e.g., GUIDs, strict date patterns) so malformed inputs can’t flow into authorization/resource construction.
- Prevent file/path traversal by resolving to full paths and ensuring the resolved path remains within the intended destination directory.
- For security-token/header/pipeline features, only attach them to the intended request surface (avoid applying policy headers to data-plane endpoints) and ensure cross-region/security operations validate the target and preserve required auxiliary tokens—fail explicitly if prerequisites aren’t satisfied.

Example (input validation + path safety):
```csharp
using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;

[ValidateNotNullOrEmpty]
[ValidatePattern(@"^\d{4}-\d{2}-\d{2}$")] // YYYY-MM-DD
public string ScheduledEventsApiVersion { get; set; }

[ValidateNotNullOrEmpty]
public string ContainerSubscriptionId { get; set; } // validate as GUID in code during binding

public static bool IsFilePathWithinDirectory(string filePath, string destinationDirectory)
{
    if (string.IsNullOrEmpty(filePath) || string.IsNullOrEmpty(destinationDirectory)) return false;

    var fullDestinationDirectory = Path.GetFullPath(destinationDirectory);
    if (!fullDestinationDirectory.EndsWith(Path.DirectorySeparatorChar.ToString(), StringComparison.Ordinal) &&
        !fullDestinationDirectory.EndsWith(Path.AltDirectorySeparatorChar.ToString(), StringComparison.Ordinal))
    {
        fullDestinationDirectory += Path.DirectorySeparatorChar;
    }

    var fullFilePath = Path.GetFullPath(filePath);
    return fullFilePath.StartsWith(fullDestinationDirectory, StringComparison.Ordinal);
}
```

Operational rule of thumb: if a value or security credential is required for a protected operation, validate it early and explicitly gate the security side-effect to the correct target; never rely on downstream service failures to enforce safety.