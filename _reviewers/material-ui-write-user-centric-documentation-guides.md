---
title: Write user-centric documentation guides
description: 'Documentation should be written with the user''s perspective in mind,
  using clear, action-oriented language and intuitive organization. Follow these principles:'
repository: mui/material-ui
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 96063
---

Documentation should be written with the user's perspective in mind, using clear, action-oriented language and intuitive organization. Follow these principles:

1. Use active voice and direct "you" statements instead of passive voice
2. Structure content with informative question-based headers that anticipate user needs
3. Provide complete, self-contained examples that can be copied and used directly
4. Write one sentence per line for better readability and maintainability

Example:

```diff
- ## Overview
- The component can be configured with various options that are found in the API documentation.
+ ## How do I configure the component?
+ You can customize the component using these key options:
+ 
+ 1. Set the `variant` prop to change the visual style
+ 2. Use the `size` prop to adjust dimensions
+ 3. Add the `disabled` prop to control interactivity
+
+ ```jsx
+ // Complete, ready-to-use example
+ import { Button } from '@mui/material';
+ 
+ export default function CustomButton() {
+   return (
+     <Button
+       variant="contained"
+       size="large"
+       disabled={false}
+     >
+       Click me
+     </Button>
+   );
+ }
+ ```
```