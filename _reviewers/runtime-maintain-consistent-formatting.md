---
title: Maintain consistent formatting
description: 'Ensure consistent formatting and organization throughout the codebase
  to improve readability and maintainability. This includes:


  1. **Consistent spacing and alignment**'
repository: dotnet/runtime
label: Code Style
language: Other
comments_count: 4
repository_stars: 16578
---

Ensure consistent formatting and organization throughout the codebase to improve readability and maintainability. This includes:

1. **Consistent spacing and alignment**
   - Avoid spaces before commas or parentheses
   - Use consistent indentation and alignment within similar code blocks
   - Be explicit about whitespace rules when exceptions are needed

2. **Logical organization of related elements**
   - Group related functionality together (e.g., instructions of the same type)
   - Sort lists and collections in a logical order (alphabetical, numerical, etc.)

3. **Consistent use of delimiters and separators**
   - Follow project conventions for spacing around operators and separators

**Examples:**

Instead of inconsistent spacing in macro definitions:
```c
#define s390_trap2(code)                S390_E(code, 0x01ff)
#define s390_vab(c , v1, v2, v3)        S390_VRRc(c, 0xe7f3, v1, v2, v3, 0, 0, 0)
```

Use consistent spacing:
```c
#define s390_trap2(code)		S390_E(code, 0x01ff)
#define s390_vab(c, v1, v2, v3)		S390_VRRc(c, 0xe7f3, v1, v2, v3, 0, 0, 0)
```

For ordered lists like package sources, maintain logical ordering:
```xml
<add key="darc-pub-dotnet-emsdk-b567cdb-1" value="..." />
<add key="darc-pub-dotnet-emsdk-b567cdb-2" value="..." />
```

When formatting rules must be violated, document the exception:
```xml
<!-- SA1001: Commas should not be preceded by a whitespace; needed due to ifdef -->
<NoWarn>$(NoWarn);SA1001</NoWarn>
```

For grouping related elements, keep them together:
```c
#define FIRST_AVXVNNIINT8_INSTRUCTION INS_vpdpwsud
// Group all AVXVNNI instructions together rather than spreading them
// throughout different sections
```
