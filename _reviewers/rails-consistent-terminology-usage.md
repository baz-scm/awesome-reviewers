---
title: Consistent terminology usage
description: Always use consistent terminology for the same concept throughout your
  codebase, documentation, and user interfaces. When multiple terms could describe
  the same thing, choose one definitive term and use it consistently everywhere.
repository: rails/rails
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 57027
---

Always use consistent terminology for the same concept throughout your codebase, documentation, and user interfaces. When multiple terms could describe the same thing, choose one definitive term and use it consistently everywhere.

For example, when referring to database configuration elements, don't alternate between calling them "configuration keys" and "connection names" - pick the most semantically accurate term (e.g., "connection name") and use it consistently:

```ruby
# GOOD:
# Connection URLs for non-primary databases can be configured using
# environment variables. The variable name is formed by concatenating the
# connection name with `_DATABASE_URL`.

# BAD:
# Similar environment variable prefixed with the configuration key...
# ...prefixed with the connection name...
# (Using inconsistent terminology for the same concept)
```

Terminology consistency reduces cognitive load for readers and maintainers, prevents confusion, and makes documentation more accessible. This principle applies equally to code comments, user-facing labels, and semantic HTML elements.


[
  {
    "discussion_id": "2001071505",
    "pr_number": 54765,
    "pr_file": "railties/lib/rails/generators/rails/app/templates/config/databases/mysql.yml.tt",
    "created_at": "2025-03-18T13:37:28+00:00",
    "commented_code": "#   production:\n#     url: <%%= ENV[\"MY_APP_DATABASE_URL\"] %>\n#\n<%- unless options.skip_solid? -%>\n# The connection URL for non-primary databases can also be configured using a\n# similar environment variable prefixed with the configuration key in uppercase.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2001071505",
        "repo_full_name": "rails/rails",
        "pr_number": 54765,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/databases/mysql.yml.tt",
        "discussion_id": "2001071505",
        "commented_code": "@@ -49,6 +49,14 @@ test:\n #   production:\n #     url: <%%= ENV[\"MY_APP_DATABASE_URL\"] %>\n #\n+<%- unless options.skip_solid? -%>\n+# The connection URL for non-primary databases can also be configured using a\n+# similar environment variable prefixed with the configuration key in uppercase.",
        "comment_created_at": "2025-03-18T13:37:28+00:00",
        "comment_author": "eileencodes",
        "comment_body": "It's more correct to refer to that key as the connection name, because it's 3-tier and the key is `development` and `animals`. I'm not trying to be pedantic but I'm particular about this because I don't want multiple names for the same thing in our docs.\r\n\r\n```suggestion\r\n# similar environment variable prefixed with the connection name appended to `DATABASE_URL`.\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2006439629",
        "repo_full_name": "rails/rails",
        "pr_number": 54765,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/databases/mysql.yml.tt",
        "discussion_id": "2001071505",
        "commented_code": "@@ -49,6 +49,14 @@ test:\n #   production:\n #     url: <%%= ENV[\"MY_APP_DATABASE_URL\"] %>\n #\n+<%- unless options.skip_solid? -%>\n+# The connection URL for non-primary databases can also be configured using a\n+# similar environment variable prefixed with the configuration key in uppercase.",
        "comment_created_at": "2025-03-20T20:53:58+00:00",
        "comment_author": "floehopper",
        "comment_body": "> It's more correct to refer to that key as the connection name, because it's 3-tier and the key is development and animals. I'm not trying to be pedantic but I'm particular about this because I don't want multiple names for the same thing in our docs.\r\n\r\nThat makes complete sense. However, I also find the revised version slightly confusing because it talks about both prefixing and appending. How about changing the original to this:\r\n\r\n```\r\n# Connection URLs for non-primary databases can also be configured using\r\n# environment variables. The variable name is formed by concatenating the\r\n# connection name with `_DATABASE_URL`. For example:\r\n#\r\n#   CACHE_DATABASE_URL=\"mysql2://cacheuser:cachepass@localhost/cachedatabase\"\r\n#\r\n```\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2007327178",
        "repo_full_name": "rails/rails",
        "pr_number": 54765,
        "pr_file": "railties/lib/rails/generators/rails/app/templates/config/databases/mysql.yml.tt",
        "discussion_id": "2001071505",
        "commented_code": "@@ -49,6 +49,14 @@ test:\n #   production:\n #     url: <%%= ENV[\"MY_APP_DATABASE_URL\"] %>\n #\n+<%- unless options.skip_solid? -%>\n+# The connection URL for non-primary databases can also be configured using a\n+# similar environment variable prefixed with the configuration key in uppercase.",
        "comment_created_at": "2025-03-21T10:50:18+00:00",
        "comment_author": "floehopper",
        "comment_body": "@eileencodes I've attempted to address your concerns in https://github.com/rails/rails/pull/54765/commits/689188a5a9d9e3f7d6b60a3958b84be865384335. Let me know what you think.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1554102769",
    "pr_number": 51499,
    "pr_file": "guides/source/layout.html.erb",
    "created_at": "2024-04-05T18:28:18+00:00",
    "commented_code": "</ul>\n    </div>\n  </nav>\n\n  <header id=\"page_header\">\n    <div class=\"wrapper clearfix\">\n      <nav id=\"feature_nav\">\n        <div class=\"header-logo\">\n          <a href=\"index.html\" title=\"Return to the Guides Home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n          <span id=\"version_switcher\">\n            Version:\n            <select class=\"guides-version\">\n          <a href=\"index.html\" title=\"Guides home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n          <span id=\"version_switcher\" class=\"js-only\">\n            <label for=\"version_switcher-select\">Version: <span class=\"sr-only\">pick from the list to go to that Rails version's guides</span></label>",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1554102769",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554102769",
        "commented_code": "@@ -44,14 +52,15 @@\n       </ul>\n     </div>\n   </nav>\n+\n   <header id=\"page_header\">\n     <div class=\"wrapper clearfix\">\n       <nav id=\"feature_nav\">\n         <div class=\"header-logo\">\n-          <a href=\"index.html\" title=\"Return to the Guides Home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n-          <span id=\"version_switcher\">\n-            Version:\n-            <select class=\"guides-version\">\n+          <a href=\"index.html\" title=\"Guides home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n+          <span id=\"version_switcher\" class=\"js-only\">\n+            <label for=\"version_switcher-select\">Version: <span class=\"sr-only\">pick from the list to go to that Rails version's guides</span></label>",
        "comment_created_at": "2024-04-05T18:28:18+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Why does this have a different text for screen reader users? This should not be necessary. If the text displayed is clear enough for both users, which in this case it is, we should not change the behavior of that.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557048843",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554102769",
        "commented_code": "@@ -44,14 +52,15 @@\n       </ul>\n     </div>\n   </nav>\n+\n   <header id=\"page_header\">\n     <div class=\"wrapper clearfix\">\n       <nav id=\"feature_nav\">\n         <div class=\"header-logo\">\n-          <a href=\"index.html\" title=\"Return to the Guides Home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n-          <span id=\"version_switcher\">\n-            Version:\n-            <select class=\"guides-version\">\n+          <a href=\"index.html\" title=\"Guides home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n+          <span id=\"version_switcher\" class=\"js-only\">\n+            <label for=\"version_switcher-select\">Version: <span class=\"sr-only\">pick from the list to go to that Rails version's guides</span></label>",
        "comment_created_at": "2024-04-09T07:03:19+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "I don't agree that the label version is enough for all users. It fails criteria 3.2.2 \"change of context\".\n\nI do agree that I rather have both visual and sr content to be the same but the design as is makes it look weird as mentioned by the comment.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557535742",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554102769",
        "commented_code": "@@ -44,14 +52,15 @@\n       </ul>\n     </div>\n   </nav>\n+\n   <header id=\"page_header\">\n     <div class=\"wrapper clearfix\">\n       <nav id=\"feature_nav\">\n         <div class=\"header-logo\">\n-          <a href=\"index.html\" title=\"Return to the Guides Home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n-          <span id=\"version_switcher\">\n-            Version:\n-            <select class=\"guides-version\">\n+          <a href=\"index.html\" title=\"Guides home for <%= @edge.present? ? 'Edge' : @version %> Guides\">Guides</a>\n+          <span id=\"version_switcher\" class=\"js-only\">\n+            <label for=\"version_switcher-select\">Version: <span class=\"sr-only\">pick from the list to go to that Rails version's guides</span></label>",
        "comment_created_at": "2024-04-09T12:15:34+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Well, so I think it's fine to leave it as it's. I didn't really have a very strong opinion on that either.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1556658844",
    "pr_number": 51499,
    "pr_file": "guides/source/layout.html.erb",
    "created_at": "2024-04-09T00:27:17+00:00",
    "commented_code": "<meta name=\"theme-color\" content=\"#C81418\">\n</head>\n\n<body dir=\"<%= @direction %>\" class=\"guide\">\n<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n  <script>\n    document.body.classList.remove('no-js')\n  </script>\n\n  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n    Skip to main content\n  </a>\n\n  <nav id=\"topNav\" aria-label=\"Secondary\">",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1556658844",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T00:27:17+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "I find this label quite confusing. Secondary of what? I'd remove it. It's pretty clear that it's a navigation region, I think that's enough.\r\n\r\n```suggestion\r\n  <nav id=\"topNav\">\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1557059689",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T07:10:26+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "It must have a label because it's not the primary navigation (otherwise it fails a wcag criterium), as there is already a primary navigation element.\n\nI hate the label \"secondary\" personally, do you have a different suggestion?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557531844",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:12:17+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "I understand that it's not the primary navigation, but when this element is shown, the element containing the primary navigation is hidden, so in theory this is the one that now becomes the primary navigation element. What do you think?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557539000",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:18:23+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "I think you are right. Okay my proposal will be to drop the label and instead add an ERB comment for the next developer that the navs are mutually exclusive and thus not actually secondary.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557542926",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:21:38+00:00",
        "comment_author": "jathayde",
        "comment_body": "Is the name something used for voice navigation or is it more to provide context? Perhaps \"global\" and \"chapter contents\" or some other delineation that alludes to the content?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557547303",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:25:18+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "In our screen readers it will do something along the lines of: \"Secondary navigation\". It must provide context. However, the \"primary\" (top) navigation is allowed to not have a contextual label. That's basically what we were discussing here.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557579598",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:50:47+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "@brunoprietog I actually think this can be made just a `div`. It's not a `nav` in the sense that it only holds a single button that expands a set of links. Do you agree?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557583105",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556658844",
        "commented_code": "@@ -28,14 +28,22 @@\n   <meta name=\"theme-color\" content=\"#C81418\">\n </head>\n \n-<body dir=\"<%= @direction %>\" class=\"guide\">\n+<body dir=\"<%= @direction %>\" class=\"guide no-js\">\n+  <script>\n+    document.body.classList.remove('no-js')\n+  </script>\n+\n+  <a id=\"main-skip-link\" href=\"#container\" class=\"skip-link\">\n+    Skip to main content\n+  </a>\n+\n   <nav id=\"topNav\" aria-label=\"Secondary\">",
        "comment_created_at": "2024-04-09T12:53:25+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Yes, I agree! The same thing crossed my mind for a moment.",
        "pr_file_module": null
      }
    ]
  }
]
