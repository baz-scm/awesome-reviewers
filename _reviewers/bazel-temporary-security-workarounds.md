---
title: temporary security workarounds
description: When implementing workarounds for OS-level security restrictions, ensure
  they are explicitly temporary and include clear plans for proper long-term solutions.
  Avoid recommending users bypass security features through unofficial methods, and
  instead guide them toward sanctioned approaches when possible.
repository: bazelbuild/bazel
label: Security
language: Java
comments_count: 1
repository_stars: 24489
---

When implementing workarounds for OS-level security restrictions, ensure they are explicitly temporary and include clear plans for proper long-term solutions. Avoid recommending users bypass security features through unofficial methods, and instead guide them toward sanctioned approaches when possible.

Security restrictions evolve over time, and workarounds that function today may break in future system updates. Code should detect the specific security context and implement fallbacks gracefully, while documenting the temporary nature of any bypasses.

Example approach:
```java
// Temporary workaround for Ubuntu 24.04 AppArmor restrictions
// TODO: Remove when proper allowlisting mechanism is available
if (stderr.lines().anyMatch(line -> line.endsWith(": \"mount\": Permission denied"))) {
  try {
    runBinTrue(cmdEnv, linuxSandbox, /* wrapInBusybox= */ true);
    return SupportLevel.SUPPORTED_VIA_BUSYBOX;
  } catch (CommandException e2) {
    // Provide guidance for sanctioned solutions rather than workarounds
    cmdEnv.getReporter().handle(Event.warn(
        "linux-sandbox failed due to security restrictions. " +
        "Consider using sanctioned methods to configure permissions."));
  }
}
```

The goal is to maintain functionality while respecting the intent of security measures and preparing for their proper implementation.