---
title: Use data providers effectively
description: Organize your test suite by using data providers to consolidate similar
  test cases rather than creating multiple test methods with duplicated logic. This
  improves maintainability, increases test coverage, and makes adding new test scenarios
  easier.
repository: getsentry/sentry-php
label: Testing
language: PHP
comments_count: 7
repository_stars: 1873
---

Organize your test suite by using data providers to consolidate similar test cases rather than creating multiple test methods with duplicated logic. This improves maintainability, increases test coverage, and makes adding new test scenarios easier.

When you have multiple test cases that follow the same testing pattern but with different input/output values, refactor them using a data provider:

```php
/**
 * @dataProvider messageDataProvider
 */
public function testMessage(string $message, array $params, ?string $formatted, array $expected): void
{
    $event = new Event();
    $event->setMessage($message, $params, $formatted);
    
    $data = $event->toArray();
    
    $this->assertArrayHasKey('message', $data);
    $this->assertSame($expected, $data['message']);
}

public function messageDataProvider(): \Generator
{
    // Test case 1: Basic message
    yield [
        'foo',
        [],
        null,
        ['message' => 'foo'],
    ];
    
    // Test case 2: Message with parameters and formatted value
    yield [
        'foo @bar',
        ['@bar' => 'bar'],
        'foo bar',
        [
            'message' => 'foo @bar',
            'params' => ['@bar' => 'bar'],
            'formatted' => 'foo bar',
        ],
    ];
}
```

Data providers also help document the relationship between inputs and expected outputs, making your tests serve as better documentation. Remember to give your data provider methods descriptive names and consider adding comments for complex test cases.