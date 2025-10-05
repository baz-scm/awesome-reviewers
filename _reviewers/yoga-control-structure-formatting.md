---
title: Control structure formatting
description: Always use braces for control structures (if, for, while, etc.) even
  for single statements, and maintain consistent spacing around parentheses and braces.
  This improves code readability and prevents potential bugs when code is modified
  later.
repository: facebook/yoga
label: Code Style
language: Java
comments_count: 2
repository_stars: 18255
---

Always use braces for control structures (if, for, while, etc.) even for single statements, and maintain consistent spacing around parentheses and braces. This improves code readability and prevents potential bugs when code is modified later.

Use proper spacing with a space after the keyword and before the opening parenthesis, and place the opening brace on the same line with a space before it:

```java
// Good
if (attrs != null) {
    layoutParams = new LayoutParams(context, attrs);
}

// Avoid
if(attrs != null){
    layoutParams = new LayoutParams(context, attrs);
}

// Avoid (missing braces)
if (attrs != null)
    layoutParams = new LayoutParams(context, attrs);
```

This standard ensures consistent formatting across the codebase and makes code easier to read and maintain.