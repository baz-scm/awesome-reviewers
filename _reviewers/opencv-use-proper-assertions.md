---
title: Use proper assertions
description: 'Write tests with proper assertions to ensure reliability and maintainability.
  Follow these guidelines:


  1. **Check for empty data** before proceeding with tests to prevent invalid test
  conditions:'
repository: opencv/opencv
label: Testing
language: C++
comments_count: 7
repository_stars: 82865
---

Write tests with proper assertions to ensure reliability and maintainability. Follow these guidelines:

1. **Check for empty data** before proceeding with tests to prevent invalid test conditions:
```cpp
string path = cvtest::findDataFile("test_image.png");
Mat img = imread(path);
ASSERT_FALSE(img.empty()) << "Cannot open test image: " << path;
```

2. **Use ASSERT_* for critical conditions** that should halt test execution when failed:
```cpp
// Use ASSERT_TRUE for file operations and resource initialization
ASSERT_TRUE(fs.isOpened()) << "Failed to open file";

// Use EXPECT_* for test validations that shouldn't interrupt the test
EXPECT_EQ(dst.cols, 270);
```

3. **Maintain correct parameter order** in equality assertions with (expected, actual) to generate meaningful error messages:
```cpp
// Correct: ASSERT_EQ(expected_reference, actual_result)
ASSERT_EQ(4, img.channels());
EXPECT_EQ(6, lines[0][0]);
```

4. **Use specialized assertions** for common comparisons instead of custom loops:
```cpp
// Use instead of manual matrix comparison loops
EXPECT_MAT_NEAR(src_mat, dst_mat, 0);
// or
EXPECT_PRED_FORMAT2(cvtest::MatComparator(0, 0), src_mat, dst_mat);
```

Well-written assertions make tests more reliable, easier to debug, and help identify the exact cause of failures.
