---
title: Externalize configuration values
description: Avoid hardcoding configuration values directly in scripts, especially
  for values that might change between environments or contain sensitive information.
  Instead, use environment variables, build parameters, or secrets management systems.
repository: chef/chef
label: Configurations
language: Shell
comments_count: 6
repository_stars: 7860
---

Avoid hardcoding configuration values directly in scripts, especially for values that might change between environments or contain sensitive information. Instead, use environment variables, build parameters, or secrets management systems.

Key practices:
1. Move endpoint URLs, license keys, and service addresses to environment variables
2. Maintain consistent naming conventions for environment variables across different scripts
3. Configure CI/CD systems to inject these values during build and deployment
4. Use default values only for development environments, never for production configurations

Example - Instead of:
```bash
export CHEF_LICENSE_SERVER="http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000"
```

Use:
```bash
export CHEF_LICENSE_SERVER="${CHEF_LICENSE_SERVER:-fallback_value_for_dev_only}"
```

Or configure the value in your CI/CD system's environment variables or secrets store.

For version information, prefer environment variables provided by your CI/CD system over reading from files:
```bash
# Preferred
VERSION="${EXPEDITOR_VERSION}"

# Avoid
VERSION=$(cat VERSION)
```
