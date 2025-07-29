---
title: Complete code examples
description: Ensure all code examples are complete, functional, and accurately demonstrate
  the intended concepts. Code examples should include all necessary imports, variable
  declarations, and interactive elements to be self-contained and runnable.
repository: sveltejs/svelte
label: Code Style
language: Markdown
comments_count: 4
repository_stars: 83580
---

Ensure all code examples are complete, functional, and accurately demonstrate the intended concepts. Code examples should include all necessary imports, variable declarations, and interactive elements to be self-contained and runnable.

Key requirements:
- Include all necessary imports at the top of examples
- Declare all variables used in the example (e.g., `let visible = $state(false);`)
- Add interactive elements when demonstrating dynamic behavior (e.g., checkboxes to toggle state)
- Ensure syntax matches the concept being demonstrated (avoid quotes when showing unquoted syntax)
- Make examples functional rather than just illustrative fragments

Example of a complete code example:
```svelte
<script>
  import { fade, fly } from 'svelte/transition';
  
  let visible = $state(false);
</script>

<label>
  <input type="checkbox" bind:checked={visible}>
  visible
</label>

{#if visible}
  <div in:fly={{ y: 200, duration: 2000 }} out:fade>
    flies in, fades out
  </div>
{/if}
```

This approach helps developers understand the full context and makes examples immediately usable for learning and testing.