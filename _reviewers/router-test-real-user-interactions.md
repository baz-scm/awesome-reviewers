---
title: test real user interactions
description: Write tests that simulate actual user behavior and verify real rendering
  outcomes rather than testing implementation details or internal state. Use `data-testid`
  attributes with `getByTestId` instead of `getByRole` for better maintainability,
  as it allows changing text and HTML structure without breaking tests. Focus on testing
  what users actually see and...
repository: TanStack/router
label: Testing
language: TSX
comments_count: 4
repository_stars: 11590
---

Write tests that simulate actual user behavior and verify real rendering outcomes rather than testing implementation details or internal state. Use `data-testid` attributes with `getByTestId` instead of `getByRole` for better maintainability, as it allows changing text and HTML structure without breaking tests. Focus on testing what users actually see and interact with on screen.

For user interactions, test real events like hover, focus, and click behaviors:

```tsx
// Good: Test actual rendering and user interaction
test('when user hovers over link, it preloads route', async () => {
  const router = createRouter({ 
    routeTree, 
    defaultPreload: 'intent' 
  })
  
  render(<RouterProvider router={router} />)
  
  const link = screen.getByTestId('posts-link')
  
  // Test real user interaction
  fireEvent.focus(link)
  
  // Verify actual rendering outcome
  expect(await screen.findByRole('heading', { name: 'Posts' }))
    .toBeInTheDocument()
})

// Avoid: Testing only internal state
test('loader function gets called', () => {
  expect(mockLoader).toHaveBeenCalled() // Less valuable
})
```

Always verify that components actually render on screen using testing-library queries, and test edge cases like different router configurations (e.g., with `basePath` set) to ensure comprehensive real-world coverage.