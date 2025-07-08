---
title: Guard shared state
description: Consistently protect shared state with appropriate synchronization mechanisms
  and ensure proper cleanup to prevent race conditions and deadlocks in concurrent
  environments.
repository: hashicorp/terraform
label: Concurrency
language: Go
comments_count: 4
repository_stars: 45532
---

Consistently protect shared state with appropriate synchronization mechanisms and ensure proper cleanup to prevent race conditions and deadlocks in concurrent environments.

When working with shared state:
1. **Protect all access to shared variables** with the same mutex, including both reads and writes
2. **Use `defer` statements to guarantee lock releases**, especially in functions with multiple return paths
3. **Consider synchronized accessor methods** instead of direct access to shared data structures
4. **Be consistent about mutex design patterns** - whether embedding or using as a field

```go
// BAD: Data race - accessing 'closed' without mutex protection
func (c *proxyCommandConn) Read(b []byte) (int, error) {
    if c.closed {  // Race condition here!
        return 0, io.EOF
    }
    return c.stdoutPipe.Read(b)
}

// GOOD: Protected access to shared state
func (c *proxyCommandConn) Read(b []byte) (int, error) {
    c.mutex.Lock()
    if c.closed {
        c.mutex.Unlock()
        return 0, io.EOF
    }
    c.mutex.Unlock()
    
    return c.stdoutPipe.Read(b)
}

// GOOD: Using defer for guaranteed unlock
func (l *Loader) LoadState(configPath string) (*states.State, tfdiags.Diagnostics) {
    // ... other code ...
    
    id, err := stateManager.Lock(statemgr.NewLockInfo())
    if err != nil {
        return state, diags.Append(/* error */)
    }
    defer stateManager.Unlock(id)  // Ensures unlock happens on all return paths
    
    // ... rest of function with potentially multiple return statements ...
}

// GOOD: Using synchronized accessor method
func (ctx *EvalContext) Variables() map[string]cty.Value {
    // Returns a new map with synchronized access internally
    // instead of directly exposing a shared map
}
```