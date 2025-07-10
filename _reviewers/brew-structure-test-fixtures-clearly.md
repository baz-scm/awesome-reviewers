---
title: Structure test fixtures clearly
description: Test fixtures should clearly separate input parameters from expected
  outputs to enhance readability and maintainability. For table-driven tests, use
  a consistent pattern that explicitly distinguishes between test inputs and expected
  results. This approach makes tests more understandable and easier to maintain over
  time.
repository: Homebrew/brew
label: Testing
language: Ruby
comments_count: 3
repository_stars: 44168
---

Test fixtures should clearly separate input parameters from expected outputs to enhance readability and maintainability. For table-driven tests, use a consistent pattern that explicitly distinguishes between test inputs and expected results. This approach makes tests more understandable and easier to maintain over time.

A well-structured table-driven test might look like:

```ruby
tests = {
  "generic tarball URL": {
    params: {
      url: "http://digit-labs.org/files/tools/synscan/releases/synscan-5.02.tar.gz",
    },
    expected: {
      name: "synscan",
      version: "5.02",
    },
  },
  "with version override": {
    params: {
      url: "http://digit-labs.org/files/tools/synscan/releases/synscan-5.02.tar.gz",
      version: "3.40",
    },
    expected: {
      name: "synscan",
      version: "3.40",
    }
  },
}

tests.each do |description, test|
  it "processes #{description}" do
    result = process_with(test[:params])
    expect(result).to eq(test[:expected])
  end
end
```

This structure makes it immediately clear what inputs are being provided and what outputs are expected, improving test readability and making failures easier to diagnose.