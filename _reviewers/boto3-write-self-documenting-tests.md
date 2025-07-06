---
title: Write self-documenting tests
description: 'Tests should clearly communicate their purpose and expectations without
  requiring readers to analyze implementation details or scroll through files. Each
  test should:'
repository: boto/boto3
label: Testing
language: Python
comments_count: 8
repository_stars: 9417
---

Tests should clearly communicate their purpose and expectations without requiring readers to analyze implementation details or scroll through files. Each test should:

1. Use descriptive names that indicate the specific scenario being tested
2. Include explicit assertions that verify all expected behaviors
3. Maintain context within the test method itself
4. Organize shared setup logically

Example of a poorly documented test:
```python
def test_upload(self):
    transfer = self.create_s3_transfer()
    filename = self.files.create_file_with_size('foo.txt', 1024 * 1024)
    transfer.upload_file(filename, self.bucket_name, 'foo.txt')
    self.assertTrue(self.object_exists('foo.txt'))
```

Improved version:
```python
def test_upload_below_threshold_uses_single_part_upload(self):
    # Configure transfer to use single-part for small files
    config = TransferConfig(multipart_threshold=5 * 1024 * 1024)
    transfer = self.create_s3_transfer(config)
    
    # Create a 1MB file (below threshold)
    filename = self.files.create_file_with_size('foo.txt', 1024 * 1024)
    
    # Upload should use single-part upload
    transfer.upload_file(filename, self.bucket_name, 'foo.txt')
    
    # Verify file exists and was uploaded as single part
    self.assertTrue(self.object_exists('foo.txt'))
    self.assertEqual(self.get_upload_type('foo.txt'), 'SINGLE_PART')
```

The improved version:
- Has a specific, descriptive name
- Documents test setup and expectations
- Includes all relevant assertions
- Maintains context within the test method
- Makes the test's purpose clear without requiring external knowledge