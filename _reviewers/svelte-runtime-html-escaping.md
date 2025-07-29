---
title: Runtime HTML escaping
description: HTML escaping must occur at runtime, not during compilation or build
  time, to properly prevent XSS vulnerabilities. When content is escaped too early
  in the process, it may not account for dynamic values or runtime context that could
  introduce security risks.
repository: sveltejs/svelte
label: Security
language: JavaScript
comments_count: 2
repository_stars: 83580
---

HTML escaping must occur at runtime, not during compilation or build time, to properly prevent XSS vulnerabilities. When content is escaped too early in the process, it may not account for dynamic values or runtime context that could introduce security risks.

Compile-time escaping can miss dynamic content that gets injected at runtime, leaving applications vulnerable to XSS attacks. Always ensure that HTML escaping functions are called when the content is actually being rendered or output.

Example of incorrect approach (escaping at compile time):
```javascript
// DON'T: Escaping template quasis at compile time
export function escape_template_quasis(template, is_attr) {
    walk(template, {}, {
        TemplateLiteral(node, { next }) {
            for (let quasi of node.quasis) {
                quasi.value.raw = escape_html(quasi.value.raw, is_attr);
            }
            next();
        }
    });
}
```

Instead, ensure escaping happens when content is rendered:
```javascript
// DO: Import and use runtime escaping
import { escape_html } from '../../../escaping.js';

// Apply escaping when content is actually output/rendered
function renderContent(dynamicContent) {
    return escape_html(dynamicContent);
}
```