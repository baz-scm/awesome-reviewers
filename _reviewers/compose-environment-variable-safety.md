---
title: Environment variable safety
description: Always use `os.environ.get()` instead of direct dictionary access when
  reading environment variables to avoid KeyError exceptions. Establish clear precedence
  rules where command line options override environment variables, and log conflicts
  appropriately when incompatible configuration sources are detected.
repository: docker/compose
label: Configurations
language: Python
comments_count: 3
repository_stars: 35858
---

Always use `os.environ.get()` instead of direct dictionary access when reading environment variables to avoid KeyError exceptions. Establish clear precedence rules where command line options override environment variables, and log conflicts appropriately when incompatible configuration sources are detected.

When accessing environment variables, prefer the safe getter method:
```python
# Good
profiles = environment.get('COMPOSE_PROFILE')
ignore_orphans = environment.get_boolean('COMPOSE_IGNORE_ORPHANS')

# Avoid
if 'CLICOLOR' in os.environ and os.environ['CLICOLOR'] == "0"
```

For configuration precedence, implement command line options taking priority over environment variables:
```python
def compatibility_from_options(working_dir, options=None, environment=None):
    # Command line takes precedence over environment
    if options and options.get('--compatibility'):
        return True
    if environment and 'COMPOSE_COMPATIBILITY' in environment:
        return environment.get_boolean('COMPOSE_COMPATIBILITY')
    return False
```

When conflicting configuration is detected, log the conflict clearly:
```python
if ignore_orphans and options['--remove-orphans']:
    log.warn("COMPOSE_IGNORE_ORPHANS is set, --remove-orphans flag is being ignored.")
```

This approach prevents runtime errors from missing environment variables and ensures predictable configuration behavior across different deployment environments.