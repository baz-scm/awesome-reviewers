---
title: Provide actionable errors
description: Error messages should not only identify problems but also guide developers
  toward solutions. Include specific steps, alternatives, or configuration changes
  that can resolve the issue.
repository: microsoft/typescript
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 105378
---

Error messages should not only identify problems but also guide developers toward solutions. Include specific steps, alternatives, or configuration changes that can resolve the issue.

When designing error handling:
1. Make error messages specific to the exact construct causing the error
2. Position error indicators at locations that clearly indicate the source of the problem
3. Include remediation steps in the error message when possible
4. Consider graceful degradation for non-critical errors where it improves user experience

Example of a good error message:
```typescript
// Instead of:
if (fileExtensionIsOneOf(fileName, [Extension.Cts, Extension.Cjs])) {
    return Diagnostics.ECMAScript_imports_and_exports_cannot_be_written_in_a_CommonJS_file_under_verbatimModuleSyntax;
}

// Prefer:
if (fileExtensionIsOneOf(fileName, [Extension.Cts, Extension.Cjs])) {
    return Diagnostics.ECMAScript_imports_and_exports_cannot_be_written_in_a_CommonJS_file_under_verbatimModuleSyntax_Adjust_the_type_field_in_the_nearest_package_json_to_make_this_file_an_ECMAScript_module_or_adjust_your_verbatimModuleSyntax_module_and_moduleResolution_settings_in_TypeScript;
}
```

This approach reduces debugging time by helping developers understand not just what went wrong, but how to fix it. For complex configurations or language features, this guidance is especially valuable to both new and experienced developers.