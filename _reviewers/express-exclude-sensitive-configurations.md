---
title: Exclude sensitive configurations
description: 'Do not commit sensitive, time-limited, or environment-specific configuration
  files to version control. Instead:


  1. For files with expiration dates (like SSL certificates):'
repository: expressjs/express
label: Configurations
language: Other
comments_count: 2
repository_stars: 67300
---

Do not commit sensitive, time-limited, or environment-specific configuration files to version control. Instead:

1. For files with expiration dates (like SSL certificates):
   - Provide clear generation instructions in documentation
   - Consider using auto-generation tools or modules
   - Add these files to .gitignore

2. For environment-specific configurations:
   - Use template files with placeholders (e.g., config.example.js)
   - Document the required configuration parameters
   - Ensure all sensitive files are in .gitignore

Example of proper .gitignore usage:
```
# npm
node_modules
package-lock.json
npm-shrinkwrap.json

# Security
*.pem
*.key
*.crt
```

Example of documentation in README.md:
```markdown
## Setup
Before running the example, generate the required SSL certificates:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
```