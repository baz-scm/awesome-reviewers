---
title: Sanitize user input
description: "Always sanitize and validate user-controlled input before using it in\
  \ sensitive operations, and never hard-code credentials in source code. \n\n**For\
  \ command execution:**"
repository: n8n-io/n8n
label: Security
language: Python
comments_count: 2
repository_stars: 122978
---

Always sanitize and validate user-controlled input before using it in sensitive operations, and never hard-code credentials in source code. 

**For command execution:**
- User input should never be directly interpolated into shell commands
- Use parameter substitution libraries or sanitize inputs with allowlists
- Prefer higher-level APIs when available instead of raw shell commands

**For credential management:**
- Store credentials in environment variables or dedicated secret management systems
- Load credentials at runtime, not in source code
- Use different credentials for development and production environments

**Bad example (command injection vulnerability):**
```python
username = request.get_json().get('username')
os.system(f'docker compose -f {compose_file} -p n8n-{username} up -d')
```

**Better example:**
```python
import shlex
import subprocess

username = request.get_json().get('username')
# Validate username format with a strict pattern
if not re.match(r'^[a-zA-Z0-9_-]+$', username):
    return jsonify({'error': 'Invalid username format'}), 400

# Use subprocess with parameters list instead of shell=True
subprocess.run(['docker', 'compose', '-f', compose_file, '-p', f'n8n-{username}', 'up', '-d'])
```

**Bad example (credential management):**
```python
uri = "mongodb+srv://akaneai420:ilovehentai321@cluster0.jwyab3g.mongodb.net/?retryWrites=true"
```

**Better example:**
```python
# Load from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
uri = f"mongodb+srv://{db_user}:{db_password}@{db_host}/?retryWrites=true"
```

These practices help prevent both command injection attacks and credential leakage, which are common security vulnerabilities in web applications.