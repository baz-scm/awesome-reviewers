---
title: trust server-side validation
description: When integrating with external APIs or services that implement their
  own input validation, avoid duplicating that validation logic on the client side.
  Trust the authoritative server's validation mechanisms rather than attempting to
  replicate them locally.
repository: home-assistant/core
label: Security
language: Json
comments_count: 1
repository_stars: 80450
---

When integrating with external APIs or services that implement their own input validation, avoid duplicating that validation logic on the client side. Trust the authoritative server's validation mechanisms rather than attempting to replicate them locally.

This principle prevents validation inconsistencies, reduces maintenance overhead, and avoids potential security gaps that could arise from imperfect client-side validation implementations. The external service is the authoritative source for what constitutes valid input, and attempting to second-guess or replicate their validation logic can lead to discrepancies.

For example, when working with a third-party API that accepts various input formats (addresses, coordinates, URLs), let the service handle the validation:

```python
# Good: Let the external service validate
def share_to_vehicle(data):
    # Send data directly to external API
    # Let Tesla/external service validate the input format
    response = external_api.share(data)
    return response

# Avoid: Duplicating external validation logic
def share_to_vehicle(data):
    # Don't try to replicate Tesla's validation rules
    if not validate_address_format(data):  # Unnecessary
        raise ValidationError("Invalid format")
    response = external_api.share(data)
    return response
```

Focus your validation efforts on your own application's business logic and data integrity requirements, not on replicating external service validation.