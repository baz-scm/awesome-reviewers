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


[
  {
    "discussion_id": "2176624041",
    "pr_number": 55249,
    "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
    "created_at": "2025-07-01T07:19:26+00:00",
    "commented_code": "config.action_controller.perform_caching = true\n  <%- end -%>\n\n  # Cache assets for far-future expiry since they are all digest stamped.\n  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n  # Cache digest stamped assets for far-future expiry.\n  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n  config.public_file_server.headers = {\n    'cache-control' => lambda do |path, _|\n      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2176624041",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624041",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
        "comment_created_at": "2025-07-01T07:19:26+00:00",
        "comment_author": "byroot",
        "comment_body": "```suggestion\r\n      if path.start_with?(\"/assets/\")\r\n```\r\n\r\nI think just checking the directory is enough. If you put non-immutable assets in `/assets/` that's on you.",
        "pr_file_module": null
      },
      {
        "comment_id": "2176868216",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624041",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
        "comment_created_at": "2025-07-01T08:44:07+00:00",
        "comment_author": "thisismydesign",
        "comment_body": "What about `public/assets/.manifest.json`? Is there a downside to sticking with a more precise match? Seems like the safer option.",
        "pr_file_module": null
      },
      {
        "comment_id": "2176971130",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624041",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
        "comment_created_at": "2025-07-01T09:20:29+00:00",
        "comment_author": "byroot",
        "comment_body": "What's the use case for downloading it?",
        "pr_file_module": null
      },
      {
        "comment_id": "2176972516",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624041",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
        "comment_created_at": "2025-07-01T09:20:53+00:00",
        "comment_author": "byroot",
        "comment_body": "> Is there a downside to sticking with a more precise match?\r\n\r\nYes, the digest implementation may change, and the regexp stop matching.",
        "pr_file_module": null
      },
      {
        "comment_id": "2177078889",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624041",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)",
        "comment_created_at": "2025-07-01T09:57:01+00:00",
        "comment_author": "thisismydesign",
        "comment_body": "You're right, updated.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176624993",
    "pr_number": 55249,
    "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
    "created_at": "2025-07-01T07:19:54+00:00",
    "commented_code": "config.action_controller.perform_caching = true\n  <%- end -%>\n\n  # Cache assets for far-future expiry since they are all digest stamped.\n  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n  # Cache digest stamped assets for far-future expiry.\n  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n  config.public_file_server.headers = {\n    'cache-control' => lambda do |path, _|\n      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)\n        \"public, max-age=#{1.year.to_i}\"\n      else\n        \"public, max-age=#{1.hour.to_i}\"",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2176624993",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2176624993",
        "commented_code": "@@ -17,8 +17,17 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.match?(/\\A\\/assets\\/.*-[a-f0-9]{8,}[a-f0-9.]*$/)\n+        \"public, max-age=#{1.year.to_i}\"\n+      else\n+        \"public, max-age=#{1.hour.to_i}\"",
        "comment_created_at": "2025-07-01T07:19:54+00:00",
        "comment_author": "byroot",
        "comment_body": "```suggestion\r\n        \"public, max-age=#{1.hour.to_i}\"\r\n```\r\n\r\nYou can go even lower. 1 or 5 minutes just to avoid thundering herds should be plenty.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2177223048",
    "pr_number": 55249,
    "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
    "created_at": "2025-07-01T10:47:58+00:00",
    "commented_code": "config.action_controller.perform_caching = true\n  <%- end -%>\n\n  # Cache assets for far-future expiry since they are all digest stamped.\n  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n  # Cache digest stamped assets for far-future expiry.\n  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n  config.public_file_server.headers = {\n    'cache-control' => lambda do |path, _|\n      if path.start_with?(\"/assets/\")\n        # Files in /assets/ are expected to be fully immutable.\n        # If the content change the URL too.\n        \"public, immutable, max-age=#{1.year.to_i}\"\n      else\n        # For anything else we cache for 1 minute.\n        \"public, max-age=#{1.minute.to_i}, stale-while-revalidate=#{5.minutes.to_i}\"",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2177223048",
        "repo_full_name": "rails/rails",
        "pr_number": 55249,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2177223048",
        "commented_code": "@@ -17,8 +17,20 @@ Rails.application.configure do\n   config.action_controller.perform_caching = true\n   <%- end -%>\n \n-  # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  # Cache digest stamped assets for far-future expiry.\n+  # Short cache for others: robots.txt, sitemap.xml, 404.html, etc.\n+  config.public_file_server.headers = {\n+    'cache-control' => lambda do |path, _|\n+      if path.start_with?(\"/assets/\")\n+        # Files in /assets/ are expected to be fully immutable.\n+        # If the content change the URL too.\n+        \"public, immutable, max-age=#{1.year.to_i}\"\n+      else\n+        # For anything else we cache for 1 minute.\n+        \"public, max-age=#{1.minute.to_i}, stale-while-revalidate=#{5.minutes.to_i}\"",
        "comment_created_at": "2025-07-01T10:47:58+00:00",
        "comment_author": "byroot",
        "comment_body": "I improved the defaults with `immutable` and `stale-while-revalidate`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2105042681",
    "pr_number": 55109,
    "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
    "created_at": "2025-05-23T16:58:18+00:00",
    "commented_code": "<%- end -%>\n\n  # Cache assets for far-future expiry since they are all digest stamped.\n  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=3600\" }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2105042681",
        "repo_full_name": "rails/rails",
        "pr_number": 55109,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2105042681",
        "commented_code": "@@ -18,7 +16,7 @@ Rails.application.configure do\n   <%- end -%>\n \n   # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=3600\" }",
        "comment_created_at": "2025-05-23T16:58:18+00:00",
        "comment_author": "Earlopain",
        "comment_body": "This should be one year, not one hour",
        "pr_file_module": null
      },
      {
        "comment_id": "2105067269",
        "repo_full_name": "rails/rails",
        "pr_number": 55109,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt",
        "discussion_id": "2105042681",
        "commented_code": "@@ -18,7 +16,7 @@ Rails.application.configure do\n   <%- end -%>\n \n   # Cache assets for far-future expiry since they are all digest stamped.\n-  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=#{1.year.to_i}\" }\n+  config.public_file_server.headers = { \"cache-control\" => \"public, max-age=3600\" }",
        "comment_created_at": "2025-05-23T17:08:09+00:00",
        "comment_author": "grantbdev",
        "comment_body": "Oops, thanks!",
        "pr_file_module": null
      }
    ]
  }
]
