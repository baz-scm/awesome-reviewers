---
title: Null-Safe Inputs And Mapping
description: When a value is optional (or can differ by feature/region/constructor),
  never assume it’s present or non-empty. Apply consistent null/empty/whitespace handling,
  gate context-dependent logic, and validate after any transform (e.g., JSON/model
  conversion) so missing fields don’t silently change behavior.
repository: Azure/azure-powershell
label: Null Handling
language: C#
comments_count: 5
repository_stars: 4762
---

When a value is optional (or can differ by feature/region/constructor), never assume it’s present or non-empty. Apply consistent null/empty/whitespace handling, gate context-dependent logic, and validate after any transform (e.g., JSON/model conversion) so missing fields don’t silently change behavior.

**Apply this standard:**
1. **Normalize inputs early:** treat whitespace-only strings as `null`; use `string.IsNullOrWhiteSpace` for string parameters.
2. **Guard required combinations:** validate that when one input is provided (e.g., identity type/IDs), the other required fields are not `null`/empty; throw a clear `PSInvalidOperationException` (or equivalent) for invalid combinations.
3. **Gate context usage:** only dereference optional context objects when they’re guaranteed to exist; if not, either skip inference or throw a clear error.
4. **Validate after serialization/type conversion:** if you bridge models (JSON serialize/deserialize, dictionary casts, etc.), null-check the result and confirm critical fields (e.g., IDs, target details) survived.
5. **Preserve existing values unless explicitly overridden:** in update flows, don’t overwrite nullable/optional properties with defaults just because the new parameters are absent.

**Pattern example (normalization + post-mapping validation):**
```csharp
string changeReference = boundParameters.TryGetValue("-ChangeReference", out var v)
    ? v as string
    : null;
changeReference = string.IsNullOrWhiteSpace(changeReference) ? null : changeReference;

// Example for mapping/bridge where fields can be lost
var json = JsonConvert.SerializeObject(restoreRequest);
var mapped = JsonConvert.DeserializeObject<MyCrrRestoreRequest>(json);
if (mapped == null || mapped.TargetDetails == null || string.IsNullOrEmpty(mapped.SourceResourceId))
{
    throw new InvalidOperationException("Mapping lost required fields (TargetDetails/SourceResourceId). Update the bridge models.");
}
```

This prevents NullReferenceExceptions, incorrect defaults, and silent behavior changes caused by missing/empty inputs or divergent model mappings.