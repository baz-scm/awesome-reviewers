---
title: Accessible security indicators
description: Ensure all security-related UI elements such as warnings, error messages,
  and destructive action buttons meet WCAG contrast standards. Poor contrast in these
  elements creates an accessibility issue that can prevent users from noticing important
  security warnings or destructive actions, potentially leading to security vulnerabilities.
repository: shadcn-ui/ui
label: Security
language: Css
comments_count: 1
repository_stars: 90568
---

Ensure all security-related UI elements such as warnings, error messages, and destructive action buttons meet WCAG contrast standards. Poor contrast in these elements creates an accessibility issue that can prevent users from noticing important security warnings or destructive actions, potentially leading to security vulnerabilities.

Before implementing color changes, verify contrast ratios using tools like WebAIM's contrast checker (https://webaim.org/resources/contrastchecker/).

Example:
```css
/* GOOD: Verified accessible destructive color */
:root {
  --destructive: 0 72.8% 47%;
  --destructive-foreground: 210 20% 98%; /* Ensure this has sufficient contrast with destructive */
}

/* Before committing color changes, add a comment confirming accessibility */
/* Contrast ratio verified: 4.6:1 against white background, passes WCAG AA */
```