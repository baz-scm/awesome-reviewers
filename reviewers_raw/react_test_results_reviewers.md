# Code Reviewers

Generated from: `../../../react_test_results.json`  
Total reviewers: **18**


## Reviewer 1: Balance constraints with flexibility

**Label:** `api`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions

### Description

When designing APIs, carefully evaluate constraints imposed on consumers. Each limitation should serve a clear purpose; otherwise, favor flexibility. Instead of rigid enforcement, consider more adaptable interfaces with documentation about recommended usage patterns.

For example, in discussion #4, an initial API design restricted objects to a single observer:

```js
if (this._observer !== null && this._observer !== observer) {
  throw new Error(
    'You are attaching an observer to a fragment instance that already has one. Fragment instances ' +
      'can only have one observer. Use multiple fragment instances or first call unobserveUsing() to ' +
      'remove the previous observer.',
  );
}
```

After review, this constraint was questioned: "What's the reason for this limitation?" The developer decided to "extend it to handle multiple and drop this error" since it "doesn't really take away anything to make it more flexible."

Similarly, in discussion #5, assumptions about mouse events were challenged with a suggestion to handle more edge cases:

```js
case 'mousedown': {
  if (((nativeEvent: any): MouseEvent).button === 0) {
    isMouseDown = true;
  }
  break;
}
case 'mouseup':
case 'dragend': {
  if (((nativeEvent: any): MouseEvent).button === 0) {
    isMouseDown = false;
  }
  break;
}
```

When designing APIs that must work across different versions or environments, use fallback patterns rather than rigid requirements. As seen in discussion #1, compatibility can be preserved with approaches like:

```js
const sourceCode = context.sourceCode ?? context.getSourceCode();
```

This approach enables your API to adapt to varying contexts while maintaining a consistent interface for consumers.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `a6f48531-d26e-45ae-8c0e-6aff83dbf87a`
- `adc97371-2715-463a-a4a1-04ac01d32991`
- `f0f0d3aa-739c-4dc2-9e0c-63434df7cc1f`
- `46e84ac4-242c-4edc-95a9-e3522dcd7455`

---

## Reviewer 2: Check property existence first

**Label:** `null handling`  
**Language:** `Javascript`  
**Discussion IDs:** 3 discussions

### Description

Always verify that an object and its properties exist before accessing them to prevent "cannot read property of undefined/null" errors. This is especially important when dealing with objects that might come from different build environments (dev vs. production) or third-party libraries.

There are two common approaches:
1. Using a falsy check when null and undefined are both invalid: `if (!obj)` or `if (!obj.property)`
2. Using explicit checks when you need to distinguish between different falsy values: `if (obj === undefined)` or `if (obj.property === null)`

**Example - Before:**
```javascript
// Risky code that might fail
clonedElement._store.validated = oldElement._store.validated;
```

**Example - After:**
```javascript
// Safe code that checks existence first
if (oldElement._store && clonedElement._store) {
  clonedElement._store.validated = oldElement._store.validated;
}
```

This is particularly important in codebases where:
1. Components might be rendered in both development and production environments
2. You're integrating with third-party libraries that might have different property structures
3. Properties might be conditionally added to objects

Being proactive about property existence checks leads to more robust code and prevents unexpected runtime errors.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `6b4e4295-4bca-4f08-a474-b2e0a78f9d87`
- `e3c2a37f-01ea-42c5-921f-d000c7fa85a9`
- `efe22d8e-1c95-4904-8bda-992e37485f70`

---

## Reviewer 3: Complete hook dependencies

**Label:** `react`  
**Language:** `Javascript`  
**Discussion IDs:** 3 discussions

### Description

Always specify complete dependency arrays in React hooks to prevent bugs from stale closures and avoid unnecessary rerenders. When using hooks like `useEffect`, `useMemo`, or `useCallback`, include all values from the component scope that are referenced inside the hook's callback function.

For custom hooks that wrap React's built-in hooks:
1. Pass through dependency arrays correctly rather than hardcoding them
2. Avoid type assertions (like `as any`) that bypass dependency checking
3. Remember that global variables and constants defined outside the component don't need to be dependencies

