---
title: Structure logs effectively
description: 'When implementing logging in your application, structure your log messages
  and parameters consistently to improve readability, searchability, and integration
  with monitoring tools. Consider these practices:'
repository: django/django
label: Logging
language: Python
comments_count: 5
repository_stars: 84182
---

When implementing logging in your application, structure your log messages and parameters consistently to improve readability, searchability, and integration with monitoring tools. Consider these practices:

1. Use the appropriate logging method for your context:
   - Use `logger.exception()` only when capturing the current exception context
   - Use `logger.error()` with explicit `exc_info=True` when you need to include exception details outside of an exception handler
   
   ```python
   # Correct: Inside an exception handler
   try:
       dangerous_operation()
   except Exception:
       logger.exception("Operation failed")  # Automatically includes traceback
   
   # Correct: Outside an exception handler
   if error_occurred:
       logger.error("Operation failed", exc_info=True)  # Explicitly include traceback
   ```

2. Provide structured context with log messages:
   - Use the `extra` parameter to add structured fields to your logs
   - Be consistent with parameter formats (dict-style vs tuple-style)
   - Include identifying information like connection aliases in database logs
   
   ```python
   # Good: Structured logging with extra parameters
   logger.debug(
       "Query executed: %(sql)s; duration=%(duration).3f; alias=%(alias)s",
       extra={
           "duration": duration,
           "sql": sql,
           "params": params,
           "alias": connection.alias,
       }
   )
   ```

3. Be mindful of performance in log formatters:
   - Cache formatted values to avoid repeated expensive operations
   - Consider conditional formatting based on log levels
   - Handle both dict-style and tuple-style arguments defensively
   
   ```python
   # Performance-aware formatter
   def format(self, record):
       # Cache formatted values to avoid repeated processing
       sql = None
       formatted_sql = None
       
       if args := record.args:
           if isinstance(args, dict) and (sql := args.get("sql")):
               args["sql"] = formatted_sql = format_sql(sql)
           
       # Reuse formatted value if it's the same SQL
       if extra_sql := getattr(record, "sql", None):
           if extra_sql == sql:
               record.sql = formatted_sql
           else:
               record.sql = format_sql(extra_sql)
               
       return super().format(record)
   ```

By following these practices, you'll create logs that are more useful for debugging, monitoring, and analysis while avoiding common performance pitfalls.