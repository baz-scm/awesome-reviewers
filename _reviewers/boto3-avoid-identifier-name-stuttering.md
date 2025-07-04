---
title: Avoid identifier name stuttering
description: Do not repeat the resource name in identifier names. This form of stuttering
  makes code less readable and inconsistent. Instead, use simple, descriptive identifiers
  without redundancy.
repository: boto/boto3
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 9417
---

Do not repeat the resource name in identifier names. This form of stuttering makes code less readable and inconsistent. Instead, use simple, descriptive identifiers without redundancy.

For example:
- Use `Id` instead of `VpnGatewayId` for a VpnGateway resource
- Use `Name` instead of `ReportName` for a ReportDefinition resource

When necessary, include a `memberName` attribute to map the simplified identifier to the actual API field name:

```json
"identifiers": [
  { 
    "name": "Id", 
    "memberName": "VpnGatewayId"
  }
]
```

This approach creates more concise and consistent identifiers throughout the codebase while maintaining the correct mapping to external API representations.