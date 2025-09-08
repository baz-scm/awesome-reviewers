---
title: Minimize authentication complexity
description: Avoid implementing redundant authentication steps when secure, direct
  methods are already available. Multiple authentication layers can introduce unnecessary
  complexity and potential security vulnerabilities. When identity files or tokens
  are already being used, evaluate whether additional login steps are truly required.
repository: gravitational/teleport
label: Security
language: Yaml
comments_count: 1
repository_stars: 19109
---

Avoid implementing redundant authentication steps when secure, direct methods are already available. Multiple authentication layers can introduce unnecessary complexity and potential security vulnerabilities. When identity files or tokens are already being used, evaluate whether additional login steps are truly required.

For example, if you're already using an identity file from a trusted source like tbot, avoid adding unnecessary login commands:

```bash
# Avoid this - redundant authentication
tsh login --proxy=${PROXY} -i /identity-output/identity
tctl create --identity=/identity-output/identity resource.yaml

# Prefer this - direct identity file usage
tctl create --identity=/identity-output/identity resource.yaml
```

Before adding authentication steps, ask: "Is this authentication method necessary given the existing secure credentials?" Simpler authentication flows are often more secure and less prone to configuration errors.