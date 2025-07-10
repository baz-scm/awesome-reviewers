---
title: Escape untrusted input
description: Always use appropriate escaping mechanisms when handling input from untrusted
  sources to prevent injection attacks. User-provided data that contains special characters
  or operators can be interpreted in unintended ways if not properly escaped, leading
  to security vulnerabilities like XSS, SQL injection, or command injection.
repository: django/django
label: Security
language: Txt
comments_count: 1
repository_stars: 84182
---

Always use appropriate escaping mechanisms when handling input from untrusted sources to prevent injection attacks. User-provided data that contains special characters or operators can be interpreted in unintended ways if not properly escaped, leading to security vulnerabilities like XSS, SQL injection, or command injection.

For example, when working with search functionality where user input might contain special operators:

```python
# Unsafe approach - user could inject search operators
query = request.GET.get('q')
results = Entry.objects.filter(search_vector=query)  # Vulnerable to injection

# Secure approach using Lexeme objects to escape special characters
from django.contrib.postgres.search import SearchQuery, Lexeme
query = request.GET.get('q')
search_query = SearchQuery(Lexeme(query))  # Operators in the query string are escaped
results = Entry.objects.filter(search_vector=search_query)
```

Similarly, use appropriate escaping mechanisms in other contexts:
- HTML: Use template systems with auto-escaping or dedicated HTML escaping functions
- SQL: Use parameterized queries or ORM methods that handle escaping
- Command execution: Avoid shell=True with subprocess and validate all inputs
- URL parameters: Use proper URL encoding functions

The principle applies to any situation where user input is incorporated into operations that interpret special characters. When in doubt, assume all external input is potentially malicious and apply context-appropriate escaping.