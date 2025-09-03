---
title: Test network performance
description: Always validate network performance and connectivity before suggesting
  alternative endpoints or making routing decisions. Implement timeout-based checks
  to ensure alternatives are actually faster or more accessible for the user's specific
  network conditions.
repository: ant-design/ant-design
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 95882
---

Always validate network performance and connectivity before suggesting alternative endpoints or making routing decisions. Implement timeout-based checks to ensure alternatives are actually faster or more accessible for the user's specific network conditions.

When offering mirror sites, CDN alternatives, or fallback endpoints, first test the current connection quality and the proposed alternative's performance. This prevents suggesting slower alternatives to users who may have different network conditions (e.g., overseas users accessing domestic mirrors).

Example implementation:
```javascript
function checkMirrorAvailable(timeout = 1500) {
  return new Promise((resolve) => {
    const img = new Image();
    let done = false;
    img.onload = () => {
      if (!done) {
        done = true;
        resolve(true);
      }
    };
    img.onerror = () => {
      if (!done) {
        done = true;
        resolve(false);
      }
    };
    img.src = `https://mirror.example.com/test-resource?_t=${Date.now()}`;
    setTimeout(() => {
      if (!done) {
        done = true;
        resolve(false);
      }
    }, timeout);
  });
}
```

This approach ensures network routing decisions are based on actual performance data rather than assumptions about user location or network conditions.