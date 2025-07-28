---
title: Documentation accuracy standards
description: Ensure all function documentation accurately reflects the actual code
  behavior and includes complete, properly formatted descriptions of parameters and
  return values.
repository: neovim/neovim
label: Documentation
language: C
comments_count: 6
repository_stars: 91433
---

Ensure all function documentation accurately reflects the actual code behavior and includes complete, properly formatted descriptions of parameters and return values.

Key requirements:
1. **Match function signatures**: Documentation must accurately describe what the function actually does and returns. A void function should not claim to "return true".

2. **Complete parameter documentation**: All parameters must be documented with proper formatting:
   - Use `@param[in/out] name  Description` with two spaces after name
   - Align descriptions consistently
   - Avoid redundant phrases like "and description" when describing error parameters

3. **Proper return value documentation**: Use `@return` as the start of a sentence, not embedded within it:
   ```c
   // Incorrect:
   /// @return Always return 0.
   
   // Correct:
   /// @return always 0.
   ```

4. **Follow formatting conventions**: Use proper spacing, alignment, and structure as shown in established patterns:
   ```c
   /// Get information about Num/Caps/Scroll Lock state
   ///
   /// To be used in nvim_get_keyboard_mods_state() API function.
   ///
   /// @param[out]  dict  Pointer to dictionary where information about modifiers
   ///                    is to be dumped.
   /// @param[out]  err   Location where error message is to be saved, set to NULL
   ///                    if no error.
   ///
   /// @return true in case of error, false otherwise.
   ```

5. **Avoid unnecessary language**: Remove vague terms like "helper function" that don't add meaningful information to the documentation.

This ensures developers can rely on documentation to understand function behavior without needing to read the implementation.