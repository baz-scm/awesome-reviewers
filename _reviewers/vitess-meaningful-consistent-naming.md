---
title: Meaningful consistent naming
description: Use descriptive, semantically clear names that follow consistent patterns
  throughout the codebase. Names should convey purpose and follow established conventions.
repository: vitessio/vitess
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 19815
---

Use descriptive, semantically clear names that follow consistent patterns throughout the codebase. Names should convey purpose and follow established conventions.

Key guidelines:

1. **Use descriptive names that reflect purpose**
   - Avoid ambiguous variable names that can cause confusion
   - Replace unclear abbreviations with complete words
   ```go
   // Bad
   lockCtx, killWhileRenamingCancel := context.WithTimeout(ctx, onlineDDL.CutOverThreshold)
   defer killWhileRenamingCancel()
   
   // Good
   lockCtx, lockTimeoutCancel := context.WithTimeout(ctx, onlineDDL.CutOverThreshold)
   defer lockTimeoutCancel()
   ```

2. **Follow established naming patterns**
   - Use `Is` prefix for boolean getter methods
   - Follow Pascal case (PascalCase) for struct fields
   - Use existing patterns within the codebase
   ```go
   // Bad
   func (session *SafeSession) GetTxErrorBlockNextQueries() bool
   
   // Good
   func (session *SafeSession) IsTxErrorBlockNextQueries() bool
   ```

3. **Avoid redundancy in names**
   - Don't prefix struct names with package names
   - Remove unnecessary qualifiers when context is clear
   ```go
   // Bad (in package discovery)
   type discoveryOptions struct {...}
   
   // Good
   type options struct {...}
   
   // Bad
   type myShardActionInfo interface {...}
   
   // Good 
   type shardActionInfo interface {...}
   ```

4. **Be consistent with delimiters and formatting**
   - Use hyphens for command-line flags
   - Name functions to accurately describe what they do
   ```go
   // Bad
   fs.StringVar(&flagMysqlBindAddress, "mycnf_mysql_bin_address", ...)
   
   // Good
   fs.StringVar(&flagMysqlBindAddress, "mycnf-mysql-bin-address", ...)
   
   // Bad - function splits SQL but is called "parse"
   func parseSQL(querySQL ...string) ([]string, error)
   
   // Good - name matches actual behavior
   func splitSQL(querySQL ...string) ([]string, error)
   ```

5. **Prefer clarity over brevity**
   - Use complete words rather than unclear abbreviations
   ```go
   // Bad
   RetryNb int `json:"-"`
   
   // Good
   RetryCount int `json:"-"`
   ```

Following these naming conventions improves code readability, reduces cognitive load during reviews, and helps prevent bugs caused by confusion over variable or function purposes.