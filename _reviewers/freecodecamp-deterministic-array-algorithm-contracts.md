---
title: Deterministic Array Algorithm Contracts
description: 'For algorithm-heavy code that transforms arrays (multi-step pipelines,
  scheduling, deduping, cyclic traversal), require clear, testable function contracts
  and deterministic behavior:'
repository: freeCodeCamp/freeCodeCamp
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 444449
---

For algorithm-heavy code that transforms arrays (multi-step pipelines, scheduling, deduping, cyclic traversal), require clear, testable function contracts and deterministic behavior:

- **Input validation upfront**: if the input type/shape is invalid, return the specified neutral value immediately (often `[]`).
- **Pure transformations**: each helper should return a **new array** (and avoid mutating inputs) while adding or deriving only the fields required by the next step.
- **Deterministic ordering rules**: when deduplicating, define whether you keep the **first/earliest** occurrence (stable dedupe). When building schedules/orders, compute positions deterministically (e.g., 1-based `slot`).
- **Correct cyclic indexing**: when iterating through an array circularly, use modulo for wraparound: `nextIndex = (currentIndex + 1) % array.length`.

Example pattern (flatten → score → stable dedupe):
```js
function flattenPlaylists(playlists) {
  if (!Array.isArray(playlists)) return [];

  const out = [];
  playlists.forEach((pl, playlistIndex) => {
    if (!Array.isArray(pl)) return;
    pl.forEach((track, trackIndex) => {
      out.push({
        ...track,
        source: [playlistIndex, trackIndex],
      });
    });
  });
  return out;
}

function scoreTracks(tracks) {
  return tracks.map(t => ({
    ...t,
    score: t.votes * 10 - Math.abs(t.bpm - 120),
  }));
}

function dedupeTracks(tracks) {
  const seen = new Set();
  const out = [];
  for (const t of tracks) {
    if (seen.has(t.trackId)) continue;
    seen.add(t.trackId);
    out.push(t);
  }
  return out; // keeps the earliest occurrence
}
```

Apply this standard anytime you see multi-step array algorithms or any logic depending on order/cycles—make those rules explicit in the functions’ behavior.