```javascript
// ❌ Incorrect: Missing dependencies
function Component({foo, bar}) {
  useEffect(() => {
    console.log(foo, bar);
  }, []); // Missing foo and bar

  // ❌ Incorrect: Bypassing dependency checks
  useCustomCallback(callback, [] as any);
}

// ✅ Correct: All dependencies included
function Component({foo, bar}) {
  const nonreactive = 0; // Local constant
  
  useEffect(() => {
    console.log(foo, bar, nonreactive);
  }, [foo, bar]); // nonreactive is a constant, doesn't need to be a dependency
  
  // ✅ Correct: Properly passing dependencies through
  useCustomCallback(callback, [callback]);
}
```

ESLint's exhaustive-deps rule can help identify missing dependencies automatically, preventing subtle bugs caused by stale closures.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `da807060-07e9-47e2-a4dd-78b1996043b8`
- `e7583997-ca70-49d4-b536-c8b674801cbc`
- `3582ac95-36ee-4881-a0e9-27fc09865d0d`

---

## Reviewer 4: Optimize hot paths

**Label:** `performance optimization`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions

### Description

In performance-critical code paths that execute frequently, optimize to reduce unnecessary operations that can impact runtime performance:

1. **Minimize repeated type checks** - Cache type information or restructure code to avoid redundant `typeof` calls, especially in loops or frequently called functions

2. **Avoid unnecessary allocations** - Don't create new arrays, Sets, or objects when you can work with existing data structures directly

3. **Use direct traversal** - When operating on DOM nodes or other hierarchical structures, prefer inline traversal over building intermediate collections:

```javascript
// Avoid this in hot paths
const children = new Set(); // Unnecessary allocation
elements.forEach(el => children.add(el));
children.forEach(child => child.addEventListener(type, listener));

// Prefer this approach
elements.forEach(el => el.addEventListener(type, listener));
```

4. **Be aware of thresholds** - Understand the impact of operations based on execution frequency:
    - <1ms: Optimal for very frequent operations
    - <10ms: Good for maintaining 60fps animations
    - <100ms: Maximum for responsive interactions

Operations that take more time should be candidates for optimization when they appear in hot paths.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `e2528f7b-68e2-4f89-8557-71420f1b5b65`
- `c6c4fbea-2025-439d-bd95-9cd3833fe337`
- `e7b4a399-73ac-4e91-91e5-757855420df2`
- `df8620f7-b953-4462-89cd-a628330954b8`

---

## Reviewer 5: Explicit CSP nonce management

**Label:** `security`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions

### Description

When implementing Content Security Policy (CSP) protections, always explicitly pass nonce values to components rather than auto-applying them. This gives developers more control over security aspects and prevents potential security bypasses when integrating components from different sources.

Key implementation guidelines:
- Pass nonces explicitly to components that need them (like style and script elements)
- Be aware that different content types may require different nonce values (`style-src` and `script-src` directives)
- Ensure elements with different nonces aren't inappropriately merged
- Handle nonces consistently across your application

Example in React:

```javascript
// Correct: Explicitly passing nonce to style elements
<style
  href="foo"
  precedence="default"
  nonce={CSPnonce}>{`.foo { color: hotpink; }`}</style>

// When rendering on server, pass nonce to the renderer
renderToPipeableStream(
  <App />,
  { nonce: CSPnonce }
);

// For preinitialized styles, ensure nonces are added consistently
// to maintain security guarantees
const preinitOptions = {
  precedence: 'default',
  nonce: CSPnonce // Explicitly add nonce here too
};
```

Properly implemented CSP with nonces is one of the strongest defenses against cross-site scripting (XSS) attacks, but only if nonces are managed correctly and consistently throughout your application.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `928c4310-eb18-4051-91c7-404c72066cf2`
- `df9322d2-a238-44d5-9a38-71bf5d412331`

---

## Reviewer 6: Use appropriate testing methods

**Label:** `testing`  
**Language:** `Javascript`  
**Discussion IDs:** 3 discussions

### Description

When writing tests, use the appropriate testing utilities and ensure proper test isolation.

