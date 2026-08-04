---
title: Optional Null Patterns
description: When a value is optional in Bicep, use **nullable parameter types** and
  **null-safe property emission** instead of sentinel values (like empty strings)
  or `json('null')`.
repository: Azure/azure-quickstart-templates
label: Null Handling
language: Other
comments_count: 6
repository_stars: 14846
---

When a value is optional in Bicep, use **nullable parameter types** and **null-safe property emission** instead of sentinel values (like empty strings) or `json('null')`.

Apply these rules:
1) **Make parameters nullable when they can be omitted**
```bicep
param addressPrefix string?
```
(or `param addressPrefix string = null` if your style prefers explicit defaults)

2) **For optional object fields, set the field to `null` (or omit the field)**
- Prefer field-level nulling:
```bicep
properties: {
  snssai: {
    sst: sst
    sd: empty(sd) ? null : sd
  }
}
```
- If the schema requires omitting entirely, conditionally build the object, but keep it consistent:
```bicep
properties:!empty(sd) ? {
  snssai: {
    sst: sst
    sd: sd
  }
} : {
  snssai: {
    sst: sst
  }
}
```

3) **Use native `null`, not `json('null')`**
```bicep
zones: (length(availabilityZones) == 0) ? null : availabilityZones
```

4) **Guard optional properties with `contains()` to avoid “property doesn’t exist” errors**
```bicep
properties: {
  nsgId: contains(subnet, 'nsgId') ? (empty(subnet.nsgId) ? null : subnet.nsgId) : null
}
```

Net effect: templates stay null-safe, avoid invalid payload fields, and reduce runtime/validation errors caused by missing properties or incorrect null representations.