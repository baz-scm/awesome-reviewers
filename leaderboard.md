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
{% assign sorted = site.reviewers | sort: 'comments_count' | reverse %}
{% for r in sorted %}
  {
    "slug": "{{ r.slug }}",
    "title": "{{ r.title | escape }}",
    "comments": {{ r.comments_count }},
    "stars": {{ r.repository_stars }}
  }{% unless forloop.last %},{% endunless %}{% endfor %}
]
</script>

<!-- Include the leaderboard script -->
<script src="{{ '/assets/js/leaderboard.js' | relative_url }}"></script>
