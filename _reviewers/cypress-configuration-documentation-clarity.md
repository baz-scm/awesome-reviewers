---
title: Configuration documentation clarity
description: Ensure configuration documentation, setup instructions, and changelogs
  use precise, clear language with proper technical terminology. Avoid ambiguous words
  like "sometimes" or "generally" that create uncertainty. Use correct capitalization
  for technical terms (e.g., "Node.js" not "Node", "CommonJS/ESM" not "commonjs/ESM").
  Remove redundant words and fix...
repository: cypress-io/cypress
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 48850
---

Ensure configuration documentation, setup instructions, and changelogs use precise, clear language with proper technical terminology. Avoid ambiguous words like "sometimes" or "generally" that create uncertainty. Use correct capitalization for technical terms (e.g., "Node.js" not "Node", "CommonJS/ESM" not "commonjs/ESM"). Remove redundant words and fix grammatical errors that can confuse users.

Examples of improvements:
- "be default" → "by default"
- "Node for commonjs/ESM" → "Node.js for CommonJS/ESM" 
- "Sometimes, when using nvm..." → "When using nvm..."
- "no longer be supported" → "no longer supported"

Configuration documentation should provide definitive, tested instructions rather than vague guidance, as users rely on this information to set up their development environments correctly.