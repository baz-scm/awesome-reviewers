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
    <div class="reviewer-grid">
      {% assign top_contributors = site.data.leaderboard %}
      {% for contributor in top_contributors %}
      {% assign info = site.data.contributors[contributor.user] %}
      <a href="#contrib-{{ contributor.user }}" class="reviewer-card contributor-card" id="contrib-card-{{ contributor.user }}">
        {% if forloop.index0 == 0 %}
          <span class="badge gold">🥇</span>
        {% elsif forloop.index0 == 1 %}
          <span class="badge silver">🥈</span>
        {% elsif forloop.index0 == 2 %}
          <span class="badge bronze">🥉</span>
        {% endif %}
        <div class="contributor-card-header">
          <img src="{{ info.avatar | default: 'https://github.com/' | append: contributor.user | append: '.png?size=80' }}" alt="{{ contributor.user }} avatar" class="avatar">
          <div class="contributor-card-meta">
            {% if info.name %}<h3 class="contributor-name">{{ info.name }}</h3>{% endif %}
            <p class="username">@{{ contributor.user }}</p>
            {% if info.bio %}<p class="contributor-bio">{{ info.bio }}</p>{% endif %}
            <div class="contributor-extra">
              {% if info.company %}<span class="company">🏢 {{ info.company }}</span>{% endif %}
              {% if info.location %}<span class="location">📍 {{ info.location }}</span>{% endif %}
            </div>
          </div>
        </div>
        <div class="contributor-counts">
          <div>⭐ {{ info.stats.repositories }}</div>
          <div>📄 {{ info.stats.entries }}</div>
          <div>💬 {{ info.stats.comments }}</div>
        </div>
      </a>
      {% endfor %}
    </div>
  </div>
</main>

{% for entry in site.data.leaderboard %}
{% assign user = entry.user %}
{% assign info = site.data.contributors[user] %}
<div id="contrib-{{ user }}" class="drawer">
  <a href="#" class="drawer-overlay"></a>
  <div class="drawer-panel">
    <div class="drawer-header">
      <a href="#" class="drawer-close">&times;</a>
    </div>
    <div class="drawer-body">
      <div class="drawer-profile">
        <img src="{{ info.avatar }}" class="drawer-avatar" alt="{{ user }} avatar">
        <div>
          <h2 class="drawer-title">@{{ user }}</h2>
          {% if info.name %}<div class="drawer-name">{{ info.name }}</div>{% endif %}
          {% if info.bio %}<div class="drawer-bio">{{ info.bio }}</div>{% endif %}
          <div class="drawer-meta">
            {% if info.company %}<span class="company">🏢 {{ info.company }}</span>{% endif %}
            {% if info.location %}<span class="location">📍 {{ info.location }}</span>{% endif %}
          </div>
        </div>
      </div>
      <div class="drawer-stats">
        <div class="stat">
          <div class="count">{{ info.stats.repositories }}</div>
          <div class="label">Repositories</div>
        </div>
        <div class="stat">
          <div class="count">{{ info.stats.entries }}</div>
          <div class="label">Entries</div>
        </div>
        <div class="stat">
          <div class="count">{{ info.stats.comments }}</div>
          <div class="label">Comments</div>
        </div>
      </div>
      <div class="drawer-section">
        <details open>
          <summary>Repositories</summary>
          <ul class="link-list">
          {% for repo in info.repos %}
            <li><a href="/?repo={{ repo | uri_escape }}" target="_blank" rel="noopener noreferrer">⭐ {{ repo }} ↗️</a></li>
          {% endfor %}
          </ul>
        </details>
      </div>
      <div class="drawer-section">
        <details open>
          <summary>Reviewer Entries</summary>
          <ul class="link-list">
          {% for e in info.entries %}
            <li><a href="/reviewers/{{ e.slug }}/" target="_blank" rel="noopener noreferrer">{{ e.title }} ↗️</a></li>
          {% endfor %}
          </ul>
        </details>
      </div>
      <div class="drawer-section">
        <details>
          <summary>Comments</summary>
          <div class="comment-groups">
          {% for pair in info.comments %}
            {% assign slug = pair[0] %}
            {% assign list = pair[1] %}
            {% assign entry = info.entries | where: 'slug', slug | first %}
            {% assign title = entry.title | default: slug %}
            <details class="comment-group">
              <summary>{{ title }}</summary>
              <ul>
                {% for text in list %}
                <li>{{ text }}</li>
                {% endfor %}
              </ul>
            </details>
          {% endfor %}
          </div>
        </details>
      </div>
    </div>
  </div>
</div>
{% endfor %}

