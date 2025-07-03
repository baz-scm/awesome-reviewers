---
title: Layer security defenses
description: Implement multiple layers of security throughout your application rather
  than relying on a single protection mechanism. This defense-in-depth approach significantly
  improves your application's security posture.
repository: rails/rails
label: Security
language: Markdown
comments_count: 9
repository_stars: 57027
---

Implement multiple layers of security throughout your application rather than relying on a single protection mechanism. This defense-in-depth approach significantly improves your application's security posture.

1. Encrypt sensitive data appropriately:
```ruby
class User < ApplicationRecord
  # Use non-deterministic encryption for maximum security
  encrypts :social_security_number
  
  # Only use deterministic encryption when queries are needed
  encrypts :email, deterministic: true, downcase: true
  
  # Ensure password security beyond has_secure_password
  validates :password, length: { minimum: 12 }
end
```

2. Separate authentication (identity verification) from authorization (permissions):
```ruby
# Don't mix in Authentication module
module Authorization
  extend ActiveSupport::Concern
  
  def require_admin
    redirect_to root_path unless Current.user&.admin?
  end
end
```

3. Use environment-specific security controls:
```yaml
# config/storage.yml
production:
  service: S3
  environment: production
  # additional settings
```

4. Apply modern cryptographic standards (SHA256 instead of SHA1)
5. Use HTTPS for all remote resources
6. Add Content Security Policies to all responses including APIs
7. Implement rate limiting for authentication endpoints

Always document security trade-offs when making implementation decisions and regularly update security measures as standards evolve.
