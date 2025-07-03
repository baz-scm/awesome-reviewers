---
title: Secure credential management
description: 'When handling passwords, certificates, or keys in your code, implement
  secure encryption and storage mechanisms to prevent exposure of sensitive data. '
repository: chef/chef
label: Security
language: Ruby
comments_count: 5
repository_stars: 7860
---

When handling passwords, certificates, or keys in your code, implement secure encryption and storage mechanisms to prevent exposure of sensitive data. 

Key practices:

1. Use strong encryption with unique salts when hashing sensitive data to prevent rainbow table attacks:

```ruby
# Poor implementation - vulnerable to rainbow tables
def obscure(cleartext)
  return nil if cleartext.nil? || cleartext.empty?
  Digest::SHA2.new(256).hexdigest(cleartext)
end

# Better implementation - with salt
def obscure(cleartext)
  return nil if cleartext.nil? || cleartext.empty?
  salt = SecureRandom.hex(16)  # Generate a random 16-byte salt
  hash = Digest::SHA2.new(256).hexdigest(salt + cleartext)
  { hash: hash, salt: salt }  # Store both hash and salt
end
```

2. Use platform-appropriate secure storage mechanisms (registry on Windows, keychain on macOS) rather than storing credentials in plaintext files.

3. When migrating between encryption methods, ensure backward compatibility while maintaining or improving security. Plan for safe key rotation without disrupting existing implementations.

4. Use dedicated encryption libraries when available rather than implementing your own cryptography:

```ruby
# Prefer built-in encryption libraries over custom implementations
Chef::ReservedNames::Win32::Crypto.encrypt(password)
```

5. Validate that credential operations succeed and provide meaningful error handling when they fail, without exposing sensitive details in logs or error messages.
