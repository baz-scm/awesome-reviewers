---
title: Use secure hash functions
description: When hashing sensitive data such as authentication tokens, always use
  cryptographically secure hash functions like SHA-256 instead of faster but insecure
  alternatives like MD5 or CRC32. Secure hash functions provide protection against
  reverse engineering and rainbow table attacks, which is critical for maintaining
  the confidentiality of sensitive...
repository: snyk/cli
label: Security
language: Go
comments_count: 1
repository_stars: 5178
---

When hashing sensitive data such as authentication tokens, always use cryptographically secure hash functions like SHA-256 instead of faster but insecure alternatives like MD5 or CRC32. Secure hash functions provide protection against reverse engineering and rainbow table attacks, which is critical for maintaining the confidentiality of sensitive information.

Additionally, consider truncating the hash output to further prevent reverse engineering attempts. For debugging purposes, guard such operations behind debug flags to minimize exposure in production environments.

Example:
```go
func writeLogHeader(config configuration.Configuration) {
    tokenShaSum := []byte{}
    if token := config.GetString(configuration.AUTHENTICATION_TOKEN); len(token) > 0 {
        temp := sha256.Sum256([]byte(token))  // Use SHA-256, not MD5 or CRC32
        tokenShaSum = temp[:16]  // Truncate to 16 bytes to prevent reverse engineering
    }
    // ... rest of logging logic
}
```

This approach ensures that even if logs are compromised, the original sensitive data remains protected through strong cryptographic practices.