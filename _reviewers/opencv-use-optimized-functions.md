---
title: Use optimized functions
description: When implementing algorithms, prefer using OpenCV's built-in optimized
  functions over writing custom implementations. OpenCV's library functions are typically
  vectorized, extensively tested, and optimized for performance across different platforms
  and hardware architectures.
repository: opencv/opencv
label: Algorithms
language: C++
comments_count: 7
repository_stars: 82865
---

When implementing algorithms, prefer using OpenCV's built-in optimized functions over writing custom implementations. OpenCV's library functions are typically vectorized, extensively tested, and optimized for performance across different platforms and hardware architectures.

Key examples:
1. Use `inRange()` instead of custom saturation checks (Discussion 7)
2. Use `cv::sum()` for channel operations instead of manually splitting and summing (Discussion 9)
3. Consider converting frequently used operations to vectorized functions that can leverage SIMD instructions (Discussion 10, 17)
4. Use mathematical functions with scalar parameters when available, such as `divide(src, 2, dst)` instead of creating intermediate matrices (Discussion 20)
5. Use OpenCV's metrics functions like `cv::PSNR()` instead of custom implementations (Discussion 42)
6. Prefer `cv::RNG` over standard library random generators for deterministic behavior and testability (Discussion 47)

Example - Instead of this:
```cpp
Mat saturate(Mat& src, const double& low, const double& up)
{
    Mat dst = Mat::ones(src.size(), CV_8UC1);
    MatIterator_<Vec3d> it_src = src.begin<Vec3d>(), end_src = src.end<Vec3d>();
    MatIterator_<uchar> it_dst = dst.begin<uchar>();
    for (; it_src != end_src; ++it_src, ++it_dst)
    {
        for (int i = 0; i < 3; ++i)
        {
            if ((*it_src)[i] > up || (*it_src)[i] < low)
            {
                *it_dst = 0;
                break;
            }
        }
    }
    return dst;
}
```

Use this:
```cpp
Mat saturate(Mat& src, const double& low, const double& up)
{
    Mat dst;
    inRange(src, Scalar(low, low, low), Scalar(up, up, up), dst);
    return dst;
}
```
