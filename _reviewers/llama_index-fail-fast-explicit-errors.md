---
title: Fail fast, explicit errors
description: 'Surface failures immediately and explicitly instead of hiding them.
  Specifically:


  1. **Never silently swallow errors.** Catching an exception only to log it and return
  an empty/default result (or continue as if nothing happened) hides real problems
  from callers. If an operation fails, raise — don''t swallow it.'
repository: run-llama/llama_index
label: Error Handling
language: Python
comments_count: 17
repository_stars: 52785
---

Surface failures immediately and explicitly instead of hiding them. Specifically:

1. **Never silently swallow errors.** Catching an exception only to log it and return an empty/default result (or continue as if nothing happened) hides real problems from callers. If an operation fails, raise — don't swallow it.
   ```python
   # Bad: silent failure
   try:
       results = self._index.query(...)
   except Exception as e:
       logger.error(f"Error querying: {e}")
       return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

   # Good: let it propagate (or raise a clearer error)
   results = self._index.query(...)
   ```

2. **Validate inputs as early as possible (fail fast).** Prefer validating required arguments/invariants in `__init__` or at the start of a call rather than deep inside downstream methods, so misconfiguration is caught immediately with a clear message (e.g., missing credentials, an `enforce` key not present in `params`, an unsupported `chunker_type`, a string exceeding an API's length limit).
   ```python
   def __init__(self, username=None, password=None, token=None):
       self.username = username or os.environ.get("SF_USERNAME")
       self.password = password or os.environ.get("SF_PASSWORD")
       self.security_token = token or os.environ.get("SF_TOKEN")
       if not all([self.username, self.password, self.security_token]):
           raise ValueError(
               "Salesforce credentials must be provided as constructor "
               "arguments or via SF_USERNAME, SF_PASSWORD, SF_TOKEN env vars."
           )
   ```

3. **Use the most specific, correct exception type and preserve the original error.** Don't collapse everything into a bare `Exception`; use `ValueError`/`TypeError`/library-specific exceptions, and when wrapping a lower-level error, chain it with `raise NewError(...) from e` so the root cause isn't lost. Let upstream, more specific exceptions (e.g., a client's `NotFoundError`) propagate unchanged unless you add real value by wrapping them.

4. **Only add error-handling scaffolding where it's actually needed.** Don't wrap imports or calls in `try/except` when the dependency is a hard requirement (it can't actually fail in a way you need to handle), and don't duplicate a `try/except` for a failure mode that's already handled downstream — redundant or guard-everything error handling obscures real bugs and adds maintenance burden without benefit.

Applying these consistently means errors surface close to their root cause, with accurate types and messages, making bugs easier to diagnose and preventing silent data loss or incorrect behavior.</description>
