---
title: Reduce nesting depth
description: Improve code readability by reducing nesting depth with early returns
  and functional approaches. Use early returns to handle edge cases first, and prefer
  functional operators over nested conditionals when working with streams or collections.
repository: kubeflow/kubeflow
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 15064
---

Improve code readability by reducing nesting depth with early returns and functional approaches. Use early returns to handle edge cases first, and prefer functional operators over nested conditionals when working with streams or collections.

Example for early return:
```typescript
// Instead of this
selectType(event): void {
  this.typeSelected = event.value;
  if (this.typeSelected === 'New') {
    this.volume.controls.name.setValue(this.currentVolName);
  }
}

// Prefer this
selectType(event): void {
  this.typeSelected = event.value;
  if (this.typeSelected !== 'New') return;
  this.volume.controls.name.setValue(this.currentVolName);
}
```

Example for functional approach:
```typescript
// Instead of this
this.router.events.subscribe(event => {
  if (event instanceof NavigationEnd) {
    // Do something
  }
});

// Prefer this
this.router.events
  .pipe(filter(event => event instanceof NavigationEnd))
  .subscribe(event => {
    // Do something
  });
```
