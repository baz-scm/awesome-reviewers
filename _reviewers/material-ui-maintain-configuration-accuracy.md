---
title: Maintain configuration accuracy
description: Regularly audit configuration files to remove unused entries and ensure
  all configurations accurately reflect the project's requirements and intended functionality.
  When modifying configuration files, carefully consider the purpose of each entry
  and verify that changes align with the desired behavior.
repository: mui/material-ui
label: Configurations
language: Json
comments_count: 3
repository_stars: 96063
---

Regularly audit configuration files to remove unused entries and ensure all configurations accurately reflect the project's requirements and intended functionality. When modifying configuration files, carefully consider the purpose of each entry and verify that changes align with the desired behavior.

Examples:
1. Remove unused dependencies from package.json files:
   ```diff
   "devDependencies": {
   -  "@eslint/js": "^9.21.0",
   -  "eslint": "^9.21.0",
   -  "eslint-plugin-react-hooks": "^5.0.0",
   -  "eslint-plugin-react-refresh": "^0.4.19",
   -  "globals": "^15.15.0",
     "typescript": "~5.7.2",
   ```

2. Verify that dependency declarations accurately reflect actual requirements:
   ```diff
   "peerDependencies": {
   -  "@mui/material": "^5.0.0",
   +  "@mui/system": "^5.11.2",
   +  "@emotion/react": "^11.5.0",
   ```

3. When modifying configuration entries, ensure changes align with their intended purpose:
   ```diff
   {
     "groupName": "node",
   -  "matchPackageNames": ["node"],
   +  "matchPackageNames": ["node", "cimg/node", "actions/setup-node"],
   ```

By maintaining accurate configurations, you reduce technical debt, prevent unexpected behavior, and make the codebase easier to maintain over time.