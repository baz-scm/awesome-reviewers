---
name: validate-security-related-inputs-django
description: "Always validate and sanitize inputs that affect security features in Django to prevent vulnerabilities."
---

# Validate Security-Related Inputs (Django)

Django’s robust security can be undermined if developers assume the framework will handle all validation. This skill ensures that any input influencing security-sensitive logic is explicitly checked in code[40]:

- **Sanitize untrusted data.** Anytime user input is used in a security context (e.g., constructing queries, forming commands, or making decisions like permission checks), sanitize it. For instance, strip or escape dangerous characters. Django’s codebase shows patterns like replacing special characters in search queries to prevent injection[41].
- **Validate config values.** Security-related settings or parameters (like allowed hosts, CSP policies, feature flags) should be validated for type and range. Don’t just pass them through – if a setting is supposed to be a dict or a subset of options, check that and throw a clear error if it’s wrong[42][43].
- **Provide informative errors.** When rejecting bad input, error messages should help developers fix the issue without leaking sensitive info. For example, if a security header config is invalid, say why but do not expose any secret values in the message[42].
- **Early validation.** Do these checks as early as possible – ideally at the boundary of processing input (e.g., at form clean methods or view entry points) before any security-critical operation uses the data[44].

Examples from Django include escaping search queries used with Postgres full-text search to prevent malicious query operators[45], and validating that a weight parameter is one of allowed letters before using it[46]. By having reviewers enforce this, you catch potential XSS, SQL injection, or config mistakes early, keeping the application safe.
