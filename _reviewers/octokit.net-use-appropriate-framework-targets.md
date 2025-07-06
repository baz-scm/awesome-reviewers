---
title: Use appropriate framework targets
description: 'When configuring .NET projects, always use the correct target framework
  elements and versions:


  1. Use the singular `<TargetFramework>` element when targeting a single framework:'
repository: octokit/octokit.net
label: Configurations
language: Other
comments_count: 2
repository_stars: 2793
---

When configuring .NET projects, always use the correct target framework elements and versions:

1. Use the singular `<TargetFramework>` element when targeting a single framework:
```xml
<TargetFramework>netstandard2.0</TargetFramework>
```

2. Use the plural `<TargetFrameworks>` element only when targeting multiple frameworks:
```xml
<TargetFrameworks>netstandard2.0;net6.0</TargetFrameworks>
```

3. Always prefer Long Term Support (LTS) versions (like .NET 6) over non-LTS versions (like .NET 5) to ensure stability and longer support lifecycles. This reduces the frequency of required updates and provides more reliable runtime environments for production applications.