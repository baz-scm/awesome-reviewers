---
title: Maintain consistent style
description: 'Maintain consistent style patterns throughout the codebase to improve
  readability, reduce maintenance overhead, and prevent errors. Key areas to focus
  on:'
repository: oven-sh/bun
label: Code Style
language: Other
comments_count: 12
repository_stars: 79093
---

Maintain consistent style patterns throughout the codebase to improve readability, reduce maintenance overhead, and prevent errors. Key areas to focus on:

1. **Use consistent struct declarations**: For top-level structs, prefer:
   ```zig
   const Installer = @This();
   ```
   instead of:
   ```zig
   pub const Installer = struct {
   ```

2. **Eliminate redundancies**: Remove duplicate declarations such as repeated flags, option definitions, or multiple type declarations.
   ```zig
   // Bad - duplicates in options list
   GLOBAL_OPTIONS[LONG_OPTIONS]="--extension-order --jsx-factory --jsx-fragment --extension-order --jsx-factory --jsx-fragment"
   
   // Good - no duplicates
   GLOBAL_OPTIONS[LONG_OPTIONS]="--extension-order --jsx-factory --jsx-fragment"
   ```

3. **Maintain consistent formatting**: Ensure proper spacing, consistent namespace qualifiers, and appropriate control structures.
   ```zig
   // Bad - inconsistent namespace qualification
   if (comptime Environment.debug_checks) {
   
   // Good - consistent qualification
   if (comptime bun.Environment.debug_checks) {
   ```
   
4. **Use appropriate control structures**: Choose the most readable structure for the logic being expressed.
   ```zig
   // Consider switch statements for multiple conditions
   fn isValidRedirectStatus(status: u16) bool {
       return switch (status) {
           301, 302, 303, 307, 308 => true,
           else => false,
       };
   }
   ```

Consistent style makes code easier to read, review, and maintain for the entire team.