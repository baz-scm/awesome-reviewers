---
title: Simplify code structure
description: 'Strive to simplify code structure by eliminating unnecessary complexity.
  This includes:


  1. **Move conditions higher in the code** when appropriate to avoid unnecessary
  operations. Check conditions as early as possible to fail fast or skip work.'
repository: kubeflow/kubeflow
label: Code Style
language: Go
comments_count: 7
repository_stars: 15064
---

Strive to simplify code structure by eliminating unnecessary complexity. This includes:

1. **Move conditions higher in the code** when appropriate to avoid unnecessary operations. Check conditions as early as possible to fail fast or skip work.

```go
// Bad
if (someCondition) {
    // do work
}
if err := r.Update(ctx, profileIns); err != nil {
    return err
}

// Good
if (someCondition) {
    // do work
    if err := r.Update(ctx, profileIns); err != nil {
        return err
    }
}
```

2. **Avoid unnecessary conditionals** that don't change program behavior.

```go
// Bad
if !ok || existingValue != v {
    ns.Labels[k] = v
}

// Good
ns.Labels[k] = v
```

3. **Simplify complex if statements** by using early returns or continue statements to reduce nesting.

```go
// Bad
if pod.Status.ContainerStatuses[i].Name == instance.Name && 
   pod.Status.ContainerStatuses[i].State != instance.Status.ContainerState {
    // handle condition
}

// Good
if pod.Status.ContainerStatuses[i].Name != instance.Name {
    continue
}
if pod.Status.ContainerStatuses[i].State == instance.Status.ContainerState {
    continue
}
// handle condition
```

4. **Reduce nesting** by checking negative conditions first and returning early.

```go
// Bad
if nodename != "" {
    // lots of code here
}

// Good
if nodename == "" {
    return nil
}
// lots of code here with less indentation
```

5. **Reuse existing functions** instead of creating new ones with similar functionality.

This makes your code more readable, maintainable, and less error-prone.
