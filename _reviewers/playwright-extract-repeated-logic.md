---
title: Extract repeated logic
description: When you find yourself writing similar code patterns multiple times,
  extract them into reusable methods, constants, or leverage existing helpers. This
  improves maintainability and reduces the chance of inconsistencies.
repository: microsoft/playwright
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 76113
---

When you find yourself writing similar code patterns multiple times, extract them into reusable methods, constants, or leverage existing helpers. This improves maintainability and reduces the chance of inconsistencies.

**Examples of what to extract:**

1. **Repeated code blocks** - Extract into shared methods:
```typescript
// Instead of duplicating enqueue logic:
for (let i = 0; i < repeatCount; ++i)
  this._frameQueue.push(this._lastFrameBuffer);

// Extract to:
private _enqueueFrames(count: number, buffer: Buffer) {
  for (let i = 0; i < count; ++i)
    this._frameQueue.push(buffer);
}
```

2. **Magic values used multiple times** - Use constants:
```typescript
// Instead of repeating colors:
const color = elements.length > 1 ? '#f6b26b7f' : '#6fa8dc7f';

// Use constants:
const HIGHLIGHT_COLOR_MULTIPLE = '#f6b26b7f';
const HIGHLIGHT_COLOR_SINGLE = '#6fa8dc7f';
```

3. **Leverage existing utilities** - Before writing new code, check if helpers already exist:
```typescript
// Instead of custom implementation, use existing helper:
const callLocation = wrapFunctionWithLocation((location: Location, ...args) => 
  this._modifier('skip', location, ...args)
);
```

4. **Avoid redundant computations** - Pass computed values instead of recomputing:
```typescript
// Instead of retrieving from map twice:
const data = this._dataByTestId.get(params.testId);
this._updateTest(data); // Pass the data directly
```