---
title: Follow formatting standards
description: 'Maintain consistent code formatting by adhering to the defined standards
  in the .editorconfig file and Azure SDK implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html.
  Pay attention to these specific formatting rules:'
repository: Azure/azure-sdk-for-net
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 5809
---

Maintain consistent code formatting by adhering to the defined standards in the .editorconfig file and Azure SDK implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html. Pay attention to these specific formatting rules:

1. Avoid trailing whitespace at the end of lines
2. In tests, do not emit "Act", "Arrange", or "Assert" comments
3. When including code examples in documentation (like README files), ensure they are mirrored in corresponding test files with proper conditional compilation:

```csharp
#if SNIPPET
// Code snippet that appears in README
[DllImport("user32.dll")]
static extern IntPtr GetForegroundWindow();
#endif
```

4. Use correct casing, grammar, and formatting in changelog entries:
   - Use sentence case for the first word (capitalize first letter)
   - Be specific and clear about changes (e.g., "Changed `public IList<string>` to `public IReadOnlyList<string>`")

Consistent formatting improves readability, simplifies code reviews, and helps maintain a professional codebase.
