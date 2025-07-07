---
title: Secure infrastructure maintenance
description: 'Maintain CI/CD infrastructure with security and currency as top priorities.
  This includes:


  1. **Keep build tools updated**: Always use the latest stable versions of build
  tools and dependencies in CI/CD environments to benefit from bug fixes, security
  updates, and improved features.'
repository: tensorflow/tensorflow
label: CI/CD
language: Dockerfile
comments_count: 2
repository_stars: 190625
---

Maintain CI/CD infrastructure with security and currency as top priorities. This includes:

1. **Keep build tools updated**: Always use the latest stable versions of build tools and dependencies in CI/CD environments to benefit from bug fixes, security updates, and improved features.

2. **Never bypass security measures**: Security controls like package signature verification are essential and should never be disabled for convenience.

Example from Discussion 1:
```dockerfile
# GOOD: Keep signature verification enabled
# Install packages securely
RUN C:\tools\msys64\usr\bin\bash.exe -lc 'pacman --noconfirm -Syy git curl zip unzip patch'

# BAD: Don't disable signature verification
# RUN Add-Content -Path C:\tools\msys64\etc\pacman.d\mirrorlist.mingw32 -Value 'SigLevel = Never'
# RUN Add-Content -Path C:\tools\msys64\etc\pacman.d\mirrorlist.mingw64 -Value 'SigLevel = Never'
# RUN Add-Content -Path C:\tools\msys64\etc\pacman.d\mirrorlist.msys -Value 'SigLevel = Never'
```

Example from Discussion 0:
```dockerfile
# GOOD: Use recent versions of build tools
RUN (New-Object Net.WebClient).DownloadFile(
         'https://github.com/bazelbuild/bazelisk/releases/download/v1.16.0/bazelisk-windows-amd64.exe',
         'C:\tools\bazel\bazel.exe')

# BAD: Don't use outdated versions
# RUN (New-Object Net.WebClient).DownloadFile(
#         'https://github.com/bazelbuild/bazelisk/releases/download/v1.11.0/bazelisk-windows-amd64.exe',
#         'C:\tools\bazel\bazel.exe')
```

Regularly audit build environments to ensure they remain secure and up-to-date. Document version update procedures to make maintenance easier for the team.