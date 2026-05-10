---
title: Validate by File Header
description: When parsing untrusted files (e.g., images), do not choose decode/encode
  logic based on filename suffix/substring (e.g., “.pgm/.ppm/.jpg”). Instead, detect
  the actual format using file content (magic bytes/header) and only proceed if it
  matches supported signatures; otherwise fail safely.
repository: Tencent/ncnn
label: Security
language: C++
comments_count: 1
repository_stars: 23205
---

When parsing untrusted files (e.g., images), do not choose decode/encode logic based on filename suffix/substring (e.g., “.pgm/.ppm/.jpg”). Instead, detect the actual format using file content (magic bytes/header) and only proceed if it matches supported signatures; otherwise fail safely.

Why: filename-based routing is trivially bypassed/ambiguous (e.g., “lena.jpg.png”); it can send data down the wrong parser path.

Apply it like this (minimal pattern):

```cpp
// Read first bytes, then decide format by magic/header.
// Do not rely on path.find(...) or last-N extension checks.

enum class ImgFmt { PGM, PPM, JPG, Unknown };

ImgFmt sniff_fmt(FILE* fp) {
    unsigned char b[8] = {0};
    size_t n = fread(b, 1, sizeof(b), fp);
    fseek(fp, 0, SEEK_SET);

    // PGM/PPM: start with ASCII 'P' then '5' (binary PGM) or '6' (binary PPM)
    if (n >= 2 && b[0] == 'P' && (b[1] == '5' || b[1] == '6'))
        return b[1] == '5' ? ImgFmt::PGM : ImgFmt::PPM;

    // Example JPG SOI
    if (n >= 2 && b[0] == 0xFF && b[1] == 0xD8)
        return ImgFmt::JPG;

    return ImgFmt::Unknown;
}

cv::Mat imread_secure(const std::string& path) {
    FILE* fp = fopen(path.c_str(), "rb");
    if (!fp) return cv::Mat();

    ImgFmt fmt = sniff_fmt(fp);
    if (fmt == ImgFmt::Unknown) { fclose(fp); return cv::Mat(); }

    // Decode based on fmt (not on filename suffix), with strict size/bounds checks.
    // ...

    fclose(fp);
    return cv::Mat();
}
```

Team standard:
- Prefer magic-byte/header sniffing over extension checks.
- If the header doesn’t match the expected decoder, return an error/empty result.
- Keep fallback logic conservative; never let extension-based routing be the sole authority for untrusted inputs.