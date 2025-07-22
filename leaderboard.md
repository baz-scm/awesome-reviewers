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
      <a href="#contrib-{{ contributor.user }}" class="reviewer-card contributor-card" id="contrib-card-{{ contributor.user }}">
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
    <div class="p-4 border-b">
      <div class="flex items-center space-x-3">
        <img src="https://github.com/{{ user }}.png?size=80" class="w-16 h-16 rounded-full" alt="{{ user }} avatar">
        <div>
          <h2 class="font-bold text-xl">@{{ user }}</h2>
          {% if info.name %}<div class="text-sm text-gray-700">{{ info.name }}</div>{% endif %}
          {% if info.bio %}<div class="text-sm text-gray-700">{{ info.bio }}</div>{% endif %}
          {% if info.company %}<div class="text-sm text-gray-700">🏢 {{ info.company }}</div>{% endif %}
          {% if info.location %}<div class="text-sm text-gray-700">📍 {{ info.location }}</div>{% endif %}
        </div>
      </div>
    </div>
    <div class="flex text-center divide-x divide-gray-200 my-4">
      <div class="flex-1">
        <div class="text-lg font-semibold">{{ info.repos | size }}</div>
        <div class="text-xs text-gray-600">Repositories</div>
      </div>
      <div class="flex-1">
        <div class="text-lg font-semibold">{{ info.entries | size }}</div>
        <div class="text-xs text-gray-600">Entries</div>
      </div>
      <div class="flex-1">
        {% assign comment_count = 0 %}
        {% for pair in info.comments %}
          {% assign comment_count = comment_count | plus: pair[1].size %}
        {% endfor %}
        <div class="text-lg font-semibold">{{ comment_count }}</div>
        <div class="text-xs text-gray-600">Comments</div>
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-semibold mb-2">Repositories</h3>
      <div class="space-y-2">
        {% for repo in info.repos %}
        <a href="/?repo={{ repo | uri_escape }}" target="_blank" rel="noopener noreferrer" class="block border rounded-md p-2 hover:bg-gray-50">⭐ {{ repo }} <span class="ml-1">↗️</span></a>
        {% endfor %}
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-semibold mb-2">Reviewer Entries</h3>
      <div class="space-y-2">
        {% for e in info.entries %}
        <a href="/reviewers/{{ e.slug }}/" target="_blank" rel="noopener noreferrer" class="block border rounded-md p-2 hover:bg-gray-50">{{ e.title }} <span class="ml-1">↗️</span></a>
        {% endfor %}
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-semibold mb-2">Comments</h3>
      <div>
        {% for pair in info.comments %}
          {% assign slug = pair[0] %}
          {% assign list = pair[1] %}
          {% assign entry = info.entries | where: 'slug', slug | first %}
          {% assign title = entry.title | default: slug %}
          <details class="border rounded-md p-2 mb-2">
            <summary class="cursor-pointer font-medium">{{ title }}</summary>
            <ul class="mt-2 ml-4 list-disc">
              {% for text in list %}
              <li class="mb-1">{{ text }}</li>
              {% endfor %}
            </ul>
          </details>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
{% endfor %}

