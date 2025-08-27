---
title: Simplify complex code
description: 'Break down complex code structures into simpler, more readable forms
  to improve maintainability and reduce cognitive load. This involves several key
  practices:'
repository: bazelbuild/bazel
label: Code Style
language: Java
comments_count: 15
repository_stars: 24489
---

Break down complex code structures into simpler, more readable forms to improve maintainability and reduce cognitive load. This involves several key practices:

**Extract duplicate code into helper methods:**
```java
// Instead of duplicating logic:
if (write) {
  new CommandBuilder()
      .setWorkingDir(env.getWorkspace())
      .addArg(modTidyValue.buildozer().getPathString())
      .addArg("-f")
      .addArg("-")
} else {
  new CommandBuilder()
      .setWorkingDir(env.getWorkspace())
      .addArg(modTidyValue.buildozer().getPathString())
      .addArg("-f")
      .addArg("-")
}

// Extract common construction:
private CommandBuilder createBaseBuilder() {
  return new CommandBuilder()
      .setWorkingDir(env.getWorkspace())
      .addArg(modTidyValue.buildozer().getPathString())
      .addArg("-f")
      .addArg("-");
}
```

**Use early returns to reduce nesting:**
```java
// Instead of nested conditions:
if (artifact instanceof DerivedArtifact) {
  return true;
} else if (artifact instanceof BasicActionInput || artifact instanceof VirtualActionInput) {
  return isOutputPath(artifact, outputRoot);
} else {
  return false;
}

// Use early returns:
if (artifact instanceof DerivedArtifact) {
  return true;
}
if (artifact instanceof BasicActionInput || artifact instanceof VirtualActionInput) {
  return isOutputPath(artifact, outputRoot);
}
return false;
```

**Prefer switch expressions over if-else chains:**
```java
// Instead of if-else:
Mode mode;
if (testCase.getStatus() == Status.PASSED) {
  mode = Mode.INFO;
} else {
  mode = Mode.ERROR;
}

// Use switch expression:
Mode mode = switch (testCase.getStatus()) {
  case PASSED -> Mode.INFO;
  default -> Mode.ERROR;
};
```

**Make implicit operations explicit for clarity:**
```java
// Instead of implicit this:
equals(platformValue)

// Be explicit:
this.equals(platformValue)
```

**Break large methods into focused smaller methods** when they handle multiple distinct responsibilities, and **extract string literals into constants** when they appear in multiple places or carry semantic meaning.