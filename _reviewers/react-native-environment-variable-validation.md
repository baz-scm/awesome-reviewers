---
title: Environment variable validation
description: Environment variables should be properly validated with correct type
  checking and without redundant conditions. Common issues include comparing strings
  to integers and using unnecessary double-checks that can lead to unexpected behavior.
repository: facebook/react-native
label: Configurations
language: Ruby
comments_count: 2
repository_stars: 123178
---

Environment variables should be properly validated with correct type checking and without redundant conditions. Common issues include comparing strings to integers and using unnecessary double-checks that can lead to unexpected behavior.

**Key principles:**
1. **Avoid redundant checks**: Don't check if an environment variable exists and then check its value in the same condition
2. **Use correct types**: Environment variables are always strings, so compare against string values
3. **Simplify boolean logic**: Use direct comparisons instead of complex conditional chains

**Examples of issues and fixes:**

❌ **Problematic patterns:**
```ruby
# Redundant checking
if ENV["RCT_USE_PREBUILT_RNCORE"] && ENV["RCT_USE_PREBUILT_RNCORE"] == "1"

# Type mismatch - comparing string to integer
return ENV["RCT_NEW_ARCH_ENABLED"] == 0 ? false : true
```

✅ **Improved patterns:**
```ruby
# Direct value check
if ENV["RCT_USE_PREBUILT_RNCORE"] == "1"

# Correct string comparison with simplified logic
return ENV["RCT_NEW_ARCH_ENABLED"] != "0"
```

This approach prevents runtime errors, improves code readability, and ensures consistent behavior across different environments and deployment scenarios.