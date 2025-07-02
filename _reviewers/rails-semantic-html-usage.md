---
title: Semantic HTML usage
description: 'Use HTML elements according to their semantic purpose to ensure proper
  accessibility and code organization. Choose elements based on their intended role,
  not just how they appear visually:'
repository: rails/rails
label: Code Style
language: Other
comments_count: 3
repository_stars: 57027
---

Use HTML elements according to their semantic purpose to ensure proper accessibility and code organization. Choose elements based on their intended role, not just how they appear visually:

1. Use `<nav>` only for sections containing navigation links, not for containers with single links or static content
2. Place `<footer>` appropriately within document structure (can be inside `<article>` or `<section>`)
3. Use `role="button"` for links that behave like buttons rather than navigation

Example of proper semantic structure:
```html
<main>
  <article>
    <header id="feature">
      <!-- article introduction -->
      <!-- chapter index / toc -->
    </header>   

    <!-- article contents with headings -->    

    <footer>
      <h2>Feedback</h2>
      <!-- feedback explanation -->
    </footer>
  </article>
</main>
```

When HTML semantics aren't consistently recognized by screen readers, add explicit ARIA roles and attributes to enhance accessibility. This improves both code organization and the experience for users of assistive technologies.


[
  {
    "discussion_id": "1554119475",
    "pr_number": 51499,
    "pr_file": "guides/source/layout.html.erb",
    "created_at": "2024-04-05T18:34:38+00:00",
    "commented_code": "</nav>\n    </div>\n  </header>\n\n  <hr class=\"hide\" />\n\n  <section id=\"feature\">\n    <div class=\"wrapper\">\n      <%= yield :header_section %>\n  <main id=\"container\">\n    <article>\n      <header id=\"feature\">\n        <div class=\"wrapper\">\n          <%= yield :header_section %>\n\n      <%= yield :index_section %>\n          <%= yield :index_section %>\n        </div>\n      </header>\n\n      <hr>\n    </div>\n  </section>\n      <div class=\"wrapper\">\n        <div id=\"mainCol\">\n          <section id=\"article-body\">\n            <%= yield %>\n          </section>\n\n  <main id=\"container\">\n    <div class=\"wrapper\">\n      <div id=\"mainCol\">\n        <%= yield %>\n        <hr>\n        <h3>Feedback</h3>\n        <p>\n          You're encouraged to help improve the quality of this guide.\n        </p>\n        <p>\n          Please contribute if you see any typos or factual errors.\n          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n        </p>\n        <p>\n          You may also find incomplete content or stuff that is not up to date.\n          Please do add any missing documentation for main. Make sure to check\n          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n          if the issues are already fixed or not on the main branch.\n          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n          for style and conventions.\n        </p>\n        <p>\n          If for whatever reason you spot something to fix but cannot patch it yourself, please\n          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n        </p>\n        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n        </p>\n          <hr>\n\n          <footer aria-labelledby=\"heading-feedback\">",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1554119475",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-05T18:34:38+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "This should not be a footer. The footer should only be the one below the main element. In fact, when a footer is included inside the main element NVDA doesn't recognize it as such either, and even the h3 is already more than enough to indicate that it is a feedback section, which makes it somewhat repetitive.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557051680",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T07:05:24+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "In html 5, footer may also be an element inside an article or section. I experience the same behaviour as you (because I also use NVDA when I use a screen reader) but I believe jaws does denote it differently.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557543733",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T12:22:17+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Oh, I don't know. I'm not too convinced about adding so many additional regions beyond the navigation, main region and footer. It adds a lot of noise that is already covered by the heading levels and becomes a bit repetitive information.\r\n\r\nBy the way, I personally don't tend to use many links to skip to specific sections and hope this can be done natively. And really, there's no way to skip to the body of the article with a command to go to a region. You can easily use 2, but that makes me think we're not being very consistent with using regions, or if we're even using them properly.\r\n\r\nWhat do you think?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557576138",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T12:48:08+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "My personal thoughts here were:\r\n\r\n- I am browsing the guides extensively\r\n- I am in the middle of the article and find something I want to give feedback on\r\n- I know there is a _region_ (labelled section) that explains how to give feedback\r\n- I want to go there straight away\r\n\r\nWith NVDA I can get there right away when browsing the article pressing <kbd>D</kbd>, which should navigate to the next landmark or region. In this case the footer is nested inside article, and thus not _complementary_, but it is labelled by the heading, and thus it becomes a section with role=\"region\", iirc. Using the TOC navigation here would be sub-optimal as it doesn't allow be to go to \"last heading of the current level\", by pressing <kbd>2</kbd>. I would need to press it repeatedly, right? Since there are so little regions, that's not the case.\r\n\r\nDoes this make sense?",
        "pr_file_module": null
      },
      {
        "comment_id": "1557588925",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T12:57:42+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "That might make sense, but then, we would also have to have a region for the article, right? To get back quickly, at least to the beginning of the article.\r\n\r\nActually, this shouldn't be a problem with the article element, but unfortunately it hasn't worked in Chromium and NVDA for a while now.\r\n\r\nAnd in the case of the feedback region, I guess we would have to give it the role=\"region\" explicitly, since NVDA doesn't recognize it either because it's a footer inside a main element.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557594136",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T13:01:21+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "We have a region for the article: https://github.com/rails/rails/pull/51499/files/93f9819c62890301f398e752b6083c9d2c9f6c40#diff-dc279d925a05373ac5f34307441799f98ac4accbe0b0a8f12f99f703585afa7dR113 Is that not working for you? I haven't tested mine but I can.\r\n\r\nIt _should_ be:\r\n\r\n```html\r\n<main>\r\n  <article>\r\n\r\n    <header id=\"feature\">\r\n      article introduction\r\n\r\n      chapter index / toc\r\n    </header>   \r\n\r\n    article contents with lots of headings    \r\n\r\n    <footer>\r\n     <h2>Feedback</h2>\r\n\r\n     feedback explanation\r\n    </footer>\r\n  </article>\r\n</main>\r\n```\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1557595145",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T13:02:09+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "(sidenote: I am fine with explicit role-ing things if SRs don't recognise it, so let's do that if we must)",
        "pr_file_module": null
      },
      {
        "comment_id": "1557603577",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T13:08:34+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Right! So I think assigning the explicit roles would be enough to solve this.\r\n\r\nIn any case, an article is not exposed as a region, it's exposed as another type of element. In fact, at least in NVDA, there's no default shortcut to jump to it, I configured the A to do so but it's not the common case.",
        "pr_file_module": null
      },
      {
        "comment_id": "1557622932",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T13:22:14+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "Cool! Yeah, I _love_ different support for different SRs and even different versions of the same SR \ud83d\udde1\ufe0f \ud83d\ude01. \r\n\r\nI'll explicitly role both the article header and article footer (so your NVDA can skip back/forth to them)\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1557636426",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1554119475",
        "commented_code": "@@ -94,48 +106,54 @@\n       </nav>\n     </div>\n   </header>\n+\n   <hr class=\"hide\" />\n \n-  <section id=\"feature\">\n-    <div class=\"wrapper\">\n-      <%= yield :header_section %>\n+  <main id=\"container\">\n+    <article>\n+      <header id=\"feature\">\n+        <div class=\"wrapper\">\n+          <%= yield :header_section %>\n \n-      <%= yield :index_section %>\n+          <%= yield :index_section %>\n+        </div>\n+      </header>\n \n-      <hr>\n-    </div>\n-  </section>\n+      <div class=\"wrapper\">\n+        <div id=\"mainCol\">\n+          <section id=\"article-body\">\n+            <%= yield %>\n+          </section>\n \n-  <main id=\"container\">\n-    <div class=\"wrapper\">\n-      <div id=\"mainCol\">\n-        <%= yield %>\n-        <hr>\n-        <h3>Feedback</h3>\n-        <p>\n-          You're encouraged to help improve the quality of this guide.\n-        </p>\n-        <p>\n-          Please contribute if you see any typos or factual errors.\n-          To get started, you can read our <%= link_to 'documentation contributions', 'https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation' %> section.\n-        </p>\n-        <p>\n-          You may also find incomplete content or stuff that is not up to date.\n-          Please do add any missing documentation for main. Make sure to check\n-          <%= link_to 'Edge Guides', 'https://edgeguides.rubyonrails.org' %> first to verify\n-          if the issues are already fixed or not on the main branch.\n-          Check the <%= link_to 'Ruby on Rails Guides Guidelines', 'ruby_on_rails_guides_guidelines.html' %>\n-          for style and conventions.\n-        </p>\n-        <p>\n-          If for whatever reason you spot something to fix but cannot patch it yourself, please\n-          <%= link_to 'open an issue', 'https://github.com/rails/rails/issues' %>.\n-        </p>\n-        <p>And last but not least, any kind of discussion regarding Ruby on Rails\n-          documentation is very welcome on the <%= link_to 'official Ruby on Rails Forum', 'https://discuss.rubyonrails.org/c/rubyonrails-docs' %>.\n-        </p>\n+          <hr>\n+\n+          <footer aria-labelledby=\"heading-feedback\">",
        "comment_created_at": "2024-04-09T13:30:53+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "Yes, sadly. Just like the history of browser feature compatibility \ud83d\ude30",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1556511957",
    "pr_number": 51499,
    "pr_file": "guides/source/index.html.erb",
    "created_at": "2024-04-08T23:00:31+00:00",
    "commented_code": "<% content_for :index_section do %>\n<nav id=\"subCol\" aria-label=\"Chapter\" class=\"guide-index\">",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1556511957",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/index.html.erb",
        "discussion_id": "1556511957",
        "commented_code": "@@ -7,6 +7,10 @@\n \n <% content_for :index_section do %>\n <nav id=\"subCol\" aria-label=\"Chapter\" class=\"guide-index\">",
        "comment_created_at": "2024-04-08T23:00:31+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "This doesn't seem right to me, it's not a navigation container. It only has a link to skip to the body of the article and text. It also doesn't contain the chapter as it makes it appear by reading the aria-label.\r\n\r\n```suggestion\r\n<div id=\"subCol\" class=\"guide-index\">\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1557055259",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/index.html.erb",
        "discussion_id": "1556511957",
        "commented_code": "@@ -7,6 +7,10 @@\n \n <% content_for :index_section do %>\n <nav id=\"subCol\" aria-label=\"Chapter\" class=\"guide-index\">",
        "comment_created_at": "2024-04-09T07:08:03+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "Yeah I agree. It believe the choice was made to have it as nav because on articles it does contain links but on the index it doesn't.\n\nLet's change it here.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1556661283",
    "pr_number": 51499,
    "pr_file": "guides/source/layout.html.erb",
    "created_at": "2024-04-09T00:30:33+00:00",
    "commented_code": "<ul class=\"nav\">\n          <li><a class=\"nav-item\" id=\"home_nav\" href=\"https://rubyonrails.org/\">Home</a></li>\n          <li class=\"guides-index guides-index-large\">\n            <a href=\"index.html\" id=\"guidesMenu\" class=\"guides-index-item nav-item\">Guides Index</a>\n            <a href=\"index.html\" id=\"guidesMenu\" aria-controls=\"guides\" aria-expanded=\"false\" class=\"guides-index-item nav-item\">Guides Index</a>",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1556661283",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556661283",
        "commented_code": "@@ -62,7 +71,7 @@\n         <ul class=\"nav\">\n           <li><a class=\"nav-item\" id=\"home_nav\" href=\"https://rubyonrails.org/\">Home</a></li>\n           <li class=\"guides-index guides-index-large\">\n-            <a href=\"index.html\" id=\"guidesMenu\" class=\"guides-index-item nav-item\">Guides Index</a>\n+            <a href=\"index.html\" id=\"guidesMenu\" aria-controls=\"guides\" aria-expanded=\"false\" class=\"guides-index-item nav-item\">Guides Index</a>",
        "comment_created_at": "2024-04-09T00:30:33+00:00",
        "comment_author": "brunoprietog",
        "comment_body": "What do you think about giving a button role to this link? It's not really navigating to any page, and that's the only purpose of a link actually. (Unless JavaScript is disabled, in which case it shouldn't have those other ARIA attributes either if that's the case).\r\n\r\n```suggestion\r\n            <a href=\"index.html\" id=\"guidesMenu\" role=\"button\" aria-controls=\"guides\" aria-expanded=\"false\" class=\"guides-index-item nav-item\">Guides Index</a>\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1557061864",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556661283",
        "commented_code": "@@ -62,7 +71,7 @@\n         <ul class=\"nav\">\n           <li><a class=\"nav-item\" id=\"home_nav\" href=\"https://rubyonrails.org/\">Home</a></li>\n           <li class=\"guides-index guides-index-large\">\n-            <a href=\"index.html\" id=\"guidesMenu\" class=\"guides-index-item nav-item\">Guides Index</a>\n+            <a href=\"index.html\" id=\"guidesMenu\" aria-controls=\"guides\" aria-expanded=\"false\" class=\"guides-index-item nav-item\">Guides Index</a>",
        "comment_created_at": "2024-04-09T07:11:22+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "I like it. \n\nLet's apply it in JavaScript so it's only a button if... It's a button \ud83d\ude01",
        "pr_file_module": null
      },
      {
        "comment_id": "1557567577",
        "repo_full_name": "rails/rails",
        "pr_number": 51499,
        "pr_file": "guides/source/layout.html.erb",
        "discussion_id": "1556661283",
        "commented_code": "@@ -62,7 +71,7 @@\n         <ul class=\"nav\">\n           <li><a class=\"nav-item\" id=\"home_nav\" href=\"https://rubyonrails.org/\">Home</a></li>\n           <li class=\"guides-index guides-index-large\">\n-            <a href=\"index.html\" id=\"guidesMenu\" class=\"guides-index-item nav-item\">Guides Index</a>\n+            <a href=\"index.html\" id=\"guidesMenu\" aria-controls=\"guides\" aria-expanded=\"false\" class=\"guides-index-item nav-item\">Guides Index</a>",
        "comment_created_at": "2024-04-09T12:41:31+00:00",
        "comment_author": "SleeplessByte",
        "comment_body": "In dfc0d32e9c",
        "pr_file_module": null
      }
    ]
  }
]
