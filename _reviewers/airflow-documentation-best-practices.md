---
title: Documentation best practices
description: 'Documentation should follow established best practices to ensure clarity,
  consistency, and usefulness:


  1. **Use proper link types**: Use relative links for internal resources and absolute
  HTTP links only for external resources.'
repository: apache/airflow
label: Documentation
language: Other
comments_count: 5
repository_stars: 40858
---

Documentation should follow established best practices to ensure clarity, consistency, and usefulness:

1. **Use proper link types**: Use relative links for internal resources and absolute HTTP links only for external resources.
   ```python
   # Good
   - `Task SDK Overview <../concepts/taskflow.html>`_
   
   # Bad
   - `Task SDK Overview <https://airflow.apache.org/docs/apache-airflow/stable/concepts/taskflow.html>`_
   ```

2. **Write in complete sentences**: Ensure all descriptions, especially in API documentation and migration notes, are complete sentences with proper grammar and punctuation.

3. **Document API components thoroughly**: Include docstrings for all API functions, methods, and classes with detailed information about parameters, return values, and usage examples.
   ```python
   @task
   def process_data(data_path: str, limit: Optional[int] = None) -> Dict[str, Any]:
       """
       Process data from the specified path with optional limit.
       
       :param data_path: Path to the data file to process
       :param limit: Maximum number of records to process, None for unlimited
       :return: Dictionary containing processed results
       """
       # Implementation
   ```

4. **Document all API variants**: Ensure "sub" decorators and related API components (like `@task.skip_if`) are documented alongside their parent components.

5. **Use enhanced documentation directives**: Use specialized directives like `exampleinclude` instead of `literalinclude` to provide "[sources]" links that give users access to complete context and code examples.

Following these practices improves documentation usability, making it easier for developers to understand and correctly implement the documented functionality.