---
title: Consistent Imports And Constants
description: 'Keep code style consistent by (1) avoiding redundant imports and (2)
  centralizing shared UI values.


  - Imports: Use only what you actually need. If the project uses the modern JSX transform,
  don’t import a default `React` namespace just for JSX.'
repository: opencut-app/opencut
label: Code Style
language: TSX
comments_count: 2
repository_stars: 81817
---

Keep code style consistent by (1) avoiding redundant imports and (2) centralizing shared UI values.

- Imports: Use only what you actually need. If the project uses the modern JSX transform, don’t import a default `React` namespace just for JSX.
  - Prefer:
    ```ts
    import { useEffect, useRef, useState } from "react";
    ```
- Constants: Don’t hardcode semantic or user-visible fallback values in multiple components. Define them once (e.g., in a `constants/` module) and import them everywhere.
  - Prefer:
    ```ts
    // constants/starCounts.ts
    export const STARS_LOADING_DISPLAY = "28k";

    // component
    import { STARS_LOADING_DISPLAY } from "@/constants/starCounts";

    const label = `${isLoading ? STARS_LOADING_DISPLAY : stars}+`;
    ```