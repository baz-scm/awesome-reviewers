---
title: Prioritize JSX readability
description: Favor inline conditional rendering in JSX over extracting logic to variables
  before the return statement, as it maintains better flow control visibility and
  reduces cognitive overhead when reading components. Additionally, use descriptive
  variable names that clearly convey their purpose and state.
repository: cypress-io/cypress
label: React
language: TSX
comments_count: 2
repository_stars: 48850
---

Favor inline conditional rendering in JSX over extracting logic to variables before the return statement, as it maintains better flow control visibility and reduces cognitive overhead when reading components. Additionally, use descriptive variable names that clearly convey their purpose and state.

For conditional rendering, prefer:
```tsx
return (
  <div>
    {state.specs.length < 1 
      ? <NoSpec />
      : <SpecList />
    }
  </div>
)
```

Over extracting to variables:
```tsx
const specListContent = state.specs.length < 1 
  ? <NoSpec />
  : <SpecList />

return (
  <div>
    {specListContent}
  </div>
)
```

The inline approach keeps the rendering logic visible in context, making it easier to understand what gets rendered without jumping between variable definitions. For variable naming, choose names that clearly indicate the variable's role - for example, use `isRunning` instead of `isLive` when the variable represents whether a process is currently executing.