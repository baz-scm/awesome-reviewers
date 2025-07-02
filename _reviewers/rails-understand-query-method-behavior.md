---
title: Understand query method behavior
description: When working with database queries in Active Record, it's essential to
  understand the precise behavior of query methods to avoid unexpected results and
  performance issues.
repository: rails/rails
label: Database
language: Markdown
comments_count: 4
repository_stars: 57027
---

When working with database queries in Active Record, it's essential to understand the precise behavior of query methods to avoid unexpected results and performance issues.

Key considerations:

1. **Method Override Behaviors**: Some methods replace previous configurations rather than augmenting them. For example, `pluck` ignores any previous `select` clauses:

```ruby
# This ignores the select(:email) - only id is selected
Customer.select(:email).pluck(:id)
# => SELECT "customers"."id" FROM customers

# For raw SQL in pluck, use Arel.sql:
Customer.pluck(Arel.sql("DISTINCT id"))
# => SELECT DISTINCT id FROM customers
```

2. **Query Merging Complexity**: When combining queries with `merge`, `or`, and `and`, be careful about how conditions are combined to avoid incorrect SQL generation:

```ruby
# Complex queries can generate unexpected SQL if not carefully constructed
base = Comment.joins(:post).where(user_id: 1).where("recent = 1")
base.merge(base.where(draft: true).or(Post.where(archived: true)))
```

3. **Index Usage Control**: For performance optimization, understand how to control which indexes are used in queries:

```ruby
# When using implicit_order_column with multiple columns
# Adding nil at the end prevents appending the primary key
add_index :users, [:created_at, :id], name: "optimal_recent_users_query"
User.implicit_order_column = [:created_at, nil] # Prevents adding id twice to ORDER BY
```

Carefully understanding these behaviors helps you write more predictable, efficient database queries and avoid unexpected results when refactoring.


