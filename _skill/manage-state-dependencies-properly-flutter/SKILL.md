---
name: manage-state-dependencies-properly-flutter
description: "Handle Flutter state updates and dependencies carefully to avoid improper rebuilds or setState errors during widget builds."
---

# Manage State Dependencies Properly (Flutter)

Flutter widgets must manage state in tandem with the framework’s build and render cycle. Two key practices ensure that state changes don’t occur at the wrong time and that widgets rebuild when expected:

1. **Establish explicit dependencies.** If a widget uses some external state (like an `InheritedWidget` or ambient state from `BuildContext`), make sure to register it as a dependency. Avoid one-off lookups (e.g. calling `Overlay.of(context)` directly) that don’t notify the widget when that external state changes[22]. Instead, prefer patterns like calling `context.dependOnInheritedWidgetOfExactType` or using provided widgets that automatically trigger rebuilds. This way, when the external source updates, your widget knows to rebuild.
2. **Avoid state changes during build.** Never call `setState` (or trigger any stateful change) while Flutter is in the middle of a build/layout pass. For example, doing state updates in `initState` or `didChangeDependencies` without deferring can cause “setState during build” runtime errors. If you must schedule an update in response to something during build, defer it using a post-frame callback[23]. In Flutter, you can check the scheduler phase and use `SchedulerBinding.instance.addPostFrameCallback` to run code after the current frame completes[24].

**Example:** A Flutter widget needed to call a callback `onCloseRequested` inside `didChangeDependencies`. The solution was to wrap the call in a check of the scheduler phase and use `addPostFrameCallback` if Flutter was in the middle of building[23]. This prevented the setState-from-build error and ensured the callback runs just after the build. By following these patterns, we prevent obscure bugs and ensure Flutter apps remain stable and responsive, similar to React’s rules about not mutating state during render[25].
