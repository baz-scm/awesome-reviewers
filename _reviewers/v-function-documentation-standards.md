---
title: function documentation standards
description: 'All public functions and methods must be documented with comments that
  `v doc` can understand. Documentation should start with the function name and clearly
  explain the function''s behavior and purpose. For static methods, explicitly identify
  them as such (e.g., "MethodName static method returns..."). '
repository: vlang/v
label: Documentation
language: Other
comments_count: 7
repository_stars: 36582
---

All public functions and methods must be documented with comments that `v doc` can understand. Documentation should start with the function name and clearly explain the function's behavior and purpose. For static methods, explicitly identify them as such (e.g., "MethodName static method returns..."). 

Comments should be informative and provide meaningful context rather than simply repeating variable or function names. Avoid comments that just expand on names without adding value - it's better to have no comment than one that merely restates obvious information.

Example of proper function documentation:
```v
// get_queryset returns a list of QuerySet objects from the database query
pub fn (db &DB) get_queryset(query string) ![]QuerySet {

// Time.new static method returns a time struct with the calculated Unix time
pub fn Time.new() Time {
```

For complex code sections, add explanatory comments that clarify the purpose and reasoning, especially when the logic is not immediately obvious from reading the code.