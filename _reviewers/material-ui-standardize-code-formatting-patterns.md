---
title: Standardize code formatting patterns
description: 'Maintain consistent code formatting patterns across the codebase to
  improve readability and maintainability. This includes:


  1. Use consistent spacing and indentation'
repository: mui/material-ui
label: Code Style
language: Markdown
comments_count: 4
repository_stars: 96063
---

Maintain consistent code formatting patterns across the codebase to improve readability and maintainability. This includes:

1. Use consistent spacing and indentation
2. Group related code blocks logically
3. Break long lines for better readability
4. Use clear and descriptive naming

Example of good formatting:

```tsx
// Good: Clear organization and spacing
import React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  modularCssLayers: true,
});

export default function AppTheme({ children }: { children: React.ReactNode }) {
  return <ThemeProvider theme={theme}>{children}</ThemeProvider>;
}

// Bad: Inconsistent spacing and organization
import React from 'react'
import {createTheme,ThemeProvider} from '@mui/material/styles'
const theme=createTheme({modularCssLayers:true})
export default function AppTheme({children}:{children:React.ReactNode}){return(
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
)}
```

This pattern helps maintain code quality by:
- Making code easier to read and understand
- Reducing cognitive load during code reviews
- Facilitating easier maintenance and updates
- Promoting consistency across the team