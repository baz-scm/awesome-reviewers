---
title: Maintain consistent style
description: 'Follow established patterns consistently throughout the codebase to
  improve readability and maintainability:


  1. **Use auto properties with appropriate access modifiers**:'
repository: octokit/octokit.net
label: Code Style
language: C#
comments_count: 7
repository_stars: 2793
---

Follow established patterns consistently throughout the codebase to improve readability and maintainability:

1. **Use auto properties with appropriate access modifiers**:
   - Prefer auto properties with private setters over readonly fields
   - Use private setters for properties set only in constructors
   ```csharp
   // Instead of:
   readonly string _title;
   
   // Prefer:
   public string Title { get; private set; }
   ```

2. **Follow constructor best practices**:
   - Required parameters only in constructors; use object initializers for optional values
   - Format parameterless constructors on a single line: `public ClassName() { }`
   - Ensure all properties are properly assigned in constructors

3. **Simplify code expressions**:
   - Prefer concise expressions over verbose alternatives
   ```csharp
   // Instead of:
   Assert.True(firstRefsPage.Where(x => secondRefsPage.Contains(x)).Any() == false);
   
   // Prefer:
   Assert.False(firstRefsPage.Any(x => secondRefsPage.Contains(x)));
   ```

4. **Be consistent with established patterns**:
   - Match the style used in surrounding code
   - Apply the same formatting rules throughout the project
   - Follow the project's conventions for organization and naming