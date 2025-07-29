---
title: Choose descriptive names
description: Prioritize semantic clarity and descriptive naming over brevity or convenience.
  Avoid esoteric, abbreviated, or ambiguous identifiers that require mental translation
  to understand their purpose.
repository: sveltejs/svelte
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 83580
---

Prioritize semantic clarity and descriptive naming over brevity or convenience. Avoid esoteric, abbreviated, or ambiguous identifiers that require mental translation to understand their purpose.

**Key principles:**
- Replace esoteric terms with clear alternatives (e.g., `value` instead of `clazz`, `createSubscriber` instead of `createStartStopNotifier`)
- Use semantically meaningful parameter names (e.g., `disallow_loose` instead of `is_each`, `attribute` instead of `node_or_nodes`)
- Prefer positive boolean names over negatives (e.g., `track_owner` instead of `skip_derived_source`)
- Ensure function names match their return behavior (functions starting with `is_` should return boolean, not mixed types)

**Example:**
```javascript
// Avoid esoteric or ambiguous names
function to_class(clazz, hash, classes) { // ❌ "clazz" is esoteric
function to_class(value, hash, classes) { // ✅ "value" is clear

// Use semantically meaningful parameters  
function read_expression(parser, opening_token, is_each) { // ❌ unclear purpose
function read_expression(parser, opening_token, disallow_loose) { // ✅ clear intent

// Prefer positive boolean names
export function source(v, skip_derived_source = false) { // ❌ negative logic
export function source(v, track_owner = true) { // ✅ positive logic
```

This approach reduces cognitive load, improves code readability, and makes the codebase more maintainable by ensuring names clearly communicate their purpose and behavior.