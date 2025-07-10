---
title: Follow established naming patterns
description: 'Names should be descriptive and consistent with existing patterns in
  the codebase. This applies to methods, variables, and DSL elements:


  1. Follow existing naming patterns for similar concepts:'
repository: Homebrew/brew
label: Naming Conventions
language: Ruby
comments_count: 6
repository_stars: 44168
---

Names should be descriptive and consistent with existing patterns in the codebase. This applies to methods, variables, and DSL elements:

1. Follow existing naming patterns for similar concepts:
   ```ruby
   # Good: Follows pattern of post_install_defined?, resource_defined?
   def livecheck_defined?
     method(:livecheck).owner != Formula
   end

   # Bad: Inconsistent with existing pattern
   def has_livecheck?
     method(:livecheck).owner != Formula
   end
   ```

2. Use descriptive variable names that clearly indicate content:
   ```ruby
   # Good: Clear what the variable contains
   basename = File.basename(path, ".*")
   match_github = url.match(%r{github\.com/(?<user>\S+)/(?<repo>\S+)})

   # Bad: Unclear or ambiguous names
   m = url.match(%r{github\.com/(?<user>\S+)/(?<repo>\S+)})
   filename = File.basename(path, ".*") # When actually storing basename
   ```

3. For boolean methods, use question mark suffix and descriptive predicate:
   ```ruby
   # Good: Clear boolean nature and what's being checked
   def binary_linked_to_library?(binary, library)

   # Bad: Unclear if returns boolean
   def check_binary_linkage(binary, library)
   ```