For testing warning behaviors:
- Use `assertConsoleErrorDev` or `toErrorDev` instead of gating tests with environment flags like `@gate __DEV__`
- Assert both the warning and the expected behavior outcomes

For testing sequential or asynchronous actions:
- Use logging utilities like `Scheduler.log()` with corresponding assertions like `assertLog(['Action', 'Action'])`

Always clean up after tests that use mocks:
```javascript
// Bad: No cleanup after mocking
console.error = jest.fn();
// Test code...
// Missing cleanup!

// Good: Proper cleanup
const originalConsoleError = console.error;
console.error = jest.fn();
// Test code...
console.error = originalConsoleError; // Or use console.error.mockRestore();

// Better: Use afterEach for guaranteed cleanup
beforeEach(() => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  console.error.mockRestore();
});
```

Failing to clean up mocks can silently break subsequent tests by interfering with their assertions, making test failures difficult to debug.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `38b4c3c7-0b0a-4572-8855-e6b4cc5b6157`
- `9f88a8de-03f1-418d-b490-058b44ebfbf0`
- `a1669ac2-01d6-455c-954d-1650ad090448`

---

## Reviewer 7: Separate conditional paths

**Label:** `concurrency`  
**Language:** `Javascript`  
**Discussion IDs:** 3 discussions

### Description

When working with concurrent operations, separate conditional logic from potentially expensive or suspenseful execution paths. This improves performance, prevents race conditions, and makes concurrent code more predictable and maintainable.

**Why it matters:**
- Prevents unnecessary work in hot paths
- Reduces the risk of duplicate invocations and race conditions
- Makes concurrent code easier to reason about

**How to apply it:**
1. Hoist conditional checks higher in the call stack
2. Only invoke complex operations when necessary
3. Structure tests to properly simulate real concurrency patterns

**Example - Before:**
```js
function preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes) {
  // This check happens on every call, even when it's not needed
  if (!maySuspendCommit(type, props)) {
    // Regular path...
  } else {
    // Suspending path...
  }
}
```

**Example - After:**
```js
// In the calling function (e.g., completeWork):
const maySuspend = checkInstanceMaySuspend(type, props);
if (maySuspend) {
  preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes);
}

// Then the function only handles suspension cases
function preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes) {
  // Only suspension logic here
}
```

For testing concurrent operations, model tests to match real-world behavior using appropriate timing mechanisms:
```js
await act(async () => {
  submitButton.current.click();
  await waitForMicrotasks(); // Allow natural processing cycles
  submitButton.current.click(); // Second interaction
});
```

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `13859a85-2fb6-4fbc-a038-329e883f720e`
- `1b00d619-5e47-4fef-8860-70164b608ef0`
- `dd7a887f-82b2-4ab4-bfd2-e0fb5d367db5`

---

## Reviewer 8: Write readable conditionals

**Label:** `code style`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions

### Description

Structure conditionals for maximum clarity and comprehension. Avoid unnecessary negation in boolean expressions, use else clauses appropriately, and organize compound conditions to reduce cognitive load.

For JSX conditionals, prefer positive conditions with natural reading order:

```jsx
// Instead of:
<h1>{!show ? 'A' + counter : 'B' + counter}</h1>

// Prefer:
<h1>{show ? 'B' + counter : 'A' + counter}</h1>
```

For branching logic, use complete if/else structures rather than separate conditional blocks when checking for mutually exclusive conditions:

```javascript
// Instead of:
if (enableUnifiedSyncLane && (renderLane & SyncUpdateLanes) !== NoLane) {
  lane = SyncHydrationLane;
}
if (!lane) {
  // ...more code
}

// Prefer:
if (enableUnifiedSyncLane && (renderLane & SyncUpdateLanes) !== NoLane) {
  lane = SyncHydrationLane;
} else {
  // ...more code
}
```

These practices make code easier to scan, understand, and maintain, while reducing the potential for logical errors.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `b85bdb4d-5005-4639-879b-23b48dcaf0f2`
- `14d4d784-fcec-49d0-b6e9-0612a99d9db4`

---

## Reviewer 9: Document code intent

