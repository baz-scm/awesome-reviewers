---
title: Use descriptive names
description: Choose names that clearly communicate purpose, content, and intent. Avoid
  generic or ambiguous identifiers that require additional context to understand.
repository: snyk/cli
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 5178
---

Choose names that clearly communicate purpose, content, and intent. Avoid generic or ambiguous identifiers that require additional context to understand.

**Function names** should describe what the function does:
```ts
// Avoid: generic or misleading names
function depGraphData(dg: DepGraphData, targetName: string): string
function throwCodeClientError(error) // doesn't actually throw

// Prefer: descriptive names that indicate the action/output
function depGraphToOutputString(dg: DepGraphData, targetName: string): string  
function resolveCodeClientError(error)
```

**Variable names** should indicate their content:
```ts
// Avoid: misleading or generic names
const dirPath = 'iac/cloudformation/aurora-valid.yml'; // actually a file path
const id = await submitHashes(); // which ID?

// Prefer: specific, descriptive names
const filePath = 'iac/cloudformation/aurora-valid.yml';
const taskId = await submitHashes();
```

**Parameter names** should be explicit and self-documenting:
```ts
// Avoid: generic objects or unclear parameters
function getCodeDisplayedOutput(testResults, meta, prefix, shouldFilterIgnored)
function getIacCloudContext(testConfig: Partial<TestConfig>)

// Prefer: explicit parameters that communicate intent
function getCodeDisplayedOutput(args: {
  testResults: CodeTestResults,
  meta: string,
  prefix: string,
  shouldFilterIgnored: boolean
})
function getIacCloudContext(snykCloudEnvironment?: string)
```

This reduces cognitive load, improves code readability, and makes the codebase more maintainable by eliminating the need to infer meaning from context.