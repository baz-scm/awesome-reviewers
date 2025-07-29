---
title: Documentation clarity standards
description: Ensure technical documentation clearly distinguishes between similar
  but different concepts, uses precise language, and provides unambiguous explanations.
  When documenting Vue features, explicitly label and differentiate between reactive
  and non-reactive data, different directive behaviors, and component patterns.
repository: sveltejs/svelte
label: Vue
language: Markdown
comments_count: 4
repository_stars: 83580
---

Ensure technical documentation clearly distinguishes between similar but different concepts, uses precise language, and provides unambiguous explanations. When documenting Vue features, explicitly label and differentiate between reactive and non-reactive data, different directive behaviors, and component patterns.

Use clear, descriptive comments in code examples to highlight important distinctions:

```javascript
// reactive data - changes trigger re-renders
const reactiveUser = reactive({name: "Alice", age: 18});

// plain object - changes do not trigger re-renders  
const plainUser = {name: "Bob", age: 21};
```

Avoid ambiguous phrasing that could confuse readers about technical behavior. Choose words that clearly convey the intended meaning and relationship between concepts. Review documentation for grammatical errors and ensure consistent terminology throughout.