---
title: Meaningful semantic naming
description: 'Choose names that clearly communicate purpose and follow consistent
  patterns across the codebase:


  1. Use generic function names when the functionality is reusable, with parameters
  for specific values:'
repository: opencv/opencv
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 82865
---

Choose names that clearly communicate purpose and follow consistent patterns across the codebase:

1. Use generic function names when the functionality is reusable, with parameters for specific values:
   ```python
   # Instead of:
   def check_have_ipp_flag(cmake_file):
       # Check specifically for HAVE_IPP flag
   
   # Prefer:
   def check_cmake_flag_enabled(cmake_file, flag_name):
       # Check for any flag
   ```

2. When extending functionality that changes a method's signature, create a new method with a descriptive name rather than modifying the existing one:
   ```python
   # Instead of changing:
   corners, ids, rejected = aruco_detector.detectMarkers(img)
   # To:
   corners, ids, rejected, extra = aruco_detector.detectMarkers(img)
   
   # Create a new method:
   corners, ids, rejected, extra = aruco_detector.detectMarkersMultiDict(img)
   ```

3. Apply naming conventions consistently using established patterns in the codebase rather than creating special cases. If a mechanism exists for handling naming scenarios (like namespace prefixing for functions), use it for similar cases too.
