---
title: Extract reusable logic
description: Avoid duplicating logic across the codebase. Instead, extract common
  functionality into well-named helper functions or standalone utilities. This improves
  code readability, simplifies maintenance, and centralizes logic for easier updates.
repository: openai/codex
label: Code Style
language: TSX
comments_count: 3
repository_stars: 31275
---

Avoid duplicating logic across the codebase. Instead, extract common functionality into well-named helper functions or standalone utilities. This improves code readability, simplifies maintenance, and centralizes logic for easier updates.

Examples where this applies:
- Login flows that appear in multiple code branches
- Notification logic embedded within UI components
- Utility functions that perform specific tasks (like generating summaries)

**Before:**
```javascript
if (provider.toLowerCase() === "githubcopilot" && !apiKey) {
  apiKey = await fetchGithubCopilotApiKey();
  // Additional logic for handling the API key...
} else if (cli.flags.login) {
  if (provider.toLowerCase() === "githubcopilot") {
    apiKey = await fetchGithubCopilotApiKey();
    // Duplicate logic...
  }
}
```

**After:**
```javascript
function handleGithubCopilotLogin() {
  // Centralized login logic
}

if (provider.toLowerCase() === "githubcopilot" && !apiKey) {
  apiKey = await handleGithubCopilotLogin();
} else if (cli.flags.login) {
  if (provider.toLowerCase() === "githubcopilot") {
    apiKey = await handleGithubCopilotLogin();
  }
}
```