---
title: Validate configuration formatting
description: 'Ensure all JSON configuration files adhere to proper syntax and formatting
  conventions. Common issues to avoid include:


  1. **Invalid key-value syntax**: All JSON properties must use proper key-value format
  with double-quoted keys.'
repository: appwrite/appwrite
label: Code Style
language: Json
comments_count: 3
repository_stars: 51959
---

Ensure all JSON configuration files adhere to proper syntax and formatting conventions. Common issues to avoid include:

1. **Invalid key-value syntax**: All JSON properties must use proper key-value format with double-quoted keys.
   ```diff
   // Incorrect
   -  hi am sairam
   
   // Correct
   +  "message": "hi am sairam",
   ```

   ```

Run a JSON validator on configuration files before committing changes to catch these issues early. Proper JSON formatting ensures reliable parsing, prevents runtime errors, and maintains code consistency across the project.
