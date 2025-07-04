---
title: Prevent algorithmic pitfalls
description: 'Avoid common algorithmic errors that lead to incorrect results or inefficient
  code by following these practices:


  1. **Never modify a collection while iterating over it**'
repository: boto/boto3
label: Algorithms
language: Python
comments_count: 7
repository_stars: 9417
---

Avoid common algorithmic errors that lead to incorrect results or inefficient code by following these practices:

1. **Never modify a collection while iterating over it**
   Store results in a separate variable rather than overwriting the collection you're iterating through:

   ```python
   # Incorrect:
   response = self.meta.client.list_access_keys(UserName=self.user_name)
   for access_key in response['AccessKeyMetadata']:
       if access_key['AccessKeyId'] == self.id:
           response = access_key  # Overwriting the response being iterated!
   
   # Correct:
   response = self.meta.client.list_access_keys(UserName=self.user_name)
   result = None
   for access_key in response['AccessKeyMetadata']:
       if access_key['AccessKeyId'] == self.id:
           result = access_key
   ```

2. **Use appropriate data types for calculations**
   Cast to float when division requires decimal precision:

   ```python
   # Incorrect (integer division truncates to 0):
   percentage = (self._seen_so_far / self._size) * 100  # 123/1024*100 = 0
   
   # Correct:
   percentage = (float(self._seen_so_far) / self._size) * 100  # 12.01171875
   ```

3. **Choose specialized tools over general approaches**
   Use dedicated parsers rather than regex for complex parsing tasks:

   ```python
   # Avoid brittle regex approaches with edge cases:
   TARGET_COMPONENT_RE = re.compile(r'[^.\[\]]+(?![^\[]*\])')
   
   # Better: Use existing parsers for complex expressions
   result = jmespath.compile('foo[].bar[].baz.*.qux')
   current = result.parsed
   while current['children']:
     current = current['children'][0]
   field_name = current['value']  # 'foo'
   ```

4. **Use efficient built-in functions**
   Prefer Python's built-in functions like `any()` over creating temporary lists:

   ```python
   # Inefficient (creates a temporary list):
   needs_data = [i for i in reference.resource.identifiers if i.source == 'data']
   if needs_data:
       # do something
   
   # Efficient:
   needs_data = any(i.source == 'data' for i in reference.resource.identifiers)
   ```

5. **Implement robust comparisons**
   Compare actual types rather than names, and handle edge cases in comparison algorithms:

   ```python
   # Fragile comparison that could have false positives:
   if other.__class__.__name__ != self.__class__.__name__:
       
   # More robust comparison:
   if other.__class__ != self.__class__:
   ```

When implementing comparison algorithms (like version checking), parameterize tests to cover edge cases such as non-standard formats.