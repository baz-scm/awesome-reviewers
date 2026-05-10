---
title: Precise Validation Documentation
description: When documenting inputs/validators, explicitly state (a) the units/meaning
  of any parameters (e.g., file size units), (b) what is truly validated (syntactic/format
  via regex vs semantic correctness), and (c) timezone/offset semantics using unambiguous
  wording (avoid phrasing that suggests an offset is “missing” when “Z” explicitly
  means zero offset). This...
repository: colinhacks/zod
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 42628
---

When documenting inputs/validators, explicitly state (a) the units/meaning of any parameters (e.g., file size units), (b) what is truly validated (syntactic/format via regex vs semantic correctness), and (c) timezone/offset semantics using unambiguous wording (avoid phrasing that suggests an offset is “missing” when “Z” explicitly means zero offset). This prevents common user misunderstandings and support churn.

Example (documentation style):
```ts
// Size constraints are in bytes.
const imageFile = z.file({
  required_error: "file is required",
  invalid_type_error: "This object must be a file",
}).size({ min: 100000, max: 200000 }); // bytes

// These string datetime checks validate the expected ISO format via regex,
// not calendar correctness.
// e.g., the parser may accept a syntactically valid shape even if the date is impossible.
const dt = z.string().datetime(); // ISO 8601; default is UTC zero offset ('Z')

// If you also add date/time helpers, document their format basis and options.
const date = z.string().date(); // ISO short date format
const time = z.string().time(); // 24-hour time of day format
```

Checklist for contributors:
- Any “size”, “length”, “min/max”, or unit-based parameter: name the unit.
- Any “datetime/date/time” validator: clarify format-vs-correctness behavior.
- Any timezone/offset defaults: describe how UTC is represented (e.g., via 'Z') and avoid ambiguous phrases like “without UTC offset.”