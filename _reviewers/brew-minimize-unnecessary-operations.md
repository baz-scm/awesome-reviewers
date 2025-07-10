---
title: Minimize unnecessary operations
description: 'Optimize performance by eliminating redundant operations and arranging
  code to avoid unnecessary computations, especially in frequently executed paths.
  Follow these principles:'
repository: Homebrew/brew
label: Performance Optimization
language: Ruby
comments_count: 6
repository_stars: 44168
---

Optimize performance by eliminating redundant operations and arranging code to avoid unnecessary computations, especially in frequently executed paths. Follow these principles:

1. **Move invariant operations outside of loops** - When an operation's result doesn't change between iterations, perform it only once:

```ruby
# Instead of this:
primary_container.dependencies.each do |dep|
  Homebrew::Install.perform_preinstall_checks_once
  # other operations...
end

# Do this:
Homebrew::Install.perform_preinstall_checks_once
primary_container.dependencies.each do |dep|
  # other operations...
end
```

2. **Read and process files once** - Cache file contents rather than repeatedly reading the same file:

```ruby
# Instead of repeatedly reading files in a loop:
formulae_and_casks_to_check.each do |formula_or_cask|
  autobump_file = formula_or_cask.tap.path/".github/autobump.txt"
  next false unless File.exist?(autobump_file)
  if File.read(autobump_file).include?(formula_or_cask.name)
    # ...
  end
end

# Read files once and cache the results:
autobump_files = {}
formulae_and_casks_to_check.each do |formula_or_cask|
  tap = formula_or_cask.tap
  next if tap.nil?

  autobump_files[tap] ||= begin
    autobump_path = tap.path/".github/autobump.txt"
    autobump_path.exist? ? File.read(autobump_path).lines.map(&:strip) : []
  end
  # Use cached content
end
```

3. **Cache expensive function results** - For slow operations, calculate once and reuse:

```ruby
# Cache expensive operation results
deploy_new_x86_64_runner = @all_supported || deploy_new_x86_64_runner?
```

4. **Order conditional checks efficiently** - Check simple, fast conditions before expensive operations:

```ruby
Formula.all.any? do |formula|
  # First check the simple condition
  next false if formula.class.pour_bottle_only_if != :clt_installed
  
  # Only then perform expensive dependency analysis
  non_test_dependencies = Dependency.expand(formula, cache_key: "determine-test-runners") do |_, dependency|
    Dependency.prune if dependency.test?
  end
  # ...
end
```

5. **Combine multiple iterations** - When performing multiple operations on the same collection, try to handle everything in a single pass rather than iterating multiple times.

These optimizations are particularly important in performance-critical paths that execute frequently or process large amounts of data.