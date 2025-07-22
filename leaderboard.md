---
layout: default
title: "Top Contributors – Leaderboard"
description: "Top code review contributors across all Awesome Reviewers entries."
permalink: /leaderboard/
---

<section class="leaderboard-header">
  <div class="container">
    <h1>🏆 Top Contributors</h1>
    <p>These are the most active reviewers, ranked by the number of unique review entries they've contributed to.</p>
  </div>
</section>

<main class="main-content">
  <div class="container">
    <div class="sort-buttons">
      <button id="sort-entries" class="active">Sort by entries</button>
      <button id="sort-repos">Sort by repos</button>
    </div>
    <div class="reviewer-grid">
      {% assign top_contributors = site.data.leaderboard %}
      {% for contributor in top_contributors %}
      <div class="reviewer-card contributor-card" data-entries="{{ contributor.entries_count }}" data-repos="{{ contributor.repos_count }}">
        {% if forloop.index0 == 0 %}
          <span class="badge gold">🥇</span>
        {% elsif forloop.index0 == 1 %}
          <span class="badge silver">🥈</span>
        {% elsif forloop.index0 == 2 %}
          <span class="badge bronze">🥉</span>
        {% endif %}
        <img src="https://github.com/{{ contributor.user }}.png?size=80" alt="{{ contributor.user }}'s avatar" class="avatar">
        <a href="https://github.com/{{ contributor.user }}" target="_blank" class="username">@{{ contributor.user }}</a>
        <div class="contributor-stats">
          <span class="count">{{ contributor.entries_count }}</span> entries
          <span class="sep">•</span>
          <span class="repos">{{ contributor.repos_count }}</span> repos
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</main>
