---
title: Use object methods consistently
description: When working with Document objects, always use their accessor methods
  rather than array-style syntax. Use `$object->getAttribute('property')` and `$object->setAttribute('property',
  $value)` instead of `$object['property']`. This ensures proper encapsulation, maintains
  data integrity through validation, and creates more resilient code that won't break
  if the...
repository: appwrite/appwrite
label: Code Style
language: PHP
comments_count: 3
repository_stars: 51959
---

When working with Document objects, always use their accessor methods rather than array-style syntax. Use `$object->getAttribute('property')` and `$object->setAttribute('property', $value)` instead of `$object['property']`. This ensures proper encapsulation, maintains data integrity through validation, and creates more resilient code that won't break if the underlying implementation changes.

```diff
-// Avoid direct array access on Document objects
-if (isset($session['clientName']) && empty($session['clientName'])) {
-    $session['clientName'] = !empty($session['userAgent']) ? $session['userAgent'] : 'UNKNOWN';
-}

+// Prefer method access for Document objects
+if ($session->getAttribute('clientName', null) === null || empty($session->getAttribute('clientName'))) {
+    $clientName = !empty($session->getAttribute('userAgent')) ? $session->getAttribute('userAgent') : 'UNKNOWN';
+    $session->setAttribute('clientName', $clientName);
+}
```

This pattern ensures your code leverages the Document object's built-in validation and transformation features while providing better readability and maintainability.