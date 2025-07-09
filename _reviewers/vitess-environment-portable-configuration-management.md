---
title: Environment-portable configuration management
description: 'Ensure all configurations are environment-portable and follow current
  best practices for the target platforms. This includes:


  1. Using environment variables instead of hardcoded paths or user-specific values'
repository: vitessio/vitess
label: Configurations
language: Other
comments_count: 4
repository_stars: 19815
---

Ensure all configurations are environment-portable and follow current best practices for the target platforms. This includes:

1. Using environment variables instead of hardcoded paths or user-specific values
2. Keeping base images and dependencies updated to supported versions
3. Adapting installation methods to platform-specific best practices
4. Verifying package availability across target environments

**Examples:**

Instead of:
```bash
rm -rf /Users/username/vtdataroot/*
```

Use:
```bash
rm -rf "${VTDATAROOT:-./vtdataroot}"/*
```

For Docker configurations, regularly review base images:
```dockerfile
# Review regularly to keep updated
FROM --platform=linux/amd64 golang:1.23.4-bookworm

# Research platform-specific installation methods
RUN echo "deb http://repo.mysql.com/apt/debian/ bookworm mysql-8.4-lts" > /etc/apt/sources.list.d/mysql.list
```

When packages change across OS versions, document and adapt:
```
# For bookworm, use these packages instead of the deprecated 'etcd'
apt-get install -y etcd-client etcd-server
```