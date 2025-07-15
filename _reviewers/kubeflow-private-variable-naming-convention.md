---
title: Private variable naming convention
description: Use the 'prv' prefix for private class members and ensure they're explicitly
  declared with the 'private' access modifier. This maintains consistency with established
  team conventions and improves code readability by clearly indicating variable scope.
repository: kubeflow/kubeflow
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 15064
---

Use the 'prv' prefix for private class members and ensure they're explicitly declared with the 'private' access modifier. This maintains consistency with established team conventions and improves code readability by clearly indicating variable scope.

```typescript
export class MyComponent {
  // Correct: prefix matches access modifier
  private prvUserData: UserData;
  
  // Incorrect: prefix doesn't match access modifier
  public prvConfig: Config;
  
  // Incorrect: no prefix but is private
  private userData: UserData;
}
```

When refactoring existing code, update variable declarations to follow this pattern consistently. For observable patterns, public-facing properties should have clean names without implementation details while their corresponding subjects should use the 'prv' prefix:

```typescript
export class MyService {
  // Private subjects
  private prvDataSubject = new ReplaySubject<Data>(1);
  
  // Public observable (clean naming)
  data = this.prvDataSubject.asObservable();
}
```
