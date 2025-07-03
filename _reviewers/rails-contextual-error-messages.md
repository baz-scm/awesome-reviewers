---
title: Contextual error messages
description: Error messages should provide sufficient context to understand and debug
  the problem efficiently. Include both the expected and actual values in error messages,
  along with specific information about what failed. This makes troubleshooting much
  more straightforward and reduces debugging time.
repository: rails/rails
label: Error Handling
language: Ruby
comments_count: 4
repository_stars: 57027
---

Error messages should provide sufficient context to understand and debug the problem efficiently. Include both the expected and actual values in error messages, along with specific information about what failed. This makes troubleshooting much more straightforward and reduces debugging time.

**Good practice:**
```ruby
# Clear about what was expected and what was received
unless value == true || value == false
  raise ArgumentError, "distinct expects a boolean value, got: #{value.inspect}"
end

# Shows both expected and actual values
actual_checksum = service.compute_checksum(file) 
unless actual_checksum == checksum
  raise ActiveStorage::IntegrityError, "Checksum verification failed expecting #{checksum}, but downloaded file having #{actual_checksum}"
end

# Specific about which value caused the problem
unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }
  raise UnsupportedImageProcessingMethod, "Method '#{method_name}' is not supported. Supported methods: #{ActiveStorage.supported_image_processing_methods.join(', ')}"
end
```

**Bad practice:**
```ruby
# Vague error message with no context
unless value == true || value == false
  raise ArgumentError, "Invalid value"
end

# Missing the actual values causing the failure
unless actual_checksum == checksum
  raise ActiveStorage::IntegrityError, "Checksum verification failed"
end
```

Contextual error messages make your API more user-friendly and significantly reduce troubleshooting time when problems occur. They also serve as implicit documentation about parameter constraints and expected behaviors.