[
  {
    "discussion_id": "1908615276",
    "pr_number": 54167,
    "pr_file": "activerecord/CHANGELOG.md",
    "created_at": "2025-01-09T11:30:45+00:00",
    "commented_code": "*   Fix `#merge` with `#or` or `#and` and a mixture of attributes and SQL strings resulting in an incorrect query.\n\n    ```ruby\n    base = Comment.joins(:post).where(user_id: 1).where(\"recent = 1\")\n    puts base.merge(base.where(draft: true).or(Post.where(archived: true))).to_sql\n    ```\n\n    Before:\n\n    ```SQL\n    SELECT \"comments\".* FROM \"comments\"\n    INNER JOIN \"posts\" ON \"posts\".\"id\" = \"comments\".\"post_id\"\n    WHERE (recent = 1)\n    AND (\n      \"comments\".\"user_id\" = 1\n      AND (recent = 1)\n      AND \"comments\".\"draft\" = 1\n      OR \"posts\".\"archived\" = 1\n    )\n    ```\n\n    After:\n\n    ```SQL\n    SELECT \"comments\".* FROM \"comments\"\n    INNER JOIN \"posts\" ON \"posts\".\"id\" = \"comments\".\"post_id\"\n    WHERE \"comments\".\"user_id\" = 1\n    AND (recent = 1)\n    AND (\n      \"comments\".\"user_id\" = 1\n      AND (recent = 1)\n      AND \"comments\".\"draft\" = 1\n      OR \"posts\".\"archived\" = 1\n    )",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1908615276",
        "repo_full_name": "rails/rails",
        "pr_number": 54167,
        "pr_file": "activerecord/CHANGELOG.md",
        "discussion_id": "1908615276",
        "commented_code": "@@ -1,3 +1,41 @@\n+*   Fix `#merge` with `#or` or `#and` and a mixture of attributes and SQL strings resulting in an incorrect query.\n+\n+    ```ruby\n+    base = Comment.joins(:post).where(user_id: 1).where(\"recent = 1\")\n+    puts base.merge(base.where(draft: true).or(Post.where(archived: true))).to_sql\n+    ```\n+\n+    Before:\n+\n+    ```SQL\n+    SELECT \"comments\".* FROM \"comments\"\n+    INNER JOIN \"posts\" ON \"posts\".\"id\" = \"comments\".\"post_id\"\n+    WHERE (recent = 1)\n+    AND (\n+      \"comments\".\"user_id\" = 1\n+      AND (recent = 1)\n+      AND \"comments\".\"draft\" = 1\n+      OR \"posts\".\"archived\" = 1\n+    )\n+    ```\n+\n+    After:\n+\n+    ```SQL\n+    SELECT \"comments\".* FROM \"comments\"\n+    INNER JOIN \"posts\" ON \"posts\".\"id\" = \"comments\".\"post_id\"\n+    WHERE \"comments\".\"user_id\" = 1\n+    AND (recent = 1)\n+    AND (\n+      \"comments\".\"user_id\" = 1\n+      AND (recent = 1)\n+      AND \"comments\".\"draft\" = 1\n+      OR \"posts\".\"archived\" = 1\n+    )",
        "comment_created_at": "2025-01-09T11:30:45+00:00",
        "comment_author": "joshuay03",
        "comment_body": "I've confirmed that we see this same structure if were were to use an attribute instead of the literal:\r\n\r\n```ruby\r\nbase = Comment.joins(:post).where(user_id: 1).where(recent: true)\r\n```\r\n\r\non both main and this branch.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2098392864",
    "pr_number": 55090,
    "pr_file": "guides/source/active_record_querying.md",
    "created_at": "2025-05-20T16:23:05+00:00",
    "commented_code": "Customer.where(id: 1).pick(:id)\n```\n\nNOTE: Be aware that `pluck` silently replaces any `select` clause, even when including syntax errors, even when including statements that would modify the query result. For example:\n\n```irb\nirb> Customer.select(:email).pluck(:id)\nSELECT \"customers\".\"id\" FROM customers\n\nirb> Customer.select(\"some_random_invalid_field\").pluck(:id)\nSELECT \"customers\".\"id\" FROM customers\n\nirb> Customer.select(\"DISTINCT id\").pluck(:id)\nSELECT \"customers\".\"id\" FROM customers\n```\n\nIf you need to use raw SQL, this is how you can do it:\n\n```irb\nirb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\nSELECT DISTINCT id FROM customers\n```",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2098392864",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098392864",
        "commented_code": "@@ -2427,6 +2427,26 @@ with:\n Customer.where(id: 1).pick(:id)\n ```\n \n+NOTE: Be aware that `pluck` silently replaces any `select` clause, even when including syntax errors, even when including statements that would modify the query result. For example:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+\n+irb> Customer.select(\"some_random_invalid_field\").pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+\n+irb> Customer.select(\"DISTINCT id\").pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```",
        "comment_created_at": "2025-05-20T16:23:05+00:00",
        "comment_author": "fatkodima",
        "comment_body": "This also needs to be placed under the `#pluck` section.\r\n\r\n```suggestion\r\nNOTE: Be aware that `pluck` ignores any previous `select` clauses:\r\n\r\n```irb\r\nirb> Customer.select(:email).pluck(:id)\r\nSELECT \"customers\".\"id\" FROM customers\r\n```\r\n\r\nIf you need to use raw SQL, this is how you can do it:\r\n\r\n```irb\r\nirb> Customer.pluck(Arel.sql(\"DISTINCT id\"))\r\nSELECT DISTINCT id FROM customers\r\n```\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2098841736",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098392864",
        "commented_code": "@@ -2427,6 +2427,26 @@ with:\n Customer.where(id: 1).pick(:id)\n ```\n \n+NOTE: Be aware that `pluck` silently replaces any `select` clause, even when including syntax errors, even when including statements that would modify the query result. For example:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+\n+irb> Customer.select(\"some_random_invalid_field\").pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+\n+irb> Customer.select(\"DISTINCT id\").pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```",
        "comment_created_at": "2025-05-20T20:42:14+00:00",
        "comment_author": "daffo",
        "comment_body": "this is definitely the wrong section, my bad \ud83d\ude15 \r\nhttps://github.com/rails/rails/pull/55090/commits/b43a9d62c9c2a07aad7c8c39987cb3a7ac19d5c2",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1982898874",
    "pr_number": 54679,
    "pr_file": "activerecord/CHANGELOG.md",
    "created_at": "2025-03-06T08:21:30+00:00",
    "commented_code": "*   Allow bypassing primary key/constraint addition in `implicit_order_column`\n\n    When specifying multiple columns in an array for `implicit_order_column`, adding\n    `nil` as the last element will prevent appending the primary key to order\n    conditions, thus improving performance for certain database queries.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1982898874",
        "repo_full_name": "rails/rails",
        "pr_number": 54679,
        "pr_file": "activerecord/CHANGELOG.md",
        "discussion_id": "1982898874",
        "commented_code": "@@ -1,3 +1,11 @@\n+*   Allow bypassing primary key/constraint addition in `implicit_order_column`\n+\n+    When specifying multiple columns in an array for `implicit_order_column`, adding\n+    `nil` as the last element will prevent appending the primary key to order\n+    conditions, thus improving performance for certain database queries.",
        "comment_created_at": "2025-03-06T08:21:30+00:00",
        "comment_author": "matthewd",
        "comment_body": "```suggestion\r\n    conditions, allowing more precise control over which indexes may be used by\r\n    generated queries, by accepting the risk of API misbehavior if the specified\r\n    columns are not fully unique.\r\n```\r\n\r\n(Not a firm specific suggestion, just a quick take at trying to concisely provide some detail on the \"performance\" point, while also clarifying why it's not a \"go fast\" mode that everyone should always use.)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1964182948",
    "pr_number": 54332,
    "pr_file": "activerecord/CHANGELOG.md",
    "created_at": "2025-02-20T18:59:26+00:00",
    "commented_code": "*   Support disabling use of index for queries for MySQL v8.0.0+ and MariaDB 10.6.0+\n\n    MySQL 8.0.0 added an option to disable indexes from being used by the query optimizer by making them \"invisible\". This allows the index to still be maintained and updated but no queries will be permitted to use it. This can be useful for adding new invisible indexes or making existing indexes invisible before dropping them to ensure queries are not negatively affected. See https://dev.mysql.com/blog-archive/mysql-8-0-invisible-indexes/ for more details.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1964182948",
        "repo_full_name": "rails/rails",
        "pr_number": 54332,
        "pr_file": "activerecord/CHANGELOG.md",
        "discussion_id": "1964182948",
        "commented_code": "@@ -1,3 +1,33 @@\n+*   Support disabling use of index for queries for MySQL v8.0.0+ and MariaDB 10.6.0+\n+\n+    MySQL 8.0.0 added an option to disable indexes from being used by the query optimizer by making them \"invisible\". This allows the index to still be maintained and updated but no queries will be permitted to use it. This can be useful for adding new invisible indexes or making existing indexes invisible before dropping them to ensure queries are not negatively affected. See https://dev.mysql.com/blog-archive/mysql-8-0-invisible-indexes/ for more details.",
        "comment_created_at": "2025-02-20T18:59:26+00:00",
        "comment_author": "gmcgibbon",
        "comment_body": "```suggestion\r\n    MySQL 8.0.0 added an option to disable indexes from being used by the query optimizer by making them\r\n    \"invisible\". This allows the index to still be maintained and updated but no queries will be permitted to use it.\r\n    This can be useful for adding new invisible indexes or making existing indexes invisible before dropping them\r\n    to ensure queries are not negatively affected.\r\n    See https://dev.mysql.com/blog-archive/mysql-8-0-invisible-indexes/ for more details.\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
