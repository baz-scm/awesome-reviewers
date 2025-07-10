---
title: Split for better readability
description: 'Break long lines and complex structures across multiple lines to improve
  code readability. Follow these guidelines:


  1. Keep line length around 80 characters (soft limit)'
repository: getsentry/sentry-php
label: Code Style
language: PHP
comments_count: 11
repository_stars: 1873
---

Break long lines and complex structures across multiple lines to improve code readability. Follow these guidelines:

1. Keep line length around 80 characters (soft limit)
2. Split docblocks and comments across multiple lines
3. Break down complex arrays and method chains
4. Format related elements consistently

Example of proper formatting:

```php
/**
 * This is a long docblock description that would exceed
 * the 80 character limit if written on a single line.
 *
 * @param string $param Description of the parameter
 */
public function example($param)
{
    $data = [
        'first_key' => 'value1',
        'second_key' => 'value2',
        'third_key' => 'value3',
    ];

    $object->methodOne()
           ->methodTwo()
           ->methodThree();
}
```

Instead of:

```php
/** This is a long docblock description that would exceed the 80 character limit if written on a single line. */
public function example($param)
{
    $data = ['first_key' => 'value1', 'second_key' => 'value2', 'third_key' => 'value3'];
    
    $object->methodOne()->methodTwo()->methodThree();
}
```