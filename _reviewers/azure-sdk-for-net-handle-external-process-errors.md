---
title: Handle external process errors
description: 'When calling external processes (like dotnet, msbuild, etc.), always
  implement proper error handling and output management:


  1. Check exit codes to detect failures and propagate errors'
repository: Azure/azure-sdk-for-net
label: Error Handling
language: Other
comments_count: 2
repository_stars: 5809
---

When calling external processes (like dotnet, msbuild, etc.), always implement proper error handling and output management:

1. Check exit codes to detect failures and propagate errors
2. Display command output to users for visibility
3. Prevent command output from polluting the PowerShell pipeline
4. Ensure proper cleanup of resources even when errors occur

```powershell
# Bad practice - no error handling, output pollutes pipeline
dotnet msbuild $ServiceProj /p:ServiceDirectory=$serviceDirectory

# Good practice - handles errors, displays output, doesn't pollute pipeline
$outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) "temp-$([System.Guid]::NewGuid()).txt"
try {
    # Display output but don't pollute pipeline
    dotnet msbuild $ServiceProj /p:ServiceDirectory=$serviceDirectory | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "MSBuild failed with exit code $LASTEXITCODE"
    }
    # Process results...
}
finally {
    # Clean up resources even if an error occurred
    if (Test-Path $outputFilePath) {
        Remove-Item -Path $outputFilePath -Force | Out-Host
    }
}
```

This approach ensures scripts fail fast when external processes fail, preserves error visibility, maintains clean function return values, and properly manages resources.