**Label:** `documentation`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions

### Description

Add clear comments that explain the intent and behavior of code that might not be immediately obvious to other developers. Meaningful comments should provide context about why the code exists and how it works, especially for:

1. Complex test cases:
```javascript
await waitForAll([
  'Suspend! [Hi]', 
  'Loading...', 
  
  // pre-warming
  'Suspend! [Hi]'
]);
```

2. Configuration options with special status:
```javascript
/**
 * 'recommended' is currently aliased to the legacy / rc recommended config to maintain backwards compatibility.
 * This is deprecated and in v6, it will switch to alias the flat recommended config.
 */
recommended: legacyRecommendedConfig,
```

Good comments focus on explaining the "why" behind code decisions rather than merely restating what the code does. They serve as documentation that remains valuable even as implementations change, helping future maintainers understand design intent and important constraints.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `69cb7067-a57c-4bed-a21b-7bb2ecb6e030`
- `7ecd9362-aa63-40de-a2c5-7952b06e4da3`

---

## Reviewer 10: Standardize URL handling

**Label:** `networking`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions

### Description

When working with URLs in networking code, always use the standard `URL` constructor to properly resolve relative URLs against a base URL instead of manual string concatenation or ad-hoc replacements. This ensures proper path resolution according to the URL specification and handles edge cases correctly.

For example, instead of:
```js
// Problematic: Doesn't properly resolve relative paths
const sourceMap = await fetchFileWithCaching(sourceMapURL).catch(() => null);

// Or hacky string replacements
const normalizedURL = url.replace('/./', '/');
```

Use the URL constructor:
```js
// Properly resolves relative URLs against the base URL
const sourceMap = await fetchFileWithCaching(
  new URL(sourceMapURL, sourceURL).toString()
).catch(() => null);
```

For complex URL normalization needs, consider extracting the logic to a dedicated function that can be maintained centrally and handle different URL formats, including those with custom protocols used by bundlers. This approach prevents networking errors caused by malformed URLs and improves code maintainability.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `5b3f2daa-1bb4-4a46-9e99-5e8c5f64518a`
- `8cd0ff4b-4121-4da0-b6ba-520fc01d72b3`

---

## Reviewer 11: Dry configuration patterns

**Label:** `configurations`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions

### Description

