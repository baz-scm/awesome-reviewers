---
title: Configurable log formatting
description: Design logging systems with customizable formatting and output options.
  Separate formatting logic into protected methods that can be overridden by derived
  logger implementations.
repository: nestjs/nest
label: Logging
language: TypeScript
comments_count: 4
repository_stars: 71767
---

Design logging systems with customizable formatting and output options. Separate formatting logic into protected methods that can be overridden by derived logger implementations.

Key practices:
1. Use consistent parameter naming (prefer `json` over `asJSON`)
2. Separate color handling from message composition
3. Make core formatting components overridable
4. Support environment variables for controlling features like colored output

Example of a well-structured logger with configurable formatting:

```typescript
export class CustomizableLogger implements LoggerService {
  // Allow configuring output format
  constructor(protected options: { json?: boolean, timestamp?: boolean }) {}

  // Core logging implementation
  log(message: any, context?: string) {
    const formattedMessage = this.formatMessage(message, context, 'log');
    process.stdout.write(formattedMessage);
  }

  // Protected method for formatting - can be overridden
  protected formatMessage(message: unknown, context: string, logLevel: string): string {
    // For JSON output
    if (this.options.json) {
      return JSON.stringify({
        level: logLevel,
        message,
        context,
        timestamp: new Date().toISOString()
      }) + '\n';
    }

    // Regular formatted output with optional coloring
    const output = this.stringifyMessage(message);
    const contextMsg = context ? `[${context}] ` : '';
    const timestamp = this.options.timestamp ? this.getTimestamp() : '';
    const formattedLevel = this.colorize(logLevel.toUpperCase().padStart(7, ' '));
    
    return `${timestamp} ${formattedLevel} ${contextMsg}${output}\n`;
  }

  // Helper methods that can also be overridden
  protected stringifyMessage(message: unknown): string {
    return typeof message === 'object' ? JSON.stringify(message, null, 2) : String(message);
  }
  
  protected colorize(text: string, color?: (text: string) => string): string {
    // Default implementation or delegate to provided color function
    return color ? color(text) : text;
  }
  
  protected getTimestamp(): string {
    return new Date().toISOString();
  }
}