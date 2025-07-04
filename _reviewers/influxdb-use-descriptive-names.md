---
title: Use descriptive names
description: 'Names in code should be self-documenting, accurately reflect purpose,
  and follow consistent conventions. Apply these principles throughout your code:

  '
repository: influxdata/influxdb
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 30268
---

Names in code should be self-documenting, accurately reflect purpose, and follow consistent conventions. Apply these principles throughout your code:

1. **Function/method names must accurately reflect behavior**
   ```go
   // Poor: Name doesn't match behavior (returns true even for running compactions)
   func FullyCompacted() (bool, string)
   
   // Better: Name accurately reflects behavior
   func CompactionOptimizationAvailable() (bool, string)
   ```

2. **Variable names should describe their content**
   ```go
   // Poor: Name suggests future action, but tracks completed fields
   var fieldsToCreate []*FieldCreate
   
   // Better: Name reflects actual content
   var createdFields []*FieldCreate
   ```

3. **Use named return values for clarity**
   ```go
   // Poor: Purpose of return values unclear
   func CreateFieldIfNotExists(name string, typ influxql.DataType) (*Field, bool, error)
   
   // Better: Return values purpose is clear
   func CreateFieldIfNotExists(name string, typ influxql.DataType) (f *Field, created bool, err error)
   ```

4. **Define constants for literal values**
   ```go
   // Poor: Magic strings scattered in code
   if t.HashedToken != "" {
     token = "REDACTED"
   } else {
     variantName = "N/A"
   }
   
   // Better: Named constants with clear semantics
   const (
     TokenRedacted = "REDACTED"
     ValueNotAvailable = "N/A"
   )
   ```

5. **Function naming should align with behavior**
   ```go
   // Poor: Name implies it starts a goroutine but doesn't
   func startFileLogWatcher(w WatcherInterface, e *Executor, ctx context.Context)
   
   // Better: Name reflects actual function behavior
   func fileLogWatch(w WatcherInterface, e *Executor, ctx context.Context)
   ```

Clear, descriptive naming reduces cognitive load, improves maintainability, and helps prevent bugs by making code behavior more obvious.