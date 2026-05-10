---
title: Declarative Vue Component Data
description: 'In Vue SFCs, keep templates declarative and driven by explicit data.


  **Rules**

  1. **Put static/config data in `<script setup>`**: define typed constants/arrays
  in the script rather than building or embedding data via template expressions.'
repository: mermaid-js/mermaid
label: Vue
language: Other
comments_count: 3
repository_stars: 87952
---

In Vue SFCs, keep templates declarative and driven by explicit data.

**Rules**
1. **Put static/config data in `<script setup>`**: define typed constants/arrays in the script rather than building or embedding data via template expressions.
2. **Avoid `v-for` positional logic (`index`) for styling/behavior**: instead, add an explicit property on each item (e.g., `highlighted: true`) and base `:class`/conditional rendering on that.
3. **For interactive UI, keep template hints clear and aligned with behavior**: keyboard shortcut labels should be accurate and use appropriate semantics/markup (even if styling choices require minor CSS adjustments).

**Example (data-driven, no `index`)**
```vue
<script setup lang="ts">
import { ref } from 'vue';

interface Feature { iconUrl: string; featureName: string; }
interface Column {
  title: string;
  description: string;
  redirectUrl: string;
  highlighted?: boolean;
  features: Feature[];
}

const editorColumns: Column[] = [
  {
    title: 'Playground',
    description: 'Basic features, no login',
    redirectUrl: 'https://www.mermaidchart.com/play',
    features: [
      { iconUrl: '/icons/icon-public.svg', featureName: 'Diagram stored in URL' },
      { iconUrl: '/icons/icon-terminal.svg', featureName: 'Code editor' },
      { iconUrl: '/icons/icon-whiteboard.svg', featureName: 'Whiteboard' },
    ],
  },
  {
    title: 'Free',
    description: 'Advanced features, free account',
    redirectUrl: 'https://www.mermaidchart.com/app/sign-up',
    highlighted: true,
    features: [
      { iconUrl: '/icons/icon-folder.svg', featureName: 'Storage' },
      { iconUrl: '/icons/icon-terminal.svg', featureName: 'Code editor' },
    ],
  },
];

const isVisible = ref(false);
</script>

<template>
  <div v-if="isVisible" @click.self="isVisible = false">
    <div class="flex gap-4">
      <div
        v-for="col in editorColumns"
        :key="col.title"
        class="w-80 p-6 m-6 shadow-sm"
        :class="col.highlighted ? 'bg-white' : 'bg-[#dceef1]'"
      >
        <h3>{{ col.title }}</h3>
        <p>{{ col.description }}</p>
      </div>
    </div>
  </div>
</template>
```

This improves maintainability (template changes don’t silently break styling order) and makes behavior more testable and reviewable.