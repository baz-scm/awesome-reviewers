---
title: Structure exception handling patterns
description: Implement consistent exception handling using framework-provided mechanisms
  rather than ad-hoc try-catch blocks or manual error propagation. Use appropriate
  exception classes and interceptors to handle errors at the right architectural level.
repository: nestjs/nest
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 71766
---

Implement consistent exception handling using framework-provided mechanisms rather than ad-hoc try-catch blocks or manual error propagation. Use appropriate exception classes and interceptors to handle errors at the right architectural level.

Key guidelines:
1. Use built-in exception classes with proper status codes
2. Leverage exception interceptors for cross-cutting error handling
3. Avoid mixing different error handling approaches

Example - INCORRECT approach:
```typescript
@Controller('cats')
export class CatsController {
  @Post()
  async create(@Body() createCatDto: CreateCatDto) {
    try {
      await this.catsService.create(createCatDto);
    } catch(error) {
      console.error(error);
      return []; // Swallowing error, returning empty result
    }
  }
}
```

CORRECT approach:
```typescript
@Controller('cats')
export class CatsController {
  @Post()
  async create(@Body() createCatDto: CreateCatDto) {
    // Let exception filter handle errors
    return await this.catsService.create(createCatDto);
  }
}

// In a custom exception filter
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // Proper error handling with status codes and logging
    const status = exception instanceof HttpException 
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;
    // Handle error appropriately...
  }
}
```