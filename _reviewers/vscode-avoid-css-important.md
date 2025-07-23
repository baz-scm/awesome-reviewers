---
title: Avoid CSS !important
description: Using `!important` in CSS declarations should be avoided as it makes
  styles difficult to override and maintain. Instead, use more specific selectors
  to achieve the desired styling hierarchy. This improves code maintainability and
  follows CSS best practices.
repository: microsoft/vscode
label: Code Style
language: Css
comments_count: 3
repository_stars: 174887
---

Using `!important` in CSS declarations should be avoided as it makes styles difficult to override and maintain. Instead, use more specific selectors to achieve the desired styling hierarchy. This improves code maintainability and follows CSS best practices.

For example, instead of:
```css
.monaco-workbench .part.editor > .content .gettingStartedContainer .test-banner {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
  color: white !important;
}
```

Prefer using more specific selectors:
```css
.monaco-workbench .part.editor > .content .gettingStartedContainer .test-banner.special-banner {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  color: white;
}
```

This approach ensures styles can be more easily maintained, understood, and overridden when necessary without creating specificity wars in your stylesheets.