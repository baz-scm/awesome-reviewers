---
title: Design for testability
description: Extract complex logic into separate, pure functions to improve testability.
  Functions with clear inputs and outputs are easier to test in isolation without
  complex mocking or setup.
repository: vercel/turborepo
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 28115
---

Extract complex logic into separate, pure functions to improve testability. Functions with clear inputs and outputs are easier to test in isolation without complex mocking or setup.

For example, instead of embedding logic directly in larger functions:

```typescript
// Hard to test
export async function transform(args: TransformInput): TransformResult {
  // ...
  // Complex logic embedded in a larger function
  let data = await fs.readFile(readmeFilePath, "utf8");
  const replacements = ['pnpm run', 'npm run', 'yarn run', 'bun run'];
  const replacementRegex = new RegExp(`\\b(?:${replacements.join('|')})\\b`, 'g');
  data = data.replace(replacementRegex, `${selectedPackageManager} run`);
  // ...
}
```

Extract the logic into a testable function:

```typescript
// Easy to test with various inputs
function replacePackageManager(packageManager: string, text: string): string {
  const replacements = ['pnpm run', 'npm run', 'yarn run', 'bun run'];
  const replacementRegex = new RegExp(`\\b(?:${replacements.join('|')})\\b`, 'g');
  return text.replace(replacementRegex, `${packageManager} run`);
}

// Can now be thoroughly tested with parameterized tests
it.each([
  ['npm', '`yarn build`', '`npm run build`'],
  ['pnpm', 'Run `npm start`', 'Run `pnpm run start`'],
  // more test cases...
])('should replace package managers correctly', (packageManager, input, expected) => {
  expect(replacePackageManager(packageManager, input)).toBe(expected);
});
```

This approach makes unit testing straightforward and enables comprehensive test coverage through parameterized test cases.