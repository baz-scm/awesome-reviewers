---
title: Standardize logger configuration patterns
description: Maintain consistent logger configuration and usage patterns across the
  application while leveraging built-in customization options. This promotes maintainable
  logging practices and ensures uniform log output.
repository: nestjs/nest
label: Logging
language: TypeScript
comments_count: 4
repository_stars: 71766
---

Maintain consistent logger configuration and usage patterns across the application while leveraging built-in customization options. This promotes maintainable logging practices and ensures uniform log output.

Key guidelines:
1. Configure logging options at the application level rather than scattered throughout the code
2. Use protected methods for custom formatting when needed
3. Keep logger instances at the class level rather than creating new instances repeatedly
4. Utilize the built-in formatting options before creating custom solutions

Example of proper logger configuration and customization:

```typescript
// Global configuration
const app = await NestFactory.create(AppModule, {
  logger: {
    json: true,  // Configure JSON logging globally
  }
});

// Custom formatting when needed
class CustomLogger extends ConsoleLogger {
  protected formatMessage(
    pid: number,
    logLevel: string,
    context: string,
    timestampDiff: number,
    output: string,
  ): string {
    // Custom format implementation
    return `[${logLevel}] ${context}: ${output}`;
  }
}

// Class-level logger instance
@Injectable()
class MyService {
  private readonly logger = new Logger(MyService.name);
  
  someMethod() {
    this.logger.log('Operation completed');
  }
}
```