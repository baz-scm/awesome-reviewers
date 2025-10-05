---
title: separate formatting from logging
description: Design logging utility functions to return formatted strings rather than
  directly performing logging operations. This separation of concerns improves modularity,
  testability, and allows callers to control when and how logging occurs.
repository: facebook/yoga
label: Logging
language: Other
comments_count: 2
repository_stars: 18255
---

Design logging utility functions to return formatted strings rather than directly performing logging operations. This separation of concerns improves modularity, testability, and allows callers to control when and how logging occurs.

Instead of having utility functions that directly log:
```c
void YGLogAlign(YGLogLevel logLevel, const char * param, YGAlign value){
  char * text = "undefined";
  switch(value){
    case YGAlignAuto: text = "auto"; break;
    case YGAlignCenter: text = "center"; break;
    // ...
  }
  if(param == NULL) {
    YGLog(logLevel, text);  // Direct logging
  }
}
```

Prefer functions that return formatted strings:
```c
const char* YGAlignToString(YGAlign value) {
  switch(value){
    case YGAlignAuto: return "auto";
    case YGAlignCenter: return "center";
    // ...
    default: return "undefined";
  }
}
// Caller controls logging: YGLog(logLevel, YGAlignToString(value));
```

This approach reduces coupling, makes the formatting logic reusable in non-logging contexts, and simplifies testing of string conversion logic independently from logging behavior.