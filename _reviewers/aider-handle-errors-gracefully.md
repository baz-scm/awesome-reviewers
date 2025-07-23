---
title: Handle errors gracefully
description: 'Always implement appropriate error handling to prevent crashes while
  providing clear feedback to users. Consider these principles:


  1. **Decide on error propagation strategy**: Determine whether errors should be
  handled locally or propagated to a higher-level handler based on severity and recoverability.'
repository: Aider-AI/aider
label: Error Handling
language: Python
comments_count: 4
repository_stars: 35856
---

Always implement appropriate error handling to prevent crashes while providing clear feedback to users. Consider these principles:

1. **Decide on error propagation strategy**: Determine whether errors should be handled locally or propagated to a higher-level handler based on severity and recoverability.

2. **Catch specific exceptions**: Target exact exception types rather than using broad catches.

3. **Use consistent error reporting**: Utilize standardized error reporting mechanisms instead of print statements.

4. **Consider platform-specific issues**: Anticipate and handle platform-dependent error scenarios.

Example of proper error handling with clear propagation strategy:

```python
def register_models(model_def_fnames):
    for model_def_fname in model_def_fnames:
        if not os.path.exists(model_def_fname):
            continue
        try:
            with open(model_def_fname, "r") as model_def_file:
                model_def = json.load(model_def_file)
        except json.JSONDecodeError as e:
            # Propagate critical configuration errors to main for centralized handling
            raise ConfigurationError(f"Invalid model definition in {model_def_fname}: {e}")
        except IOError as e:
            # Log but continue if a file can't be read
            io.tool_error(f"Could not read model definition: {e}")
```

When handling cleanup operations, catch specific exceptions that might occur:

```python
try:
    # Cleanup operation
    shutil.rmtree(self.tempdir)
except (OSError, PermissionError):
    pass  # Ignore cleanup errors (especially on Windows)
```

For functions that might fail, clearly document return behavior and ensure consistent error state handling:

```python
# Return values on error should be documented and consistent
try:
    self.repo.git.commit(cmd)
    return commit_hash, commit_message
except GitError as err:
    self.io.tool_error(f"Unable to commit: {err}")
    # Explicitly return None to make the error path obvious
    return None
```