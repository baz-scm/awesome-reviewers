---
title: Secure credential data handling
description: 'Always protect sensitive credential data through proper encryption,
  secure storage, and careful handling in code. Key requirements:


  1. Never store credentials in plaintext within source code'
repository: n8n-io/n8n
label: Security
language: TypeScript
comments_count: 4
repository_stars: 122978
---

Always protect sensitive credential data through proper encryption, secure storage, and careful handling in code. Key requirements:

1. Never store credentials in plaintext within source code
2. Use appropriate encryption for sensitive fields
3. Preserve user-configured security settings
4. Handle credential updates safely

Example - Instead of:
```typescript
class Config {
  password: string = 'admin';  // BAD: Hardcoded credential
  
  constructor(options) {
    this.tls = {};  // BAD: Overwrites user TLS settings
  }
}
```

Use:
```typescript
class Config {
  @Env('DB_PASSWORD')  // GOOD: Environment variable
  password: string = '';
  
  constructor(options) {
    this.tls = options.tls ?? {};  // GOOD: Preserves settings
  }
}

// GOOD: Proper credential field protection
class Credentials {
  @Column({
    type: 'string',
    typeOptions: { password: true }  // Enables encryption
  })
  sslKey: string;
}