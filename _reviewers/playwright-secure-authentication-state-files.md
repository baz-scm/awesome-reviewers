---
title: Secure authentication state files
description: Authentication state files (such as browser session files, cookies, or
  tokens) contain sensitive credentials that can lead to full account takeover if
  exposed. These files must never be committed to version control systems as they
  could be used to impersonate users or test accounts.
repository: microsoft/playwright
label: Security
language: Markdown
comments_count: 2
repository_stars: 76113
---

Authentication state files (such as browser session files, cookies, or tokens) contain sensitive credentials that can lead to full account takeover if exposed. These files must never be committed to version control systems as they could be used to impersonate users or test accounts.

**Prevention strategies:**
1. **Use .gitignore**: Add authentication directories to your `.gitignore` file and store files in dedicated directories like `playwright/.auth/`
2. **External storage**: Store sensitive files outside the project directory using temporary directories

**Example implementation:**
```javascript
// Option 1: Secure directory with .gitignore
{
  name: 'firefox',
  use: {
    storageState: 'playwright/.auth/user.json', // Add playwright/.auth to .gitignore
  },
}

// Option 2: Temporary directory (safer)
{
  name: 'firefox', 
  use: {
    storageState: `${mkdirtemp()}/playwright/.auth/user.json`,
  },
}
```

Always verify that authentication state files are properly excluded from version control and build artifacts to prevent credential exposure.