---
title: Test behavior not implementation
description: Focus tests on user behavior and outcomes rather than implementation
  details. Structure tests to simulate real user interactions and verify expected
  results. This creates more robust tests that remain valid even when implementation
  changes.
repository: mui/material-ui
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 96063
---

Focus tests on user behavior and outcomes rather than implementation details. Structure tests to simulate real user interactions and verify expected results. This creates more robust tests that remain valid even when implementation changes.

Example:
```jsx
// Good - Simulates user behavior
const textbox = screen.getByRole('combobox');
await user.type(textbox, 'new value');
await user.keyboard('{ArrowDown}');
expect(screen.getByText('dropdown option')).to.be.visible;

// Avoid - Tests implementation details
expect(component.state.inputValue).to.equal('new value');
expect(component.state.isOpen).to.be.true;
```

Use testing-library's user-centric queries (getByRole, getByText) via the screen object rather than targeting DOM elements directly. When testing events, verify their effect rather than just their occurrence. This approach makes tests more maintainable and provides better confidence that components work correctly from the user's perspective.