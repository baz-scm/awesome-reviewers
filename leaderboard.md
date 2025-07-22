---
layout: default
title: Leaderboard
permalink: /leaderboard/
---
<div class="leaderboard-container">
  <h1>Top Reviewers</h1>
  <div id="leaderboard"></div>
</div>

<!-- Embed the reviewer stats JSON -->
<script id="review-data" type="application/json">
[
{% raw %}{% assign sorted = site.reviewers | sort: 'comments_count' | reverse %}{% endraw %}
{% raw %}{% for r in sorted %}{% endraw %}
  {
    "slug": "{{ r.basename }}",
    "title": "{{ r.title | escape }}",
    "comments": {{ r.comments_count }},
    "stars": {{ r.repository_stars }}
  }{% raw %}{% unless forloop.last %},{% endunless %}{% endfor %}{% endraw %}
]
</script>

<!-- Include the leaderboard script -->
<script src="{{ '/assets/js/leaderboard.js' | relative_url }}"></script>
