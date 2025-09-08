---
title: Use semantic HTML elements
description: When creating interactive components in React, use proper HTML semantic
  elements as the foundation, even when using styled-components. Interactive elements
  should be actual buttons, links, or form controls rather than generic divs or spans
  with click handlers.
repository: gravitational/teleport
label: React
language: TSX
comments_count: 2
repository_stars: 19109
---

When creating interactive components in React, use proper HTML semantic elements as the foundation, even when using styled-components. Interactive elements should be actual buttons, links, or form controls rather than generic divs or spans with click handlers.

Attach event handlers directly to the interactive element itself, not to child elements like icons or text. This ensures proper accessibility, keyboard navigation, and screen reader support.

Example of the issue:
```jsx
// Problematic - styled div with onClick on child
const PlayButton = styled.div`...`;
<PlayButton>
  <AdjustedPlay size="extra-large" onClick={handlePlay} />
</PlayButton>
```

Corrected approach:
```jsx
// Better - actual button element with onClick on the button
const PlayButton = styled.button`...`;
<PlayButton onClick={handlePlay}>
  <AdjustedPlay size="extra-large" />
</PlayButton>
```

This pattern applies to all interactive elements: use `<button>` for actions, `<a>` for navigation, `<input>` for form controls, etc. Styled-components should enhance semantic HTML, not replace it with generic containers.