---
title: Guard unsafe API calls
description: Always check the availability or state of data before accessing potentially
  unsafe API methods that can throw runtime errors. Many Angular APIs provide guard
  methods to safely check state before accessing values.
repository: angular/angular
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 98611
---

Always check the availability or state of data before accessing potentially unsafe API methods that can throw runtime errors. Many Angular APIs provide guard methods to safely check state before accessing values.

For example, when working with the resource API, always use `hasValue()` to guard calls to `value()`, as calling `value()` on a resource in an error state will throw an exception:

```ts
// ❌ Unsafe - can throw if resource is in error state
@if (imgResource.value() === '') {
  <div>Error state</div>
} @else {
  <img [src]="imgResource.value()" />
}

// ✅ Safe - guard with hasValue() first
@if (imgResource.isLoading()) {
  <div>Loading...</div>
} @else if (imgResource.hasValue()) {
  <img [src]="imgResource.value()" />
} @else {
  <div>Error state - retry available</div>
}
```

This pattern applies to other Angular APIs as well. Similarly, when handling errors in RxJS streams, ensure error handlers return the correct observable types expected by operators like `catchError`, which expects an `ObservableInput` rather than raw values.

The key principle is defensive programming: verify the state or availability of data before attempting to access it, preventing runtime errors and providing better user experience through proper error states.