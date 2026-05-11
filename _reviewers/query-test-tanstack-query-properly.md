---
title: Test TanStack Query Properly
description: 'When writing Angular unit/SSR tests for TanStack Query, align with Angular’s
  task tracking and keep caches isolated:


  - Prefer Angular injection helpers: test components/services should call `injectQuery`/`injectMutation`
  (not ad-hoc query execution) so Angular can track in-progress work via `PendingTasks`
  (Angular 19+).'
repository: tanstack/query
label: Angular
language: Markdown
comments_count: 2
repository_stars: 49380
---

When writing Angular unit/SSR tests for TanStack Query, align with Angular’s task tracking and keep caches isolated:

- Prefer Angular injection helpers: test components/services should call `injectQuery`/`injectMutation` (not ad-hoc query execution) so Angular can track in-progress work via `PendingTasks` (Angular 19+).
- Await completion via stability: in unit tests, use `ApplicationRef.whenStable()` or `fixture.whenStable()` to wait until queries/mutations become idle.
- Isolate per spec: create a new `QueryClient` for every test and provide it with `provideTanStackQuery(queryClient)` / `provideQueryClient(queryClient)`. Clear caches in `afterEach` if you reuse helpers.
- Keep test and production configs separate: do not include `withDevtools` (or other app dev configuration) in unit test providers—this can slow tests.
- Version note: `TestBed.tick()` exists in newer Angular versions (introduced in Angular 20). If you rely on ticking effects, ensure your project version supports it.

Example (unit test pattern):

```ts
import { injectQuery } from '@tanstack/angular-query-experimental'
import { QueryClient } from '@tanstack/query-core'
import { ApplicationRef, TestBed } from '@angular/core/testing'
import { provideTanStackQuery } from '@tanstack/angular-query-experimental'

let queryClient: QueryClient

beforeEach(() => {
  queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  })

  TestBed.configureTestingModule({
    providers: [provideTanStackQuery(queryClient)],
  })
})

afterEach(() => {
  queryClient.clear()
})

it('loads initial data', async () => {
  const appRef = TestBed.inject(ApplicationRef)

  const query = TestBed.runInInjectionContext(() =>
    injectQuery(() => ({
      queryKey: ['greeting'],
      queryFn: () => 'Hello',
    })),
  )

  // If your Angular version supports it, you can trigger effects:
  // TestBed.tick()

  await appRef.whenStable()

  expect(query.status()).toBe('success')
  expect(query.data()).toBe('Hello')
})
```