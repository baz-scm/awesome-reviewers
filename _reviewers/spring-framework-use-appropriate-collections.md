---
title: Use appropriate collections
description: Choose the right collection implementation for each algorithmic task
  to optimize both performance and readability. Use Sets for operations requiring
  uniqueness, TreeMap for maintaining sorted keys, and leverage built-in collection
  methods rather than implementing operations manually.
repository: spring-projects/spring-framework
label: Algorithms
language: Java
comments_count: 6
repository_stars: 58382
---

Choose the right collection implementation for each algorithmic task to optimize both performance and readability. Use Sets for operations requiring uniqueness, TreeMap for maintaining sorted keys, and leverage built-in collection methods rather than implementing operations manually.

Key practices:
- Use HashSet instead of List+contains checks when eliminating duplicates
- Prefer Map.computeIfAbsent over get-check-put patterns
- Use specialized collection methods like Collections.addAll or direct List.sort instead of chained operations
- Select TreeMap when sorted key access is required

Example of improvement:
```java
// Less efficient approach
List<String> items = new ArrayList<>();
items.addAll(Arrays.asList(array1));
for (String item : array2) {
    if (!items.contains(item)) {  // O(n) operation for each check
        items.add(item);
    }
}

// More efficient approach
Set<String> uniqueItems = new LinkedHashSet<>();
Collections.addAll(uniqueItems, array1);
Collections.addAll(uniqueItems, array2);  // Duplicates automatically handled
```

Another optimization example:
```java
// Less efficient sorting
Collections.sort(advisors, new OrderComparator());

// More efficient sorting
advisors.sort(OrderComparator.INSTANCE);  // Or OrderComparator.sort(advisors)
```

This approach improves algorithmic efficiency by selecting data structures with appropriate time complexity for the required operations.