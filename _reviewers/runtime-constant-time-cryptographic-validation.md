---
title: Constant-time cryptographic validation
description: Always use constant-time comparison methods when validating cryptographic
  values to prevent timing side-channel attacks. Operations like comparing authentication
  tags, MACs, hashes, or any security-sensitive values should use dedicated APIs such
  as `CryptographicOperations.FixedTimeEquals()` rather than standard equality operators
  or methods.
repository: dotnet/runtime
label: Security
language: C#
comments_count: 1
repository_stars: 16578
---

Always use constant-time comparison methods when validating cryptographic values to prevent timing side-channel attacks. Operations like comparing authentication tags, MACs, hashes, or any security-sensitive values should use dedicated APIs such as `CryptographicOperations.FixedTimeEquals()` rather than standard equality operators or methods.

Example:
```csharp
// INSECURE: Vulnerable to timing attacks
if (header != 0xA65959A6UL)
    throw new CryptographicException();

// SECURE: Use constant-time comparison
uint err = (uint)(header) ^ 0xA65959A6U;
// Aggregate other validation results with bitwise OR
err |= pad & ~0x7;
// ...
if (err != 0)
    throw new CryptographicException();
```

For larger data structures or byte sequences:
```csharp
// INSECURE: String equality is not constant-time
if (computedTag == expectedTag)
    return true;

// SECURE: Use crypto-specific APIs
return CryptographicOperations.FixedTimeEquals(
    computedTag.AsSpan(), 
    expectedTag.AsSpan());
```

This practice is especially important for operations that verify authentication tags, decrypt ciphertexts, or validate signatures, where timing differences could reveal information about secret values to attackers.
