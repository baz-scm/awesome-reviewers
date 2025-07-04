---
title: Secure authentication defaults
description: 'Configure authentication mechanisms with secure default settings to
  prevent security vulnerabilities. When implementing WebAuthn or similar authentication
  protocols:'
repository: quarkusio/quarkus
label: Security
language: Java
comments_count: 4
repository_stars: 14667
---

Configure authentication mechanisms with secure default settings to prevent security vulnerabilities. When implementing WebAuthn or similar authentication protocols:

1. **Avoid attestation bypasses**: Do not include verifiers that allow skipping attestation checks.
   ```java
   // INCORRECT: Allows attestation bypass
   return new WebAuthnAsyncManager(
       Arrays.asList(
           new NoneAttestationStatementAsyncVerifier(),
           // other verifiers
       )
   );
   ```

2. **Use recommended timeouts**: Follow standard security recommendations for timeout values.
   ```java
   // INCORRECT: Too short for authentication ceremonies
   this.timeout = config.timeout().orElse(Duration.ofSeconds(60));
   
   // CORRECT: Use recommended 5 minutes
   this.timeout = config.timeout().orElse(Duration.ofMinutes(5));
   ```

3. **Enable security verifications by default**: Features like user presence verification should be enabled by default.
   ```java
   // INCORRECT: Security feature disabled by default
   this.userPresenceRequired = config.userPresenceRequired().orElse(false);
   
   // CORRECT: Security feature enabled by default
   this.userPresenceRequired = config.userPresenceRequired().orElse(true);
   ```

4. **Prevent information disclosure**: Avoid endpoints that expose account information to unauthenticated requests, which could enable account enumeration attacks.
   ```java
   // VULNERABLE: Returns user-specific credential information
   // to unauthenticated requests
   .map(challenge -> security.toJsonString(challenge))
   .subscribe().with(challenge -> ok(ctx, challenge), ctx::fail);
   ```