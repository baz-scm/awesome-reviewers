---
title: Precise condition checks
description: Avoid using ambiguous or overly simplistic checks when determining object
  state, especially when handling null, undefined, or special values like empty strings.
  Ensure conditions precisely target the specific case you need to validate to prevent
  false positives.
repository: facebook/react
label: Null Handling
language: Javascript
comments_count: 2
repository_stars: 236852
---

Avoid using ambiguous or overly simplistic checks when determining object state, especially when handling null, undefined, or special values like empty strings. Ensure conditions precisely target the specific case you need to validate to prevent false positives.

**Why it matters:**
Imprecise conditions can lead to unexpected behavior when edge cases occur, such as when an empty string exists in both root and nested objects, or when optional values are accessed without proper checking.

**Example - problematic code:**
```javascript
// Problematic - assumes empty string key only occurs at root level
isParsingRootModel = key === '';

// Risky access of potentially undefined properties without verification
const writable = debugChannel.writable;
```

**Example - improved code:**
```javascript
// More precise check that considers context or additional conditions
isParsingRootModel = key === '' && parentContext === null;

// Using optional chaining for potentially undefined values
const writable = debugChannel?.writable;
```

When writing condition checks, consider all possible contexts where your condition might be evaluated and ensure your logic handles all edge cases appropriately. For optional types, use language features like optional chaining to safely handle potentially undefined values.

## Discussions

### [packages/react-client/src/ReactFlightClient.js](https://github.com/facebook/react/pull/32316)

```javascript
function createFromJSONCallback(response: Response) {
  // $FlowFixMe[missing-this-annot]
  return function (key: string, value: JSONValue) {
    isParsingRootModel = key === '';
```

**Discussion:**

- **sebmarkbage:** We can't assume that an empty string key is the root since it may also be on nested objects. What's the implication of that?
- **unstubbable:** Hmm, we were already using the check here: https://github.com/facebook/react/blob/192555bb0ed88db30f91c58651c421f178f90384/packages/react-client/src/ReactFlightClient.js#L983-L987 But I guess you're right, it could also be an explicit empty key in some object.

### [packages/react-server-dom-parcel/src/client/ReactFlightDOMClientBrowser.js](https://github.com/facebook/react/pull/33627)

```javascript
}

export type Options = {
  debugChannel?: {writable?: WritableStream, ...},
```

**Discussion:**

- **sebmarkbage:** @devongovett You might want to remove these options and instead just wire it up automatically in development to any HMR sockets in Parcel automatically on both ends.

