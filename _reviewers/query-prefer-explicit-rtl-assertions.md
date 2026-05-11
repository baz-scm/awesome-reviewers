---
title: Prefer explicit RTL assertions
description: 'In React Testing Library tests, keep assertions outside components,
  and rely on proper global teardown.


  - Teardown/cleanup: Since RTL v9, `cleanup()` is automatic when RTL is configured
  normally. Only call `cleanup()` manually if your test setup does not provide an
  `afterEach`.'
repository: tanstack/query
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 49380
---

In React Testing Library tests, keep assertions outside components, and rely on proper global teardown.

- Teardown/cleanup: Since RTL v9, `cleanup()` is automatic when RTL is configured normally. Only call `cleanup()` manually if your test setup does not provide an `afterEach`.
- Assertion placement: Do not use `expect(...)` inside a React component. Instead, render the value to the DOM (or expose it via an element) and assert after render using RTL queries.
- Snapshot restraint: Prefer explicit assertions on specific text/values. Use snapshots only when they meaningfully reduce effort without obscuring intent.

Example (asserting after render, without component-level `expect`):
```js
function Page() {
  const { canFetchMore } = useInfiniteQuery(
    'items',
    (key, nextId = 0) => fetchItems(nextId),
    { initialData: [/* ... */] }
  )

  return <div data-testid="can-fetch-more">{String(canFetchMore)}</div>
}

const { getByTestId } = render(<Page />)
expect(getByTestId('can-fetch-more').textContent).toBe('true')
```