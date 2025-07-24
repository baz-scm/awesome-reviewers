---
title: Prevent TOCTOU vulnerabilities
description: Time-of-Check-to-Time-of-Use (TOCTOU) race conditions occur when a program
  checks a condition and then uses the result of that check, but the condition might
  have changed between the check and use. This pattern creates security vulnerabilities,
  particularly in file system operations, but can affect any multi-step operation
  where state might change.
repository: rust-lang/rust
label: Security
language: Rust
comments_count: 3
repository_stars: 105254
---

Time-of-Check-to-Time-of-Use (TOCTOU) race conditions occur when a program checks a condition and then uses the result of that check, but the condition might have changed between the check and use. This pattern creates security vulnerabilities, particularly in file system operations, but can affect any multi-step operation where state might change.

To prevent TOCTOU vulnerabilities:

1. Use atomic operations whenever possible instead of separate check-then-act sequences
   ```rust
   // VULNERABLE TO TOCTOU:
   if !Path::new("file.txt").exists() {
       File::create("file.txt")?; // Race condition: file might be created here by another process
   }
   
   // SAFER APPROACH:
   let file = File::options().create_new(true).open("file.txt"); // Atomic operation
   ```

2. Maintain resource handles throughout operations rather than repeatedly checking state
   ```rust
   // Keep the file open while working with it rather than reopening based on metadata checks
   let mut file = File::open("data.txt")?;
   // Continue using the same file handle for subsequent operations
   ```

3. Be skeptical of metadata obtained from previous checks, as it may be stale
   
4. For security-critical operations, verify that operations succeeded with their intended effect rather than assuming success

5. Never trust user input or external data without validation, especially in multi-step operations

Remember that even file locks may be insufficient protection against malicious actors, as they're often advisory and can potentially be bypassed.