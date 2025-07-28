---
title: avoid interactive authentication automation
description: When building scripts or applications that require user authentication,
  avoid automating interactive authentication processes that could cause system instability
  or security issues. Instead, check authentication status programmatically and delegate
  the actual authentication to the user.
repository: cline/cline
label: Security
language: JavaScript
comments_count: 1
repository_stars: 48299
---

When building scripts or applications that require user authentication, avoid automating interactive authentication processes that could cause system instability or security issues. Instead, check authentication status programmatically and delegate the actual authentication to the user.

Interactive authentication commands (like login flows) can cause console freezing, unpredictable behavior, or security vulnerabilities when executed programmatically. The safer approach is to verify authentication status and provide clear instructions for users to authenticate themselves.

Example implementation:
```javascript
const checkGitHubAuth = async () => {
	try {
		execSync("gh auth status", { stdio: "ignore" })
		return true
	} catch (err) {
		console.log("\nGitHub authentication required.")
		console.log("\nPlease run the following command in your terminal to authenticate:")
		console.log("\n  gh auth login\n")
		return false
	}
}
```

This approach maintains security boundaries, prevents system issues, and ensures users maintain control over their authentication credentials while still enabling automated workflows to function properly.