Apply DRY (Don't Repeat Yourself) principles to all configuration files to improve maintainability. Extract shared configuration options into reusable constants, especially for values used across multiple environments or settings. This pattern reduces errors when configurations need updating and makes your codebase more maintainable.

For example, instead of duplicating the same rule definitions across different configuration variants:

```js
// Instead of repeated configuration:
export const configs = {
  recommended: {
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },
  'flat/recommended': {
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  }
};

// Extract common configuration to constants:
const sharedRules = {
  'react-hooks/rules-of-hooks': 'error',
  'react-hooks/exhaustive-deps': 'warn',
};

export const configs = {
  recommended: { rules: sharedRules },
  'flat/recommended': { rules: sharedRules }
};
```

This approach also makes it easier to see at a glance which configurations are shared vs. environment-specific, improving code readability and making configuration changes less error-prone.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `0cc384dc-c67b-4762-b0f5-100625b31c33`
- `790a0e7e-88e1-43b0-8df6-0d90cfc0c231`

---

## Reviewer 12: Match errors to context

**Label:** `error handling`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions

### Description

Choose error handling mechanisms based on the error's severity and context. For critical issues that should prevent further execution, throw explicit exceptions. For non-critical issues, use logging with sufficient detail to aid debugging without interrupting execution.

When throwing exceptions for critical validation errors:
```ts
if (reference.resolved === null) {
  throw new Error('Unexpected undefined reference.resolved');
}
```

When logging non-critical issues, include precise location information and use visual indicators to distinguish error types:
```ts
const { reason, severity, loc } = compilation.detail;
const lnNo = loc.start?.line;
const colNo = loc.start?.column;
const isTodo = severity === ErrorSeverity.Todo;

console.log(
  chalk[isTodo ? 'yellow' : 'red'](
    `Failed to compile ${filename}${lnNo !== undefined ? `:${lnNo}${colNo !== undefined ? `:${colNo}` : ""}` : ""}`
  ),
  reason ? `\n  Reason: ${isTodo ? 'Unimplemented' : reason}` : ""
);
```

This approach helps identify bugs early in the development process for critical issues while providing informative, actionable feedback for less severe problems without unnecessarily halting execution.

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `a134acc3-dee1-41ae-8698-021b6dec3bbf`
- `b1e480cd-171a-4b0b-8063-fef565199b22`
- `e62c4ee5-03c9-4aaa-8f67-e73a928867a8`

---

## Reviewer 13: Verify performance empirically

**Label:** `performance optimization`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions

### Description

Always validate performance optimizations through measurement rather than assumptions. Run multiple iterations of performance tests to ensure statistical significance and reduce noise in your metrics.

When proposing performance-related changes:
1. Establish baseline measurements before making changes
2. Implement your optimization
3. Run the same tests multiple times (at least 5 iterations)
4. Calculate average metrics to verify actual improvement

```javascript
// Example: Multiple iterations for reliable performance testing
const iterations = 5;
let totalRenderTime = 0;

// Collect performance data across multiple runs
for (let i = 0; i < iterations; i++) {
  const performance = await measurePerformance(component);
  totalRenderTime += performance.renderTime;
}

// Calculate and report the average
const averageRenderTime = totalRenderTime / iterations;
console.log(`Average render time: ${averageRenderTime.toFixed(2)}ms`);
```

This approach prevents changes that might appear beneficial in a single test run but actually have neutral or negative impacts in production environments. Increasing the number of iterations provides higher confidence in your performance results.

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `8f261e17-048b-433d-9327-86cf4be31d1c`
- `0c8c68a4-af71-45e2-b042-80f82acd57ef`
- `9b60afbb-8597-42e6-8347-12258016dfc0`

---

## Reviewer 14: Multi-stack config settings

**Label:** `configurations`  
**Language:** `Other`  
**Discussion IDs:** 2 discussions

### Description

When creating configuration files for development environments that use multiple technology stacks, ensure settings are properly scoped to accommodate different file types and tools within the same project. This prevents validation errors and improves developer productivity.

For example, in a workspace with both Flow and TypeScript files, customize editor settings by file type:

```json
{
  "settings": {
    // General settings
    "editor.formatOnSave": true,
    
    // Tool-specific paths
    "flow.pathToFlow": "${workspaceFolder}/node_modules/.bin/flow",
    
    // Search optimization
    "search.exclude": {
      "**/dist/**": true,
      "**/build/**": true,
      "**/out/**": true
    },
    
    // File-type specific settings
    "prettier.configPath": "",
    "prettier.ignorePath": ""
  }
}
```

These scoped configurations ensure that the proper validation rules and formatting settings are applied to different parts of the codebase, making it easier for developers to work with mixed technology projects.

### Suggested Modules

- No specific modules suggested

### Discussion References

- `da387453-fa91-46e7-a233-748b34c9aed7`
- `9606c876-362b-4191-8bc2-438ac71f89ca`

---

## Reviewer 15: Optimize React Component Dependencies

**Label:** `react`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions

### Description

When implementing React components, ensure that dependencies between component state, props, and side effects are accurately tracked to prevent missed updates and unnecessary re-renders. This is crucial for maintaining efficient and responsive React applications.

Key practices:
1. Carefully analyze component state and derived values to identify all true dependencies for useEffect and other hooks.
2. Properly handle conditional rendering and dynamic dependencies in your use of hooks like useEffect.
3. Consider object identity and reference semantics when determining dependencies, especially for props and state.
4. Separate control flow dependencies from data dependencies when possible, using techniques like memoization.

Example:
```typescript
// Problematic - missing dependency in useEffect
function ProcessData({ inputData }: { inputData: any }) {
  const derived = condition ? sourceA : sourceB;
  
  // Later operations use 'derived' but don't track its dependencies
  useEffect(() => {
    process(derived.value);
  }, []); // Missing dependency on 'derived'
}

// Improved - proper dependency tracking in useEffect
function ProcessData({ inputData }: { inputData: any }) {
  const derived = condition ? sourceA : sourceB;

  // Correctly tracks the dependency on 'derived'
  useEffect(() => {
    process(derived.value);
  }, [derived]); // Properly includes derived as dependency
}
```

By carefully managing component dependencies, you can create more maintainable React code and improve the efficiency of your application, avoiding both unnecessary re-renders and missed updates.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `c8d56ff8-fb82-4bce-9fcb-7ad16749bc64`
- `ca68ebd1-d279-417f-a915-12ef646f8be9`
- `da1d1831-8110-49a0-9808-21e71e08a135`

---

## Reviewer 16: Defensive Handling of Nullable React Components

**Label:** `react`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions

### Description

When working with React components that may return null or undefined values, implement defensive coding patterns to prevent runtime errors and improve code reliability.

- Consume iterables that may contain null values into an intermediate array before spreading them into React components:

```typescript
// Potentially problematic - may cause runtime errors if items contains null
const items = [0, 1, 2, null, 4, false, 6];
return <MyComponent items={items} />;

// Safer approach - create intermediate array and then spread
const items = [0, 1, 2, null, 4, false, 6];
const itemValues = items.filter(item => item !== null); 
return <MyComponent items={itemValues} />;
```

- When accessing properties of React component props or state, verify the prop/state exists first or use defensive access patterns like optional chaining and nullish coalescing:

```typescript
// Risky - assumes arr1[0] exists and has a value property
const MyComponent = ({ arr1 }) => <div>{arr1[0].value}</div>;

// Safer with optional chaining and nullish coalescing
const MyComponent = ({ arr1 }) => <div>{arr1?.[0]?.value ?? 0}</div>;
```

Following these practices will improve the robustness of your React code and help static analysis tools correctly infer nullability.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `9d5c541f-3610-494d-b4cc-0870060566a4`
- `95febc6f-6f62-4ee3-a18a-08f407bb3384`

---

## Reviewer 17: Proper Usage of React Hooks

**Label:** `react`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions

### Description

When using the React library in Typescript, ensure that you are correctly implementing the recommended React hooks based on the version of ESLint being used in your project.

For projects using ESLint 9.0.0 and above, use the `recommended-latest` configuration for the `react-hooks` plugin. This will enforce the latest best practices for React hook usage.

For projects using ESLint versions below 9.0.0, use the `recommended-legacy` configuration for the `react-hooks` plugin. This will ensure compatibility with older versions of React and ESLint.

Example of correct usage:

```typescript
// For ESLint 9.0.0+
{
  "extends": [
    // ...
    "plugin:react-hooks/recommended-latest"
  ]
}

// For ESLint below 9.0.0 
{
  "extends": [
    // ...
    "plugin:react-hooks/recommended-legacy"
  ]
}
```

Avoid using deprecated configuration names like the plain `recommended`, even if they are still supported for backward compatibility. Always use the version-specific configurations to ensure your React code follows the latest best practices and remains compatible with the ESLint version in use.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `3e582e54-de98-4b65-b7e0-15cd51907316`
- `51ef3fba-8238-4920-9968-28844eac444e`

---

## Reviewer 18: Proper Scoping and Usage of React Variables

**Label:** `react`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions

### Description

When implementing React components, it is important to ensure that variables are properly scoped and used throughout the component lifecycle. This reviewer provides guidance on best practices for managing variable declarations and usage in React code:

- Group related variable declarations together to improve code organization and readability.
- When using variables within React hooks like `useEffect`, explicitly list all dependencies to prevent subtle bugs related to variable capturing.
- For loop variables used in closures (e.g. event handlers), prefer block scoping to ensure the intent of the variable usage is clear.
- Ensure that the scope and purpose of variables used across different contexts (hooks, closures, JSX) is obvious to readers of the code.

Proper variable management is crucial for writing maintainable and bug-free React components. The provided code examples demonstrate correct usage patterns that align with these principles.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `b30da732-b221-4311-8683-4e98d82ca09e`
- `3236194d-8e90-4808-96a2-9aee582a9450`

---
