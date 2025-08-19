---
title: maintain API backwards compatibility
description: Never modify existing stable API versions in ways that could break backwards
  compatibility. When adding new functionality, always introduce it in unstable API
  versions first before stabilizing in new releases. For serialization formats, avoid
  renaming existing fields - instead use property mapping or add new fields alongside
  deprecated ones.
repository: duckdb/duckdb
label: API
language: Json
comments_count: 2
repository_stars: 32061
---

Never modify existing stable API versions in ways that could break backwards compatibility. When adding new functionality, always introduce it in unstable API versions first before stabilizing in new releases. For serialization formats, avoid renaming existing fields - instead use property mapping or add new fields alongside deprecated ones.

Example violations:
```json
// DON'T: Adding to existing stable version
"apis/v1/v1.2/v1.2.0.json": {
  "duckdb_get_time_ns"  // New function in stable version
}

// DON'T: Renaming serialization fields
{
  "id": 201,
  "name": "new_field_name"  // Breaking change
}
```

Correct approach:
```json
// DO: Add to unstable first
"apis/v1/unstable/new_functions.json": {
  "duckdb_get_time_ns"  // New function in unstable
}

// DO: Use property mapping for field changes
{
  "id": 201,
  "name": "projections",
  "property": "projection_map"  // Maps to new internal name
}
```

This ensures existing client code continues to work while allowing evolution of the API through proper versioning channels.