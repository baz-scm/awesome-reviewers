---
title: Robust error handling
description: 'Implement comprehensive error handling to prevent crashes and aid debugging.
  This includes:


  1. **Use try/catch blocks for risky operations** - Especially when parsing JSON
  or using browser APIs that might throw exceptions:'
repository: RooCodeInc/Roo-Code
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 17288
---

Implement comprehensive error handling to prevent crashes and aid debugging. This includes:

1. **Use try/catch blocks for risky operations** - Especially when parsing JSON or using browser APIs that might throw exceptions:

```typescript
// Before
const data = JSON.parse(message.text || "{}");

// After
let data;
try {
  data = JSON.parse(message.text || "{}");
} catch (error) {
  console.error("Failed to parse message data:", error);
  data = {}; // Provide fallback value
}
```

2. **Enhance React error boundaries** - Capture and log detailed error context:

```typescript
class ErrorBoundary extends Component<ErrorProps, ErrorState> {
  constructor(props: ErrorProps) {
    super(props);
    this.state = {};
  }

  static getDerivedStateFromError(error: unknown) {
    return {
      error: error instanceof Error ? (error.stack ?? error.message) : `${error}`,
    };
  }
  
  // Add this method to capture additional context
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Log to monitoring system with context
    logErrorToService({
      error,
      componentStack: info.componentStack,
      timestamp: new Date().toISOString(),
      additionalContext: this.props.contextData
    });
  }
  
  render() {
    if (this.state.error) {
      return <ErrorDisplay error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

3. **Include helpful context** - When handling errors, capture relevant details like timestamps, component stacks, or state information to make debugging easier.

This approach ensures your application degrades gracefully when errors occur while providing the information needed to fix underlying issues.