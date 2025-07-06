---
title: Path traversal prevention
description: 'Implement multiple validation layers to prevent path traversal attacks.
  File paths provided by users or external systems must be validated before use in
  filesystem operations:'
repository: ollama/ollama
label: Security
language: Go
comments_count: 2
repository_stars: 145705
---

Implement multiple validation layers to prevent path traversal attacks. File paths provided by users or external systems must be validated before use in filesystem operations:

1. Validate paths using both general and specialized checks:
   ```go
   // First validate with fs.ValidPath
   if !fs.ValidPath(fp) {
       return nil, fmt.Errorf("%w: %s", errFilePath, fp)
   }
   
   // Then use filepath.Clean to normalize
   fp = filepath.Clean(fp)
   
   // Finally validate containment with os.Root
   root, err := os.OpenRoot(safeDirectory)
   if err != nil {
       return nil, err
   }
   defer root.Close()
   // All file operations should go through this root
   ```

2. Enforce a consistent path policy, such as:
   - Paths must be relative (no leading "/")
   - Paths must not contain traversal components ("../", "./")
   - Paths must remain within the designated directory

3. Implement validation at every entry point rather than relying on validation in a single place - this defense-in-depth approach ensures security even if the code is refactored or one validation is bypassed.