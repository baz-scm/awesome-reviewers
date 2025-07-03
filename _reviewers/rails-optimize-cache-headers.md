---
title: Optimize cache headers
description: Use appropriate HTTP cache headers based on content mutability. For immutable
  assets (like digest-stamped files), apply aggressive caching with far-future expiry
  and the immutable flag. For mutable files, use short cache times to balance between
  preventing thundering herds and allowing timely updates.
repository: rails/rails
label: Caching
language: Other
comments_count: 4
repository_stars: 57027
---

Use appropriate HTTP cache headers based on content mutability. For immutable assets (like digest-stamped files), apply aggressive caching with far-future expiry and the immutable flag. For mutable files, use short cache times to balance between preventing thundering herds and allowing timely updates.

**For immutable assets:**
```ruby
# Assets in /assets/ are expected to be immutable with content-based filenames
if path.start_with?("/assets/")
  "public, immutable, max-age=#{1.year.to_i}"
else
  "public, max-age=#{1.minute.to_i}, stale-while-revalidate=#{5.minutes.to_i}"
end
```

Prefer simple path-based checks over regex patterns when identifying asset types, as implementation details may change. For non-asset files like robots.txt or sitemap.xml, use very short cache times (1-5 minutes) with stale-while-revalidate to improve performance while ensuring content freshness.
