---
title: Keep actions versions current
description: 'Always use the latest stable versions of GitHub Actions components in
  CI/CD workflows to avoid deprecated features, security vulnerabilities, and compatibility
  issues. This includes:'
repository: chef/chef
label: CI/CD
language: Yaml
comments_count: 6
repository_stars: 7860
---

Always use the latest stable versions of GitHub Actions components in CI/CD workflows to avoid deprecated features, security vulnerabilities, and compatibility issues. This includes:

1. Use the latest version of common actions:
   ```yaml
   # Use this
   - uses: actions/checkout@v4
   
   # Instead of these older versions
   - uses: actions/checkout@v3
   - uses: actions/checkout@v2
   ```

2. Reference the canonical branch name in external actions:
   ```yaml
   # Use this
   - uses: actionshub/chef-install@main
   
   # Instead of
   - uses: actionshub/chef-install@master
   ```

3. Keep runner images updated to currently supported versions:
   ```yaml
   # Use these
   runs-on: macos-11  # or newer
   runs-on: windows-2022  # instead of windows-2016
   
   # Replace deprecated runners like
   # runs-on: macos-10.15
   # runs-on: windows-2016
   ```

Regular updates reduce security risks, ensure compatibility with GitHub's evolving infrastructure, and prevent build failures when older components are deprecated or removed. Create a recurring task to audit and update actions versions across your workflows.
