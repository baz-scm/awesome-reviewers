---
title: Document configuration risks comprehensively
description: When documenting configuration options, provide comprehensive information
  including current default values, recommended settings, future behavioral changes,
  and potential security implications. Configuration comments should clearly explain
  not just what the option does, but also warn about risks and provide guidance on
  proper usage.
repository: argoproj/argo-cd
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 20149
---

When documenting configuration options, provide comprehensive information including current default values, recommended settings, future behavioral changes, and potential security implications. Configuration comments should clearly explain not just what the option does, but also warn about risks and provide guidance on proper usage.

For example, instead of a simple description:
```yaml
# Set this flag to false to revert to old behavior
application.sync.externalRevisionConsideredOverride: "true"
```

Provide comprehensive documentation:
```yaml
# The current behavior allows passing a different revision from the one given in the application when syncing. We highly recommend that this be set to `true`. The next major release will set the default to be `false`.
application.sync.externalRevisionConsideredOverride: "false"

# When set to true, the ApplicationSet controller will continue to generate Applications even if the repository is not found.
# NOTE: If a repository exists but is inaccessible due to access rights, SCM providers usually return a "404 Not Found" error
# instead of a "403 Permission Denied" error. Consequently, using this option may lead to the deletion of Argo CD applications
# if the SCM user associated with the token loses access to the repository.
```

This prevents misconfigurations that could lead to security vulnerabilities or unexpected application behavior.