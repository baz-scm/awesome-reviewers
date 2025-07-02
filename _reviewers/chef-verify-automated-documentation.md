---
title: Verify automated documentation
description: When using automated tools to generate documentation, always verify the
  output for accuracy and document any additional manual steps required for completion.
  Automated documentation can inherit incorrect properties or miss crucial steps in
  the process.
repository: chef/chef
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 7860
---

When using automated tools to generate documentation, always verify the output for accuracy and document any additional manual steps required for completion. Automated documentation can inherit incorrect properties or miss crucial steps in the process.

For example:
- When running tools like `rake docs_site:resources` that generate resource documentation automatically, review the output to ensure resources that inherit from parent resources don't contain properties or actions that don't apply to them.
- When using scripts like `publish-release-notes.sh` that push content to repositories, document the complete process including any subsequent manual steps (like triggering Netlify rebuilds) required for the documentation to become visible to users.

Document both the automation commands and their limitations to ensure team members understand the complete documentation workflow. This prevents confusion and ensures accurate, complete documentation reaches the end users.


[
  {
    "discussion_id": "1064755765",
    "pr_number": 13484,
    "pr_file": "docs/dev/how_to/releasing_chef_infra.md",
    "created_at": "2023-01-09T15:18:02+00:00",
    "commented_code": "If there are any new or updated resources, the docs site will need to be updated. This is a `partially` automated process. If you are making a single resource update or changing wording, it may just be easier to do it by hand.\n\n`publish-release-notes.sh` pushes to S3 and then Netlify site needs to be rebuilt, so the Docs Site may not immediately. Reach out to the Docs team to trigger an update.",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1064755765",
        "repo_full_name": "chef/chef",
        "pr_number": 13484,
        "pr_file": "docs/dev/how_to/releasing_chef_infra.md",
        "discussion_id": "1064755765",
        "commented_code": "@@ -28,23 +28,26 @@ The importance of our release notes cannot be understated. As developers, we und\n \n If there are any new or updated resources, the docs site will need to be updated. This is a `partially` automated process. If you are making a single resource update or changing wording, it may just be easier to do it by hand.\n \n+`publish-release-notes.sh` pushes to S3 and then Netlify site needs to be rebuilt, so the Docs Site may not immediately. Reach out to the Docs team to trigger an update.",
        "comment_created_at": "2023-01-09T15:18:02+00:00",
        "comment_author": "PrajaktaPurohit",
        "comment_body": "```suggestion\r\n`publish-release-notes.sh` pushes to S3 and then Netlify site needs to be rebuilt, so the Docs Site may not immediately reflect the Release notes related updates. The way to rebuild Netlify is manually or by merging a PR in chef-web-docs repository. Reach out to the Docs team to trigger an update.\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1046346041",
    "pr_number": 13428,
    "pr_file": "docs/dev/how_to/releasing_chef_infra.md",
    "created_at": "2022-12-12T20:13:33+00:00",
    "commented_code": "#### Resource Documentation Automation\n\n1. Run `rake docs_site:resources` to generate content to a `docs_site` directory\n   1. WARNING: Any resource that inherits it's basic structure from a parent resource is likely to comingle settings from both when you run that command. For example, there are 17-20 resources that consume the basic package.rb resource file. As a consequence, ALL of the children will most likely have pulled in properties and actions that do not apply to them. You have to be careful here.",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1046346041",
        "repo_full_name": "chef/chef",
        "pr_number": 13428,
        "pr_file": "docs/dev/how_to/releasing_chef_infra.md",
        "discussion_id": "1046346041",
        "commented_code": "@@ -29,10 +31,18 @@ If there are any new or updated resources, the docs site will need to be updated\n #### Resource Documentation Automation\n \n 1. Run `rake docs_site:resources` to generate content to a `docs_site` directory\n+   1. WARNING: Any resource that inherits it's basic structure from a parent resource is likely to comingle settings from both when you run that command. For example, there are 17-20 resources that consume the basic package.rb resource file. As a consequence, ALL of the children will most likely have pulled in properties and actions that do not apply to them. You have to be careful here.",
        "comment_created_at": "2022-12-12T20:13:33+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "should be `commingle`",
        "pr_file_module": null
      },
      {
        "comment_id": "1046449480",
        "repo_full_name": "chef/chef",
        "pr_number": 13428,
        "pr_file": "docs/dev/how_to/releasing_chef_infra.md",
        "discussion_id": "1046346041",
        "commented_code": "@@ -29,10 +31,18 @@ If there are any new or updated resources, the docs site will need to be updated\n #### Resource Documentation Automation\n \n 1. Run `rake docs_site:resources` to generate content to a `docs_site` directory\n+   1. WARNING: Any resource that inherits it's basic structure from a parent resource is likely to comingle settings from both when you run that command. For example, there are 17-20 resources that consume the basic package.rb resource file. As a consequence, ALL of the children will most likely have pulled in properties and actions that do not apply to them. You have to be careful here.",
        "comment_created_at": "2022-12-12T22:19:50+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "corrected",
        "pr_file_module": null
      }
    ]
  }
]
