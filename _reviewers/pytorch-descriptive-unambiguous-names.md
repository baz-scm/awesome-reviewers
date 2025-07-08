---
title: Descriptive unambiguous names
description: Always use descriptive variable names that clearly indicate their purpose
  without requiring readers to check call sites or implementation details. Avoid single-letter
  variables like `t` or vague abbreviations, especially in public interfaces and open-source
  code. Additionally, ensure clear distinction between similarly named variables,
  particularly when...
repository: pytorch/pytorch
label: Naming Conventions
language: C++
comments_count: 2
repository_stars: 91345
---

Always use descriptive variable names that clearly indicate their purpose without requiring readers to check call sites or implementation details. Avoid single-letter variables like `t` or vague abbreviations, especially in public interfaces and open-source code. Additionally, ensure clear distinction between similarly named variables, particularly when distinguishing between member variables and local variables with related purposes.

Bad example:
```cpp
void LayoutManager::assert_no_overlapping_storages(const Node& node, size_t t) {
  // t is unclear - does it mean time, temporary, or something else?
}

class AliasAnalyzer {
private:
  std::set<Value*> aliases_;
  
  void someMethod() {
    std::set<Value*> aliases; // Confusing similarity to member variable
    // Code using both aliases_ and aliases
  }
};
```

Good example:
```cpp
void LayoutManager::assert_no_overlapping_storages(const Node& node, size_t nodeIdx) {
  // Clear that this refers to a node index
}

class AliasAnalyzer {
private:
  std::set<Value*> finalized_aliases_; // More descriptive name
  
  void someMethod() {
    std::set<Value*> current_aliases; // Clearly distinct from member variable
    // Code using both finalized_aliases_ and current_aliases
  }
};
```