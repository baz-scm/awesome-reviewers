---
title: document security-sensitive features
description: When introducing compatibility flags, feature toggles, or APIs that have
  security implications, use self-documenting names that explicitly warn about risks
  and provide comprehensive documentation explaining the security concerns.
repository: cloudflare/workerd
label: Security
language: Other
comments_count: 3
repository_stars: 6989
---

When introducing compatibility flags, feature toggles, or APIs that have security implications, use self-documenting names that explicitly warn about risks and provide comprehensive documentation explaining the security concerns.

Feature names should include descriptive terms like "insecure", "unsafe", or specific risk indicators. For example, use `allow_insecure_inefficient_logged_eval` instead of just `allow_eval` to immediately signal to developers that this feature carries security risks.

Documentation should clearly explain:
- What security risks the feature introduces
- Why the feature exists despite the risks
- When it's appropriate to use (if ever)
- What precautions developers must take

Example from compatibility flags:
```cpp
experimentalAllowEvalAlways @113 :Bool
    $compatEnableFlag("allow_insecure_inefficient_logged_eval")
// Comment should explain:
// * insecure: Disastrous for security if eval content is attacker-controlled
// * inefficient: Poor fit for Workers architecture with many instances  
// * logged: Code passed to eval() will be logged for forensics
```

This approach helps prevent security vulnerabilities by making risks explicit and ensuring developers make informed decisions rather than accidentally enabling dangerous features.