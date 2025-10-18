---
title: Multiple remote configuration
description: When documenting or implementing features that involve multiple remote
  repositories, provide clear guidance on different remote configuration strategies
  and their appropriate use cases. This includes explaining the distinction between
  remotes you have write access to (typically `origin`) versus read-only upstream
  remotes, and when to track or sync different...
repository: jj-vcs/jj
label: Networking
language: Markdown
comments_count: 2
repository_stars: 21171
---

When documenting or implementing features that involve multiple remote repositories, provide clear guidance on different remote configuration strategies and their appropriate use cases. This includes explaining the distinction between remotes you have write access to (typically `origin`) versus read-only upstream remotes, and when to track or sync different remote branches.

For example, when documenting repository setup options, include all available initialization methods:

```shell
# Option 1: Start JJ in an existing Git repo with remotes
$ jj git init --colocate

# Option 2: Clone directly from remote
$ jj git clone <remote-url>

# Option 3: Initialize new repo and add remotes
$ jj git init
$ jj git remote add origin <your-fork>
$ jj git remote add upstream <canonical-repo>
```

Address common workflow questions explicitly, such as whether to keep fork repositories synchronized with upstream, and explain the trade-offs of different tracking strategies. This helps developers understand the networking implications of their remote configuration choices and select the approach that best fits their collaboration model.