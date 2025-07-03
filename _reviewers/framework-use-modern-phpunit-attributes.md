---
title: Use modern PHPUnit attributes
description: 'Prefer modern PHPUnit attributes over PHPDoc annotations for improved
  type safety, IDE support, and code readability in tests. Replace legacy annotation-style
  test decorators with their attribute counterparts:'
repository: laravel/framework
label: Testing
language: PHP
comments_count: 7
repository_stars: 33763
---

Prefer modern PHPUnit attributes over PHPDoc annotations for improved type safety, IDE support, and code readability in tests. Replace legacy annotation-style test decorators with their attribute counterparts:

- Use `#[DataProvider]` for test data organization:
```php
#[DataProvider('provideStrSanitizeTestStrings')]
public function testSanitize(?string $subject, ?string $expected, ?HtmlSanitizerConfig $config)
{
    $this->assertSame($expected, Str::sanitize($subject, $config));
}

public static function provideStrSanitizeTestStrings()
{
    return [
        'non-empty string is returned as is' => ['Hello', 'Hello', null],
        'XSS attack is sanitized' => ['<script>alert("XSS")</script>', '', null],
        // more test cases...
    ];
}
```

- Use `#[RequiresPhp('8.4.0')]` or similar attributes instead of manual version checks:
```php
// Instead of:
if (PHP_VERSION_ID < 80400) {
    $this->markTestSkipped('Property Hooks are not available to test in PHP...');
}

// Use:
#[RequiresPhp('8.4.0')]
class DatabaseEloquentWithPropertyHooksTest extends TestCase
{
    // Test methods...
}
```

- For simpler test data cases, consider `#[TestWith]`:
```php
#[TestWith(['Hello', 'Hello', null])]
#[TestWith([123, '123', null])]
#[TestWith([null, null, null])]
public function testSanitize(?string $subject, ?string $expected, ?HtmlSanitizerConfig $config)
{
    $this->assertSame($expected, Str::sanitize($subject, $config));
}
```

This approach improves code maintainability, provides better type hinting to IDEs, and follows modern PHP testing practices.
