---
title: structure contextual log messages
description: Log messages should include sufficient contextual information and structured
  formatting to enable effective debugging and filtering. This means including relevant
  metadata, level information, and clear prefixes that help developers understand
  the source and severity of logged events.
repository: llvm/llvm-project
label: Logging
language: Other
comments_count: 2
repository_stars: 33702
---

Log messages should include sufficient contextual information and structured formatting to enable effective debugging and filtering. This means including relevant metadata, level information, and clear prefixes that help developers understand the source and severity of logged events.

For error logging, include references to relevant objects or metadata that can provide additional context:

```cpp
void log(raw_ostream &OS) const override {
  OS << Message;
  if (MD)
    MD->printTree(OS);
}
```

For debug logging, include level information in prefixes to enable easy filtering:

```cpp
if (DebugType) {
  if (Level == 0)
    Level = 1;
  OsPrefix << "[" << DebugType << ":" << Level << "] ";
}
```

This approach allows developers to filter verbose output by level and provides rich context when debugging issues. Well-structured log messages reduce debugging time and improve the overall development experience.