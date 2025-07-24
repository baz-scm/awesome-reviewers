---
title: API parameter extensibility
description: Design APIs to support multiple parameters from the beginning rather
  than limiting them to single parameter inputs. This prevents future refactoring
  needs and provides better extensibility for complex operations.
repository: argoproj/argo-cd
label: API
language: TSX
comments_count: 2
repository_stars: 20149
---

Design APIs to support multiple parameters from the beginning rather than limiting them to single parameter inputs. This prevents future refactoring needs and provides better extensibility for complex operations.

When designing resource action APIs or similar interfaces, structure them to accept parameter collections rather than single values. Instead of hardcoding single parameter handling:

```typescript
// Avoid: Limited to single parameter
const resourceActionParameters = action.hasParameters ? 
    [{name: action.name, value: vals.inputParameter}] : [];
```

Design for multiple parameters using parameter mapping:

```typescript
// Preferred: Support multiple parameters
const resourceActionParameters = action.params
    ? action.params.map(param => ({
           name: param.name,
           value: vals[param.name] || param.default,
           type: param.type,
           default: param.default
       }))
    : [];
```

This approach allows APIs to evolve naturally as requirements grow, supports complex operations that need multiple inputs, and provides a consistent interface pattern across different API endpoints. Consider the parameter structure in your API specification from the start, even if initially only one parameter is needed.