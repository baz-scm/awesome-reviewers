---
title: Null-safe Data Access
description: 'Across CLI/API payload handling, treat nullable fields and missing keys
  as first-class: normalize None before iterating/len’ing, use safe access for nested
  structures, and validate prerequisites early with clear user errors.'
repository: Azure/azure-cli
label: Null Handling
language: Python
comments_count: 8
repository_stars: 4592
---

Across CLI/API payload handling, treat nullable fields and missing keys as first-class: normalize None before iterating/len’ing, use safe access for nested structures, and validate prerequisites early with clear user errors.

**Coding standards**
1) **Normalize containers before iteration/length checks**
- If a field can be `None` but you will iterate or call `len()`, convert it to an appropriate default (`[]` for iterables, `{}` for maps).

2) **Use safe nested access for dict-based payloads**
- Avoid direct `payload['a']['b']` when `a`/`b` may be missing or `None`. Use `.get()` (or explicit guards) along the path.

3) **Fallback when SDK models may surface nullable properties**
- If an SDK returns typed objects where `.properties` (or similar) may be `None`, fall back to the raw response/payload rather than forcing access.

4) **Don’t over-guard when upstream contracts already guarantee types**
- Remove redundant checks that obscure intent. If upstream guarantees `result` is a dict, don’t add `isinstance(result, dict)` solely for safety.
- Where item-level shape is uncertain, guard at the item boundary (e.g., ensure item is a dict before calling `.get()`).

5) **When null means “missing prerequisite,” raise a clear CLI error**
- If required related state is absent (e.g., managed identity object needed for an MSI-related option; host names required unless `--hostname` is provided), validate and raise `ArgumentUsageError`/validation errors before calling the backend.

**Example pattern**
```python
# 1) normalize before iteration
additional_info = json_obj.get('additionalInfo') or []
for x in additional_info:
    ...

# 2) safe nested dict access
vmss = vmss_result  # dict
storage_profile = vmss.get('virtualMachineProfile', {}).get('storageProfile')
if storage_profile is not None:
    storage_profile['imageReference'] = None

# 3) fallback when SDK returns None-able properties
keys = sdk_list_function_keys(...)
return keys.properties if keys.properties is not None else dict(keys)

# 4) explicit validation on prerequisite nulls
identity = webapp.get('identity')
if enable_using_msi and not identity:
    raise ArgumentUsageError(
        "--enable-using-msi requires a managed identity. Assign one with: ..."
    )
```

Applying these rules consistently prevents `TypeError`/`KeyError` from null containers, avoids opaque backend failures, and keeps null-handling intent explicit and reviewable.