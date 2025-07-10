---
title: Use semantic HTML elements
description: Structure HTML templates using semantically appropriate elements rather
  than generic containers. Replace non-semantic elements like `<div>` and `<p>` with
  more meaningful elements such as `<nav>`, `<ol>`, `<ul>`, and include proper accessibility
  attributes like `aria-labelledby` and `aria-current`.
repository: django/django
label: Code Style
language: Html
comments_count: 5
repository_stars: 84182
---

Structure HTML templates using semantically appropriate elements rather than generic containers. Replace non-semantic elements like `<div>` and `<p>` with more meaningful elements such as `<nav>`, `<ol>`, `<ul>`, and include proper accessibility attributes like `aria-labelledby` and `aria-current`.

Example:
```html
<!-- Instead of this -->
<p class="paginator">
  {% for i in page_range %}
    {% if i == action_list.number %}
      <span class="this-page">{{ i }}</span>
    {% else %}
      <a href="?{{ page_var }}={{ i }}">{{ i }}</a>
    {% endif %}
  {% endfor %}
</p>

<!-- Use this -->
<nav class="paginator" aria-labelledby="pagination">
  <h2 id="pagination" class="visually-hidden">Pagination</h2>
  <ul>
    {% for i in page_range %}
      {% if i == action_list.number %}
        <li><span class="this-page" aria-current="page">{{ i }}</span></li>
      {% else %}
        <li><a href="?{{ page_var }}={{ i }}">{{ i }}</a></li>
      {% endif %}
    {% endfor %}
  </ul>
</nav>
```

This improves code organization and readability while enhancing accessibility for users with assistive technologies. Proper semantic structure also makes templates more maintainable as the code's purpose is clearer to other developers.