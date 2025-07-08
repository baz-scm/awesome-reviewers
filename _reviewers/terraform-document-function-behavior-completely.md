---
title: Document function behavior completely
description: Function and method documentation should accurately describe behavior,
  parameters, and any non-obvious aspects of the implementation. Documentation should
  evolve alongside code changes.
repository: hashicorp/terraform
label: Documentation
language: Go
comments_count: 5
repository_stars: 45532
---

Function and method documentation should accurately describe behavior, parameters, and any non-obvious aspects of the implementation. Documentation should evolve alongside code changes.

When writing function documentation:

1. Clearly explain the purpose and intended behavior of the function
2. Document all parameters, including unused ones (consider using underscore notation in parameter names to reinforce documentation)
   ```go
   // As backends are not implemented by providers, the provider schema argument should always be nil
   func (s *BackendConfigState) PlanData(schema *configschema.Block, _ *configschema.Block, workspaceName string) (*plans.Backend, error) {
   ```

3. Note any limitations, requirements, or special conditions (like type requirements for comparisons)
   ```go
   // AppendWithoutDuplicates only classifies "duplicates" as diagnostics which 
   // implement ComparableDiagnostic and return true for Equals
   func (diags Diagnostics) AppendWithoutDuplicates(newDiags ...Diagnostic) Diagnostics {
   ```

4. When deprecating functionality, always provide the recommended alternative
   ```go
   "endpoint": {
       Type:       schema.TypeString,
       Optional:   true,
       Deprecated: "`endpoint` is deprecated and superseded by `msi_endpoint`, please update your configuration to use `msi_endpoint` instead",
   }
   ```

5. Explain counter-intuitive implementations that might confuse future developers
   ```go
   // Note: we need to parse the test block before the run blocks
   // because run blocks depend on test configuration
   ```

Proper documentation reduces onboarding time for new developers, prevents misuse of functions, and makes code maintenance easier over time.