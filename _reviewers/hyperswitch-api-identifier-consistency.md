---
title: API identifier consistency
description: Maintain consistent naming conventions for API identifiers, configuration
  keys, and payment method types. Use snake_case for all API identifiers to ensure
  uniformity across the system. This includes payment method types, configuration
  field names, and connector specifications.
repository: juspay/hyperswitch
label: API
language: Toml
comments_count: 3
repository_stars: 34028
---

Maintain consistent naming conventions for API identifiers, configuration keys, and payment method types. Use snake_case for all API identifiers to ensure uniformity across the system. This includes payment method types, configuration field names, and connector specifications.

When defining payment method types in configuration files, use lowercase with underscores rather than PascalCase or mixed formats. For example:

```toml
# Correct
payment_method_type = "amazon_pay"
google_pay_pre_decrypt_flow = "network_tokenization"

# Incorrect  
payment_method_type = "AmazonPay"
```

This consistency improves API predictability, reduces integration errors, and maintains a professional interface standard. Consider centralizing configuration logic in appropriate traits or specifications to avoid scattered configuration management across the codebase.