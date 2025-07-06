---
title: File-specific indentation standards
description: Maintain consistent indentation based on file type to ensure code readability
  and prevent unwanted whitespace changes in PRs. Use 4 spaces for C# (.cs) files
  and 2 spaces for configuration files (like JSON, devcontainer files).
repository: octokit/octokit.net
label: Code Style
language: Json
comments_count: 2
repository_stars: 2793
---

Maintain consistent indentation based on file type to ensure code readability and prevent unwanted whitespace changes in PRs. Use 4 spaces for C# (.cs) files and 2 spaces for configuration files (like JSON, devcontainer files).

Example for C# files:
```csharp
public class Example 
{
    public void Method() 
    {
        if (condition) 
        {
            DoSomething();
        }
    }
}
```

Example for configuration files:
```json
{
  "name": "Project",
  "settings": {
    "editor.tabSize": 4,
    "editor.insertSpaces": true
  }
}
```

When working in different editors, ensure your editor settings reflect these standards. Configure IDE settings on a per-language basis (e.g., in VSCode settings.json) to automatically apply the correct indentation for each file type. This prevents accidental reformatting and maintains consistency throughout the codebase.