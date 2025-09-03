---
title: Improve code expressiveness
description: Write code that clearly communicates its intent through expressive method
  names and simplified control flow. Replace complex inline conditions with descriptive
  method calls that encapsulate the logic, and use early returns to reduce cyclomatic
  complexity and focus functions on their primary responsibility.
repository: cypress-io/cypress
label: Code Style
language: JSX
comments_count: 2
repository_stars: 48850
---

Write code that clearly communicates its intent through expressive method names and simplified control flow. Replace complex inline conditions with descriptive method calls that encapsulate the logic, and use early returns to reduce cyclomatic complexity and focus functions on their primary responsibility.

Key practices:
- Encapsulate complex conditions in well-named methods (e.g., `project.isBrowserState(Project.BROWSER_OPEN)` instead of `project.browserState === 'opened'`)
- Use early returns to handle edge cases first, allowing the main logic to be the focus
- Choose method names that clearly express what they check or do

Example:
```javascript
// Before: Complex inline condition
if (project.browserState === 'opened' || project.browserState === 'opening') {
  // main logic
}

// After: Expressive method encapsulation
if (project.isBrowserState(Project.BROWSER_OPENING, Project.BROWSER_OPEN)) {
  // main logic
}

// Before: Nested conditional logic
function _closeBrowserBtn() {
  if (this.props.project.browserState === 'opened') {
    return (
      <li className='close-browser'>
        // button JSX
      </li>
    )
  }
}

// After: Early return with expressive method
function _closeBrowserBtn() {
  if (!this.props.project.isBrowserState(Project.BROWSER_OPEN)) return null
  
  return (
    <li className='close-browser'>
      // button JSX  
    </li>
  )
}
```

This approach makes code more readable, maintainable, and self-documenting while reducing complexity.