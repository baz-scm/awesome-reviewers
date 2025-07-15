---
title: Prevent XSS vulnerabilities
description: Never directly concatenate untrusted data (like user inputs or API responses)
  into HTML strings, as this creates cross-site scripting (XSS) vulnerabilities. Instead,
  create the HTML structure first, then populate content using safe DOM manipulation
  methods like jQuery's .text() or native JavaScript's .textContent that automatically
  escape special characters.
repository: kubeflow/kubeflow
label: Security
language: JavaScript
comments_count: 1
repository_stars: 15064
---

Never directly concatenate untrusted data (like user inputs or API responses) into HTML strings, as this creates cross-site scripting (XSS) vulnerabilities. Instead, create the HTML structure first, then populate content using safe DOM manipulation methods like jQuery's .text() or native JavaScript's .textContent that automatically escape special characters.

Example - Vulnerable code:
```javascript
innerHTML = '<div class="alert alert-warning">';
innerHTML += '<strong>Warning! </strong>' + data.log + ' </div>';
```

Example - Secure approach:
```javascript
// Create HTML structure
innerHTML = `
<div class="alert alert-warning">
    <span class="close" onclick="this.parentElement.style.display='none'">&times;</span>
    <strong>Warning!</strong><span class='warning-log'></span>
</div>`;

// Safely set the content
const $e = $("#error-msgs").html(innerHTML);
$('.warning-log', $e).text(data.log);
```
