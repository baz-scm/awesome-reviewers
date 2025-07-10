---
title: Optimize computational complexity
description: Identify and reduce computational complexity in your code by minimizing
  redundant operations and simplifying algorithms. Focus especially on code that processes
  large datasets or is called frequently.
repository: django/django
label: Algorithms
language: Python
comments_count: 4
repository_stars: 84182
---

Identify and reduce computational complexity in your code by minimizing redundant operations and simplifying algorithms. Focus especially on code that processes large datasets or is called frequently.

**Key practices:**

1. **Reduce redundant operations**, especially in loops and function calls:
   ```python
   # Inefficient - O(2N+1) function calls
   for obj in objs:
       filter_kwargs = get_filter_kwargs_for_object(obj)
       # ...process...
       filter_kwargs = get_filter_kwargs_for_object(obj)  # Called again!
       
   # Optimized - O(N) function calls
   for obj in objs:
       filter_kwargs = get_filter_kwargs_for_object(obj)
       # ...use filter_kwargs throughout...
   ```

2. **Use appropriate data structures** to improve access patterns:
   ```python
   # Creating a lookup map for faster access
   max_orders_map = {
       tuple(key_values): max_order
       for key_values, max_order in zip(keys, values)
   }
   # Now O(1) lookups instead of repeated O(n) searches
   ```

3. **Simplify complex conditionals** without sacrificing functionality:
   ```python
   # Verbose approach
   if isinstance(rel, ForeignKey) or isinstance(rel, OneToOneField):
       # do something
   
   # Simplified equivalent
   if isinstance(rel, (ForeignKey, OneToOneField)):
       # do something
   ```

4. **Choose algorithms with appropriate complexity** for your data size:
   ```python
   # Less efficient for large datasets (potentially O(n²))
   return min(desired_types, key=lambda t: self.accepted_types.index(t[0]))[1]
   
   # More efficient direct comparison (O(n))
   return max(desired_types, key=lambda t: t[0].quality)[1]
   ```

Remember that the most important optimizations target the inner loops and frequently called functions. Document the time and space complexity of critical algorithms to help future developers understand performance considerations.