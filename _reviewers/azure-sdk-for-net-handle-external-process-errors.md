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


[
  {
    "discussion_id": "2139151065",
    "pr_number": 50539,
    "pr_file": "eng/scripts/Language-Settings.ps1",
    "created_at": "2025-06-11T04:08:56+00:00",
    "commented_code": "# Save-Package-Properties.ps1\n  $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n  $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"\n  \n  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion /p:OutputProjectInfoListFilePath=\"\"$outputFilePath\"\" -tl:off\"\n\n  $msbuildOutput = dotnet msbuild `",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2139151065",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139151065",
        "commented_code": "@@ -16,17 +16,27 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"\n+  \n+  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion /p:OutputProjectInfoListFilePath=\"\"$outputFilePath\"\" -tl:off\"\n \n   $msbuildOutput = dotnet msbuild `",
        "comment_created_at": "2025-06-11T04:08:56+00:00",
        "comment_author": "weshaggard",
        "comment_body": "@copilot please remove the $msbuildOutput variable as it is no longer used. Also add error handling to fail if this msbuild call fails. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2139154406",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139151065",
        "commented_code": "@@ -16,17 +16,27 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"\n+  \n+  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion /p:OutputProjectInfoListFilePath=\"\"$outputFilePath\"\" -tl:off\"\n \n   $msbuildOutput = dotnet msbuild `",
        "comment_created_at": "2025-06-11T04:13:10+00:00",
        "comment_author": "Copilot",
        "comment_body": "Removed the unused $msbuildOutput variable and added error handling to fail if msbuild call fails. The script now throws an exception with the exit code when msbuild fails and properly cleans up the temporary file. Commit: 48ab62b",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2139217607",
    "pr_number": 50539,
    "pr_file": "eng/scripts/Language-Settings.ps1",
    "created_at": "2025-06-11T05:18:29+00:00",
    "commented_code": "# Save-Package-Properties.ps1\n  $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n  $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2139217607",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T05:18:29+00:00",
        "comment_author": "weshaggard",
        "comment_body": "@copilot this function is somehow causing an empty string to be added to the returned array of objects. What change do you think caused it to add an empty string to the object pipeline?",
        "pr_file_module": null
      },
      {
        "comment_id": "2139228464",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T05:23:46+00:00",
        "comment_author": "Copilot",
        "comment_body": "The issue was caused by `Get-Content` returning empty lines from the file, which were then included in the returned array. Fixed by filtering out empty or whitespace-only lines when reading the package info file: `Get-Content $outputFilePath | Where-Object { $_ -and $_.Trim() }`. Commit: a8e609f",
        "pr_file_module": null
      },
      {
        "comment_id": "2139233160",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T05:26:44+00:00",
        "comment_author": "weshaggard",
        "comment_body": "I don't think that is the error because the loop skips any lines that are empty and do not parse correctly. There must be some other part of this function that is writing to the powershell object pipeline. Does the msbuild call or the remove-item return an object that could be an empty string?\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2139238868",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T05:30:39+00:00",
        "comment_author": "Copilot",
        "comment_body": "You're absolutely right! The issue was that the `dotnet msbuild` command on lines 23-30 wasn't being captured, so its output was going to the PowerShell object pipeline and being included in the function's return value. Fixed by assigning the command output to `$null` to prevent it from polluting the pipeline. Also captured the `Remove-Item` commands for consistency. Commit: c5293f3",
        "pr_file_module": null
      },
      {
        "comment_id": "2140451115",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T15:09:23+00:00",
        "comment_author": "weshaggard",
        "comment_body": "@copilot If we assign the dotnet msbuild command output to $null how will we see the errors that come out of that command if there are any?",
        "pr_file_module": null
      },
      {
        "comment_id": "2140461456",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/scripts/Language-Settings.ps1",
        "discussion_id": "2139217607",
        "commented_code": "@@ -16,22 +16,41 @@ function Get-AllPackageInfoFromRepo($serviceDirectory)\n   # Save-Package-Properties.ps1\n   $shouldAddDevVersion = Get-Variable -Name 'addDevVersion' -ValueOnly -ErrorAction 'Ignore'\n   $ServiceProj = Join-Path -Path $EngDir -ChildPath \"service.proj\"\n-  Write-Host \"dotnet msbuild /nologo /t:GetPackageInfo \"\"$ServiceProj\"\" /p:ServiceDirectory=$serviceDirectory /p:AddDevVersion=$shouldAddDevVersion -tl:off\"\n+  $outputFilePath = Join-Path ([System.IO.Path]::GetTempPath()) \"package-info-$([System.Guid]::NewGuid()).txt\"",
        "comment_created_at": "2025-06-11T15:14:11+00:00",
        "comment_author": "Copilot",
        "comment_body": "You're absolutely right! I've changed the approach to use `Out-Host` instead of assigning to `$null`. This way, all msbuild output (including error messages) is displayed to users, but it doesn't pollute the PowerShell object pipeline. The error handling via `$LASTEXITCODE` still works correctly. Commit: 6d6ed17",
        "pr_file_module": null
      }
    ]
  }
]
