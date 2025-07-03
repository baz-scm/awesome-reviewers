---
title: Check nulls directly
description: Check objects directly for null/empty state instead of using separate
  tracking variables. Always perform null checks early in your functions, before entering
  resource-intensive blocks or operations that assume non-null values.
repository: opencv/opencv
label: Null Handling
language: Other
comments_count: 2
repository_stars: 82865
---

Check objects directly for null/empty state instead of using separate tracking variables. Always perform null checks early in your functions, before entering resource-intensive blocks or operations that assume non-null values.

**Don't do this:**
```cpp
// Using a separate boolean flag to track object state
std::shared_ptr<dnn::Net> qbar_sr;
bool net_loaded_ = false;  // Redundant tracking variable

void someFunction() {
    if (net_loaded_) {  // Indirect check through tracking variable
        qbar_sr->performOperation();
    }
}
```

**Do this instead:**
```cpp
// Check the object directly
std::shared_ptr<dnn::Net> qbar_sr;

void someFunction() {
    if (qbar_sr) {  // Direct check of the object itself
        qbar_sr->performOperation();
    }
}
```

And always check for null parameters at the beginning of functions:

```cpp
void processData(const char* name) {
    // Check nulls early, before any processing or resource allocation
    if (name == NULL) {
        handleError("NULL name parameter");
        return;
    }
    
    // Now it's safe to use the parameter
    processName(name);
}
```

This approach improves code readability, reduces state tracking errors, and prevents null dereference bugs by ensuring validation happens before any operations that assume non-null values.
