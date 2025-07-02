---
title: Optimize memory access
description: When implementing performance-critical algorithms, carefully consider
  memory access patterns. Document alignment assumptions when using low-level operations
  like `MemoryMarshal.Cast` or SIMD intrinsics. Prefer reference-based APIs over pinning
  to avoid GC interference. For bulk operations, use specialized helpers like `LoadUnsafe(ref
  T source, nuint...
repository: dotnet/runtime
label: Algorithms
language: C#
comments_count: 9
repository_stars: 16578
---

When implementing performance-critical algorithms, carefully consider memory access patterns. Document alignment assumptions when using low-level operations like `MemoryMarshal.Cast` or SIMD intrinsics. Prefer reference-based APIs over pinning to avoid GC interference. For bulk operations, use specialized helpers like `LoadUnsafe(ref T source, nuint elementOffset)` instead of pointer arithmetic.

```csharp
// Less optimal: Uses pinning that can hinder GC
unsafe void ProcessBytes(ReadOnlySpan<byte> source)
{
    fixed (byte* ptr = source)
    {
        for (int i = 0; i < source.Length - 7; i += 8)
        {
            ulong value = *(ulong*)(ptr + i);
            // Process 8 bytes at once
        }
    }
}

// More optimal: Uses ref-based API without pinning
void ProcessBytes(ReadOnlySpan<byte> source)
{
    ref byte sourceRef = ref MemoryMarshal.GetReference(source);
    for (int i = 0; i + 8 <= source.Length; i += 8)
    {
        // Use LoadUnsafe with explicit offset
        ulong value = Vector64.LoadUnsafe(ref sourceRef, (nuint)i);
        // Process 8 bytes at once
    }
}
```

When handling data in bulk, consider the impact of alignment requirements and document edge cases like zero-length inputs. For operations on numeric types, select appropriate operations based on platform characteristics (e.g., prefer unsigned division over signed when possible).


[
  {
    "discussion_id": "2169548434",
    "pr_number": 116903,
    "pr_file": "src/coreclr/nativeaot/Common/src/Internal/Runtime/MethodTable.cs",
    "created_at": "2025-06-26T17:27:17+00:00",
    "commented_code": "}\n        }\n\n        // Returns rank of multi-dimensional array rank, 0 for sz arrays\n        internal int MultiDimensionalArrayRank\n        {\n            get\n            {\n                Debug.Assert(this.IsArray);\n\n                int boundsSize = (int)this.ParameterizedTypeShape - SZARRAY_BASE_SIZE;\n                // Multidim array case: Base size includes space for two Int32s\n                // (upper and lower bound) per each dimension of the array.\n                return boundsSize / (2 * sizeof(int));",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2169548434",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116903,
        "pr_file": "src/coreclr/nativeaot/Common/src/Internal/Runtime/MethodTable.cs",
        "discussion_id": "2169548434",
        "commented_code": "@@ -419,6 +419,20 @@ internal int ArrayRank\n             }\n         }\n \n+        // Returns rank of multi-dimensional array rank, 0 for sz arrays\n+        internal int MultiDimensionalArrayRank\n+        {\n+            get\n+            {\n+                Debug.Assert(this.IsArray);\n+\n+                int boundsSize = (int)this.ParameterizedTypeShape - SZARRAY_BASE_SIZE;\n+                // Multidim array case: Base size includes space for two Int32s\n+                // (upper and lower bound) per each dimension of the array.\n+                return boundsSize / (2 * sizeof(int));",
        "comment_created_at": "2025-06-26T17:27:17+00:00",
        "comment_author": "jkotas",
        "comment_body": "Should this be done as unsigned division to match CoreCLR? \r\n\r\nSigned division is extra instructions: https://godbolt.org/z/cxxWP67n6",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "984222859",
    "pr_number": 76423,
    "pr_file": "src/libraries/System.Private.CoreLib/src/System/SpanHelpers.T.cs",
    "created_at": "2022-09-30T05:36:57+00:00",
    "commented_code": "}\n\n        [MethodImpl(MethodImplOptions.AggressiveInlining)]\n        private static int ComputeLastIndex<T>(nint offset, Vector128<T> equals) where T : struct\n        {\n            uint notEqualsElements = equals.ExtractMostSignificantBits();\n            int index = 31 - BitOperations.LeadingZeroCount(notEqualsElements); // 31 = 32 (bits in Int32) - 1 (indexing from zero)\n            return (int)offset + index;\n        }\n\n        [MethodImpl(MethodImplOptions.AggressiveInlining)]\n        private static int ComputeLastIndex<T>(nint offset, Vector256<T> equals) where T : struct\n        private static int ComputeLastIndex<TVector, T>(nint offset, TVector equals)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "984222859",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 76423,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/SpanHelpers.T.cs",
        "discussion_id": "984222859",
        "commented_code": "@@ -2635,40 +2596,51 @@ internal static int IndexOfAnyValueType<T>(ref T searchSpace, T value0, T value1\n         }\n \n         [MethodImpl(MethodImplOptions.AggressiveInlining)]\n-        private static int ComputeLastIndex<T>(nint offset, Vector128<T> equals) where T : struct\n-        {\n-            uint notEqualsElements = equals.ExtractMostSignificantBits();\n-            int index = 31 - BitOperations.LeadingZeroCount(notEqualsElements); // 31 = 32 (bits in Int32) - 1 (indexing from zero)\n-            return (int)offset + index;\n-        }\n-\n-        [MethodImpl(MethodImplOptions.AggressiveInlining)]\n-        private static int ComputeLastIndex<T>(nint offset, Vector256<T> equals) where T : struct\n+        private static int ComputeLastIndex<TVector, T>(nint offset, TVector equals)",
        "comment_created_at": "2022-09-30T05:36:57+00:00",
        "comment_author": "tannergooding",
        "comment_body": "This is working around the lack of variable sized `ExtractMostSignificantBits`.\r\n\r\nIt's not pretty, but it works and ideally gets replaced in .NET 8 as part of the `VectorMask` work...",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "783634009",
    "pr_number": 63722,
    "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
    "created_at": "2022-01-13T05:08:34+00:00",
    "commented_code": "// (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n            // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n\n            if (Avx2.IsSupported)\n            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n\n            if (Vector256.IsHardwareAccelerated)\n            {\n                // JIT does not support code hoisting for SIMD yet\n                Vector256<byte> zero = Vector256<byte>.Zero;\n                fixed (bool* ptr = values)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "783634009",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 63722,
        "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
        "discussion_id": "783634009",
        "commented_code": "@@ -145,81 +147,32 @@ public unsafe BitArray(bool[] values)\n             // (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n             // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n \n-            if (Avx2.IsSupported)\n+            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n+\n+            if (Vector256.IsHardwareAccelerated)\n             {\n-                // JIT does not support code hoisting for SIMD yet\n-                Vector256<byte> zero = Vector256<byte>.Zero;\n-                fixed (bool* ptr = values)",
        "comment_created_at": "2022-01-13T05:08:34+00:00",
        "comment_author": "tannergooding",
        "comment_body": "We now expose helper intrinsics that directly operate on `ref`: `LoadUnsafe(ref T source, nuint elementOffset)`.\r\n\r\nThis helps avoid pinning, which can have measurable overhead for small counts and which can hinder the GC in the case of long inputs.\r\n\r\nIt likewise helps improve readability over the pattern we are already utilizing in parts of the BCL where we were using `Unsafe.ReadUnaligned` + `Unsafe.Add` + `Unsafe.As`.\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "783634761",
    "pr_number": 63722,
    "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
    "created_at": "2022-01-13T05:10:52+00:00",
    "commented_code": "// (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n            // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n\n            if (Avx2.IsSupported)\n            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n\n            if (Vector256.IsHardwareAccelerated)\n            {\n                // JIT does not support code hoisting for SIMD yet\n                Vector256<byte> zero = Vector256<byte>.Zero;\n                fixed (bool* ptr = values)\n                for (; (i + Vector256ByteCount) <= (uint)values.Length; i += Vector256ByteCount)\n                {\n                    for (; (i + Vector256ByteCount) <= (uint)values.Length; i += Vector256ByteCount)\n                    {\n                        Vector256<byte> vector = Avx.LoadVector256((byte*)ptr + i);\n                        Vector256<byte> isFalse = Avx2.CompareEqual(vector, zero);\n                        int result = Avx2.MoveMask(isFalse);\n                        m_array[i / 32u] = ~result;\n                    }\n                    Vector256<byte> vector = Vector256.LoadUnsafe(ref value, i);\n                    Vector256<byte> isFalse = Vector256.Equals(vector, Vector256<byte>.Zero);\n\n                    uint result = isFalse.ExtractMostSignificantBits();",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "783634761",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 63722,
        "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
        "discussion_id": "783634761",
        "commented_code": "@@ -145,81 +147,32 @@ public unsafe BitArray(bool[] values)\n             // (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n             // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n \n-            if (Avx2.IsSupported)\n+            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n+\n+            if (Vector256.IsHardwareAccelerated)\n             {\n-                // JIT does not support code hoisting for SIMD yet\n-                Vector256<byte> zero = Vector256<byte>.Zero;\n-                fixed (bool* ptr = values)\n+                for (; (i + Vector256ByteCount) <= (uint)values.Length; i += Vector256ByteCount)\n                 {\n-                    for (; (i + Vector256ByteCount) <= (uint)values.Length; i += Vector256ByteCount)\n-                    {\n-                        Vector256<byte> vector = Avx.LoadVector256((byte*)ptr + i);\n-                        Vector256<byte> isFalse = Avx2.CompareEqual(vector, zero);\n-                        int result = Avx2.MoveMask(isFalse);\n-                        m_array[i / 32u] = ~result;\n-                    }\n+                    Vector256<byte> vector = Vector256.LoadUnsafe(ref value, i);\n+                    Vector256<byte> isFalse = Vector256.Equals(vector, Vector256<byte>.Zero);\n+\n+                    uint result = isFalse.ExtractMostSignificantBits();",
        "comment_created_at": "2022-01-13T05:10:52+00:00",
        "comment_author": "tannergooding",
        "comment_body": "`ExtractMostSignificantBits` behaves just like `MoveMask` on x86/x64. This is also exposed by `WASM` as `bitmask`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "783635223",
    "pr_number": 63722,
    "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
    "created_at": "2022-01-13T05:12:15+00:00",
    "commented_code": "// (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n            // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n\n            if (Avx2.IsSupported)\n            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n\n            if (Vector256.IsHardwareAccelerated)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "783635223",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 63722,
        "pr_file": "src/libraries/System.Collections/src/System/Collections/BitArray.cs",
        "discussion_id": "783635223",
        "commented_code": "@@ -145,81 +147,32 @@ public unsafe BitArray(bool[] values)\n             // (true for any non-zero values, false for 0) - any values between 2-255 will be interpreted as false.\n             // Instead, We compare with zeroes (== false) then negate the result to ensure compatibility.\n \n-            if (Avx2.IsSupported)\n+            ref byte value = ref Unsafe.As<bool, byte>(ref MemoryMarshal.GetArrayDataReference<bool>(values));\n+\n+            if (Vector256.IsHardwareAccelerated)",
        "comment_created_at": "2022-01-13T05:12:15+00:00",
        "comment_author": "tannergooding",
        "comment_body": "I've preserved the `Vector256` path given that it was already here and I would presume has undergone the necessary checks to ensure it is worth doing on x86/x64.\r\n\r\nArm64 doesn't support `V256` and so will only go down the `V128` codepath.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "650255034",
    "pr_number": 54006,
    "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
    "created_at": "2021-06-11T20:44:12+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System.Numerics;\nusing System.Runtime.CompilerServices;\n\nnamespace System.Runtime.InteropServices\n{\n    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n    public static unsafe class NativeMemory\n    {\n        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate. This should be a multiple of <paramref name=\"alignment\" /> for portability.</param>\n        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c> greater than or equal to <c>sizeof(void*)</c> for portability.</param>\n        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory failed.</exception>\n        /// <remarks>\n        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n        /// </remarks>\n        [CLSCompliant(false)]\n        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n        {\n            void* result = null;\n\n            // The C standard doesn't define what a valid alignment is, however POSIX requires a power of 2 >= sizeof(void*)\n            if (BitOperations.IsPow2(alignment) && (alignment >= (uint)sizeof(void*)))",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "650255034",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "650255034",
        "commented_code": "@@ -0,0 +1,149 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate. This should be a multiple of <paramref name=\"alignment\" /> for portability.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c> greater than or equal to <c>sizeof(void*)</c> for portability.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            void* result = null;\n+\n+            // The C standard doesn't define what a valid alignment is, however POSIX requires a power of 2 >= sizeof(void*)\n+            if (BitOperations.IsPow2(alignment) && (alignment >= (uint)sizeof(void*)))",
        "comment_created_at": "2021-06-11T20:44:12+00:00",
        "comment_author": "tannergooding",
        "comment_body": "This only validates the alignment is a power of 2 as that is relatively cheap. Also validating that `byteCount % alignment == 0` would be fairly expensive.",
        "pr_file_module": null
      },
      {
        "comment_id": "650280339",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "650255034",
        "commented_code": "@@ -0,0 +1,149 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate. This should be a multiple of <paramref name=\"alignment\" /> for portability.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c> greater than or equal to <c>sizeof(void*)</c> for portability.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            void* result = null;\n+\n+            // The C standard doesn't define what a valid alignment is, however POSIX requires a power of 2 >= sizeof(void*)\n+            if (BitOperations.IsPow2(alignment) && (alignment >= (uint)sizeof(void*)))",
        "comment_created_at": "2021-06-11T21:45:26+00:00",
        "comment_author": "jkotas",
        "comment_body": ">  Also validating that byteCount % alignment == 0 would be fairly expensive.\r\n\r\nYou do not need to use `%` once you know that the alignment is power of 2.",
        "pr_file_module": null
      },
      {
        "comment_id": "651059254",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "650255034",
        "commented_code": "@@ -0,0 +1,149 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate. This should be a multiple of <paramref name=\"alignment\" /> for portability.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c> greater than or equal to <c>sizeof(void*)</c> for portability.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            void* result = null;\n+\n+            // The C standard doesn't define what a valid alignment is, however POSIX requires a power of 2 >= sizeof(void*)\n+            if (BitOperations.IsPow2(alignment) && (alignment >= (uint)sizeof(void*)))",
        "comment_created_at": "2021-06-14T15:36:10+00:00",
        "comment_author": "tannergooding",
        "comment_body": "I've simplified the alignment check to just `if ((alignment % (uint)sizeof(void*)) == 0)`, which will generate simply `test dl, 7` (or `test dl, 3` for 32-bit)",
        "pr_file_module": null
      },
      {
        "comment_id": "651060706",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "650255034",
        "commented_code": "@@ -0,0 +1,149 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate. This should be a multiple of <paramref name=\"alignment\" /> for portability.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c> greater than or equal to <c>sizeof(void*)</c> for portability.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            void* result = null;\n+\n+            // The C standard doesn't define what a valid alignment is, however POSIX requires a power of 2 >= sizeof(void*)\n+            if (BitOperations.IsPow2(alignment) && (alignment >= (uint)sizeof(void*)))",
        "comment_created_at": "2021-06-14T15:37:57+00:00",
        "comment_author": "tannergooding",
        "comment_body": "I'll also add in a check for `byteCount` since that can just be `(byteCount & (alignment - 1)) == 0`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "652173333",
    "pr_number": 54006,
    "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
    "created_at": "2021-06-15T21:42:59+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System.Numerics;\nusing System.Runtime.CompilerServices;\n\nnamespace System.Runtime.InteropServices\n{\n    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n    public static unsafe class NativeMemory\n    {\n        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate.</param>\n        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c>.</param>\n        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n        /// <exception cref=\"ArgumentException\"><paramref name=\"alignment\" /> is not a power of two.</exception>\n        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory with <paramref name=\"alignment\" /> failed.</exception>\n        /// <remarks>\n        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n        /// </remarks>\n        [CLSCompliant(false)]\n        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n        {\n            if (!BitOperations.IsPow2(alignment))\n            {\n                // The C standard doesn't define what a valid alignment is, however Windows and POSIX requires a power of 2\n                ThrowHelper.ThrowArgumentException(ExceptionResource.Argument_AlignmentMustBePow2);\n            }\n\n            // The C standard and POSIX requires size to be a multiple of alignment and we want an \"empty\" allocation for zero\n            // POSIX additionally requires alignment to be at least sizeof(void*)\n\n            // The adjustment for byteCount can overflow here, but such overflow is \"harmless\". This is because of the requirement\n            // that alignment be a power of two and that byteCount be a multiple of alignment. Given both of these constraints\n            // we should only overflow for byteCount > (nuint.MaxValue & ~(alignment - 1)). When such an overflow occurs we will\n            // get a result that is less than alignment which will cause the allocation to fail.\n\n            void* result = Interop.Sys.AlignedAlloc(Math.Max(alignment, sizeof(void*)), (byteCount != 0) ? (byteCount + (alignment - 1)) & ~(alignment - 1) : alignment);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "652173333",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "652173333",
        "commented_code": "@@ -0,0 +1,158 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c>.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"ArgumentException\"><paramref name=\"alignment\" /> is not a power of two.</exception>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory with <paramref name=\"alignment\" /> failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            if (!BitOperations.IsPow2(alignment))\n+            {\n+                // The C standard doesn't define what a valid alignment is, however Windows and POSIX requires a power of 2\n+                ThrowHelper.ThrowArgumentException(ExceptionResource.Argument_AlignmentMustBePow2);\n+            }\n+\n+            // The C standard and POSIX requires size to be a multiple of alignment and we want an \"empty\" allocation for zero\n+            // POSIX additionally requires alignment to be at least sizeof(void*)\n+\n+            // The adjustment for byteCount can overflow here, but such overflow is \"harmless\". This is because of the requirement\n+            // that alignment be a power of two and that byteCount be a multiple of alignment. Given both of these constraints\n+            // we should only overflow for byteCount > (nuint.MaxValue & ~(alignment - 1)). When such an overflow occurs we will\n+            // get a result that is less than alignment which will cause the allocation to fail.\n+\n+            void* result = Interop.Sys.AlignedAlloc(Math.Max(alignment, sizeof(void*)), (byteCount != 0) ? (byteCount + (alignment - 1)) & ~(alignment - 1) : alignment);",
        "comment_created_at": "2021-06-15T21:42:59+00:00",
        "comment_author": "jkotas",
        "comment_body": "Does the formula for the second argument need to use the alignment after it has been bumped up to `sizeof(void*)`?",
        "pr_file_module": null
      },
      {
        "comment_id": "652173571",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "652173333",
        "commented_code": "@@ -0,0 +1,158 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c>.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"ArgumentException\"><paramref name=\"alignment\" /> is not a power of two.</exception>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory with <paramref name=\"alignment\" /> failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            if (!BitOperations.IsPow2(alignment))\n+            {\n+                // The C standard doesn't define what a valid alignment is, however Windows and POSIX requires a power of 2\n+                ThrowHelper.ThrowArgumentException(ExceptionResource.Argument_AlignmentMustBePow2);\n+            }\n+\n+            // The C standard and POSIX requires size to be a multiple of alignment and we want an \"empty\" allocation for zero\n+            // POSIX additionally requires alignment to be at least sizeof(void*)\n+\n+            // The adjustment for byteCount can overflow here, but such overflow is \"harmless\". This is because of the requirement\n+            // that alignment be a power of two and that byteCount be a multiple of alignment. Given both of these constraints\n+            // we should only overflow for byteCount > (nuint.MaxValue & ~(alignment - 1)). When such an overflow occurs we will\n+            // get a result that is less than alignment which will cause the allocation to fail.\n+\n+            void* result = Interop.Sys.AlignedAlloc(Math.Max(alignment, sizeof(void*)), (byteCount != 0) ? (byteCount + (alignment - 1)) & ~(alignment - 1) : alignment);",
        "comment_created_at": "2021-06-15T21:43:32+00:00",
        "comment_author": "tannergooding",
        "comment_body": "Yes, it does. Thanks for the catch.\r\n\r\nWill update and add a test covering this scenario.",
        "pr_file_module": null
      },
      {
        "comment_id": "652866312",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 54006,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/Runtime/InteropServices/NativeMemory.Unix.cs",
        "discussion_id": "652173333",
        "commented_code": "@@ -0,0 +1,158 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Numerics;\n+using System.Runtime.CompilerServices;\n+\n+namespace System.Runtime.InteropServices\n+{\n+    /// <summary>This class contains methods that are mainly used to manage native memory.</summary>\n+    public static unsafe class NativeMemory\n+    {\n+        /// <summary>Allocates an aligned block of memory of the specified size and alignment, in bytes.</summary>\n+        /// <param name=\"byteCount\">The size, in bytes, of the block to allocate.</param>\n+        /// <param name=\"alignment\">The alignment, in bytes, of the block to allocate. This must be a power of <c>2</c>.</param>\n+        /// <returns>A pointer to the allocated aligned block of memory.</returns>\n+        /// <exception cref=\"ArgumentException\"><paramref name=\"alignment\" /> is not a power of two.</exception>\n+        /// <exception cref=\"OutOfMemoryException\">Allocating <paramref name=\"byteCount\" /> of memory with <paramref name=\"alignment\" /> failed.</exception>\n+        /// <remarks>\n+        ///     <para>This method allows <paramref name=\"byteCount\" /> to be <c>0</c> and will return a valid pointer that should not be dereferenced and that should be passed to free to avoid memory leaks.</para>\n+        ///     <para>This method is a thin wrapper over the C <c>aligned_alloc</c> API or a platform dependent aligned allocation API such as <c>_aligned_malloc</c> on Win32.</para>\n+        ///     <para>This method is not compatible with <see cref=\"Free\" /> or <see cref=\"Realloc\" />, instead <see cref=\"AlignedFree\" /> should be called.</para>\n+        /// </remarks>\n+        [CLSCompliant(false)]\n+        public static void* AlignedAlloc(nuint byteCount, nuint alignment)\n+        {\n+            if (!BitOperations.IsPow2(alignment))\n+            {\n+                // The C standard doesn't define what a valid alignment is, however Windows and POSIX requires a power of 2\n+                ThrowHelper.ThrowArgumentException(ExceptionResource.Argument_AlignmentMustBePow2);\n+            }\n+\n+            // The C standard and POSIX requires size to be a multiple of alignment and we want an \"empty\" allocation for zero\n+            // POSIX additionally requires alignment to be at least sizeof(void*)\n+\n+            // The adjustment for byteCount can overflow here, but such overflow is \"harmless\". This is because of the requirement\n+            // that alignment be a power of two and that byteCount be a multiple of alignment. Given both of these constraints\n+            // we should only overflow for byteCount > (nuint.MaxValue & ~(alignment - 1)). When such an overflow occurs we will\n+            // get a result that is less than alignment which will cause the allocation to fail.\n+\n+            void* result = Interop.Sys.AlignedAlloc(Math.Max(alignment, sizeof(void*)), (byteCount != 0) ? (byteCount + (alignment - 1)) & ~(alignment - 1) : alignment);",
        "comment_created_at": "2021-06-16T16:44:41+00:00",
        "comment_author": "tannergooding",
        "comment_body": "Should be resolved now.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2112477469",
    "pr_number": 116057,
    "pr_file": "src/libraries/System.Private.CoreLib/src/System/String.Comparison.cs",
    "created_at": "2025-05-28T18:07:40+00:00",
    "commented_code": "switch (length)\n                {\n                    default:\n#if USE_XXHASH3\n                        if (length >= XxHash3Threshold)\n                        {\n                            uint byteLength = (uint)length * 2; // never overflows\n                            return unchecked((int)System.IO.Hashing.XxHash3.NonRandomizedHashToUInt64((byte*)src, byteLength));",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2112477469",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116057,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/String.Comparison.cs",
        "discussion_id": "2112477469",
        "commented_code": "@@ -871,6 +860,14 @@ internal static unsafe int GetNonRandomizedHashCode(ReadOnlySpan<char> span)\n                 switch (length)\n                 {\n                     default:\n+#if USE_XXHASH3\n+                        if (length >= XxHash3Threshold)\n+                        {\n+                            uint byteLength = (uint)length * 2; // never overflows\n+                            return unchecked((int)System.IO.Hashing.XxHash3.NonRandomizedHashToUInt64((byte*)src, byteLength));",
        "comment_created_at": "2025-05-28T18:07:40+00:00",
        "comment_author": "stephentoub",
        "comment_body": "Is there any way we can improve the implementation of XxHash3 to the point where we could just always use it rather than having the fallbacks for < XxHash3Threshold? Or it's simply not possible because the number of instructions required is simply higher?",
        "pr_file_module": null
      },
      {
        "comment_id": "2112648531",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116057,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/String.Comparison.cs",
        "discussion_id": "2112477469",
        "commented_code": "@@ -871,6 +860,14 @@ internal static unsafe int GetNonRandomizedHashCode(ReadOnlySpan<char> span)\n                 switch (length)\n                 {\n                     default:\n+#if USE_XXHASH3\n+                        if (length >= XxHash3Threshold)\n+                        {\n+                            uint byteLength = (uint)length * 2; // never overflows\n+                            return unchecked((int)System.IO.Hashing.XxHash3.NonRandomizedHashToUInt64((byte*)src, byteLength));",
        "comment_created_at": "2025-05-28T19:57:52+00:00",
        "comment_author": "EgorBo",
        "comment_body": "to be fair. I am not sure, it seems to be quite noticeably slower for small inputs. Do you mind if I investigate that in a separate PR?",
        "pr_file_module": null
      },
      {
        "comment_id": "2113841168",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116057,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/String.Comparison.cs",
        "discussion_id": "2112477469",
        "commented_code": "@@ -871,6 +860,14 @@ internal static unsafe int GetNonRandomizedHashCode(ReadOnlySpan<char> span)\n                 switch (length)\n                 {\n                     default:\n+#if USE_XXHASH3\n+                        if (length >= XxHash3Threshold)\n+                        {\n+                            uint byteLength = (uint)length * 2; // never overflows\n+                            return unchecked((int)System.IO.Hashing.XxHash3.NonRandomizedHashToUInt64((byte*)src, byteLength));",
        "comment_created_at": "2025-05-29T12:26:24+00:00",
        "comment_author": "filipnavara",
        "comment_body": "It's a bit of slippery slope to mix different hash algorithms for different string lengths. Once you start mixing strings of the length below and above the threshold any of the guarantees about collisions become somewhat weaker and unpredictable.",
        "pr_file_module": null
      },
      {
        "comment_id": "2113872621",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116057,
        "pr_file": "src/libraries/System.Private.CoreLib/src/System/String.Comparison.cs",
        "discussion_id": "2112477469",
        "commented_code": "@@ -871,6 +860,14 @@ internal static unsafe int GetNonRandomizedHashCode(ReadOnlySpan<char> span)\n                 switch (length)\n                 {\n                     default:\n+#if USE_XXHASH3\n+                        if (length >= XxHash3Threshold)\n+                        {\n+                            uint byteLength = (uint)length * 2; // never overflows\n+                            return unchecked((int)System.IO.Hashing.XxHash3.NonRandomizedHashToUInt64((byte*)src, byteLength));",
        "comment_created_at": "2025-05-29T12:46:49+00:00",
        "comment_author": "EgorBo",
        "comment_body": "Yeah I've just pushed an unconditional switch to XxHash3, will see how it goes",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1976356858",
    "pr_number": 111643,
    "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
    "created_at": "2025-03-01T07:39:48+00:00",
    "commented_code": "// Compute in 8 byte chunks\n            if (source.Length >= sizeof(ulong))\n            {\n                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n\n                for (int i = 0; i < longLength; i += sizeof(ulong))\n                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1976356858",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T07:39:48+00:00",
        "comment_author": "GrabYourPitchforks",
        "comment_body": "This deserves a source comment justifying why the usage of `MemoryMarshal.Cast` is acceptable. Typically this is because the data is known to be aligned or because unaligned accesses are known to be legal on the underlying platform.\r\n\r\n(Same comment elsewhere.)",
        "pr_file_module": null
      },
      {
        "comment_id": "1976421510",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T13:46:57+00:00",
        "comment_author": "EgorBo",
        "comment_body": "@GrabYourPitchforks we have a million places where we do unaligned reads/writes like this (basically, all MemoryMarshal.Read/Write/Cast, Unsafe.Read/ReadUnligned/Write/WriteUnligned, Unsafe.As, etc. in the BCL, do we want to mark them all with such comments? \ud83d\ude42 also, for non-pinned stuff GC can change the alignment dynamically. .NET simply won't work on a platform where such reads/writes may throw, we always rely on OS to fixup them.\r\n\r\nThe only tricky cases are some floating point (structs with them) loads/store on arm32 where Linux-arm32 doesn't do fixup for them (just nobody bothered implementing that in the OS). And, well, some atomic instructions on some platforms expect aligned data",
        "pr_file_module": null
      },
      {
        "comment_id": "1976429989",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T14:32:23+00:00",
        "comment_author": "jkotas",
        "comment_body": "> basically, all MemoryMarshal.Read/Write/Cast, Unsafe.Read/ReadUnligned/Write/WriteUnligned, Unsafe.As\r\n\r\nMemoryMarshal.Cast and Unsafe.As are the only ones with the potential alignment problem, there are not that many, and we have been accepting fixes to make the core more portable (e.g. https://github.com/dotnet/runtime/pull/98812).\r\n\r\n> The only tricky cases\r\n\r\nAnd the platforms/architecture that we never heard of that Unity may run on.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976433147",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T14:53:44+00:00",
        "comment_author": "EgorBo",
        "comment_body": "> MemoryMarshal.Cast and Unsafe.As are the only ones with the potential alignment problem\r\n\r\nSure, but what I meant is that we actually don't do anything special for e.g. Unsafe.ReadUnaligned - we don't lower it down to a memset or unrolled per-byte loop, it still is going to fail on a platform where such reads aren't fixed by the OS. At least on CoreCLR/NAOT\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1976434012",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T14:59:43+00:00",
        "comment_author": "EgorBo",
        "comment_body": "Let me change it to a safer pattern then",
        "pr_file_module": null
      },
      {
        "comment_id": "1976434835",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:06:00+00:00",
        "comment_author": "jkotas",
        "comment_body": "> it still is going to fail on a platform where such reads aren't fixed by the OS. At least on CoreCLR/NAOT\r\n\r\nIf we end up targeting a platform like that, the JIT will need to be fixed up to make `Unsafe.ReadUnaligned` work as appropriate.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976435237",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:09:28+00:00",
        "comment_author": "EgorBo",
        "comment_body": "> > it still is going to fail on a platform where such reads aren't fixed by the OS. At least on CoreCLR/NAOT\r\n> \r\n> If we end up targeting a platform like that, the JIT will need to be fixed up to make `Unsafe.ReadUnaligned` work as appropriate.\r\n\r\nI suspect that would be a terrible perform regression, most of the places where we use these unaligned loads/stores are optimizations to process multiple elements at once, so it will work the opposite way for such targets",
        "pr_file_module": null
      },
      {
        "comment_id": "1976436295",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:17:13+00:00",
        "comment_author": "MichalPetryka",
        "comment_body": "> > it still is going to fail on a platform where such reads aren't fixed by the OS. At least on CoreCLR/NAOT\r\n> \r\n> If we end up targeting a platform like that, the JIT will need to be fixed up to make `Unsafe.ReadUnaligned` work as appropriate.\r\n\r\nRISC-V already does have unaligned access support as optional, it can be queried with a syscall though (it has 4 values, fast, slow, unsupported and undefined, in all but the first case the compilers should do single byte loads for unaligned). I'm not sure what's the current plan of supporting that by Samsung though.\r\nWorth noting that SIMD unaligned support is also optional there and that supporting unaligned for only SIMD or only scalar are both legal.\r\n\r\nAnother problematic platform is NativeAOT-LLVM (and maybe Mono-LLVM), since LLVM has non-explicit unaligned loads as UB and can emit broken code for them if we try to do them.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976436878",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:21:08+00:00",
        "comment_author": "EgorBo",
        "comment_body": "> > > it still is going to fail on a platform where such reads aren't fixed by the OS. At least on CoreCLR/NAOT\r\n> > \r\n> > \r\n> > If we end up targeting a platform like that, the JIT will need to be fixed up to make `Unsafe.ReadUnaligned` work as appropriate.\r\n> \r\n> RISC-V already does have unaligned access support as optional, it can be queried with a syscall though (it has 4 values, fast, slow, unsupported and undefined, in all but the first case the compilers should do single byte loads for unaligned). I'm not sure what's the current plan of supporting that by Samsung though. Worth noting that SIMD unaligned support is also optional there and that supporting unaligned for only SIMD or only scalar are both legal.\r\n> \r\n> Another problematic platform is NativeAOT-LLVM, since LLVM has non-explicit unaligned loads as UB and can emit broken code for them if we try to do them.\r\n\r\nI don't see how any of that is remotely related here, though. It's arm64-accelerated path with CRC",
        "pr_file_module": null
      },
      {
        "comment_id": "1976438751",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:35:03+00:00",
        "comment_author": "EgorBo",
        "comment_body": "@GrabYourPitchforks @jkotas I'm actually curious what would be a canonical way to walk a span of bytes and process 8 bytes at a time via `ulong` without using unsafe APIs or introducing portability problems with misalignment",
        "pr_file_module": null
      },
      {
        "comment_id": "1976439012",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:37:34+00:00",
        "comment_author": "EgorBo",
        "comment_body": "Something like this probably?\r\n```cs\r\nvoid DoWork(ReadOnlySpan<byte> bytes)\r\n{\r\n    int longLength = bytes.Length & ~0x7;\r\n    bytes = bytes.Slice(0, longLength);\r\n    for (int i = 0; i < bytes.Length; i+= 8)\r\n    {\r\n        ulong value = BitConverter.ToUInt64(bytes[i..]); // or MemoryMarshal.Read\r\n    }\r\n    // process the remaining bytes\r\n    // ...\r\n}\r\n```\r\nI guess it's one of those cases when safe code doesn't read better than unsafe \ud83d\ude42 ",
        "pr_file_module": null
      },
      {
        "comment_id": "1976441497",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:54:14+00:00",
        "comment_author": "tannergooding",
        "comment_body": "`BinaryPrimitives.ReadInt64LittleEndian` is likely \"better\" than `BitConverter`, it's at least more explicit. `MemoryMarshal.Read` is likely something we want to avoid in \"safe\" code because of where it lives (even if it does bounds check/etc).\r\n\r\nToday, we basically have to pick between being \"safe\" or being \"efficient\". We can get semi-efficient for scalars, but that's potentially leaving 2-64x perf on the table, depending on platform/scenario.\r\n\r\nIf the JIT could elide bounds checks for `V128.Create(rospan)` then we have a safe way to operate on the data. We can alternatively centralize the unsafe code behind a core helper, for example we have `InvokeSpanIntoSpan` and a pattern that makes use of \"functional interfaces + generics\" to do this for `TensorPrimitives`. This at least reduces risk as the logic that accesses memory can be well tested and not duplicated everywhere. We'll never be able to get rid of *all* unsafe code either, something like `TensorPrimitives` which needs to handle large data needs to be able to pin so it gets access to non-temporal loads/stores, for example.\r\n\r\nI think our goal should therefore really be to move paths like these to use centralized helpers instead of trying to rewrite them to be \"safe\". We know they're important to perf and we know they benefit from unsafe today, so lets pull some of the `InvokeSpanIntoSpan` and `Aggregate` helpers so that cases like this are functionally rewritten to `=> Aggregate<T, IdentityOperator<T>, Crc32Operator<T>>(x)` and all the \"dangerous\" code is centralized. When the JIT finally gets support for eliding bounds checks over `V128.Create(rospan)` that one helper can be rewritten to use the safe pattern and the rest of the BCL implicitly gets it. We can add a number of `Debug.Assert`, memory access checks, and even potentially `opt-in` forced validation path (such as would lightup via a feature switch) to help ensure robustness in the interim.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976442053",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T15:57:40+00:00",
        "comment_author": "jkotas",
        "comment_body": "> I guess it's one of those cases when safe code doesn't read better than unsafe\r\n\r\nIt is because of we have not designed safe APIs that make this kind of code look good.\r\n\r\nI think that that best you can do using existing .NET APIs is approximation of \"eat the span\" pattern that's idiomatic in golang:\r\n```csharp\r\nwhile (span.Length >= 8)\r\n{\r\n   ulong v = BitConverter.ToInt64(span);\r\n\r\n   ...\r\n\r\n   span = span.Slice(8);\r\n}\r\n```\r\n\r\nNew APIs can make it look better:\r\n```\r\nwhile (BitConverter.TryRead(span, out long v))\r\n{\r\n   ...\r\n\r\n   span = span.Slice(8);\r\n}\r\n```\r\n\r\nAnother alternative is to introduce iterators that are idiomatic in Rust:\r\n```\r\n// Rust equivalent is for chunk in data.array_chunks::<8>()\r\nforeach (long v in span.IterateAsInt64())\r\n{\r\n...\r\n}\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1976443651",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T16:08:32+00:00",
        "comment_author": "jkotas",
        "comment_body": "> `=> Aggregate<T, IdentityOperator<T>, Crc32Operator<T>>(x)`\r\n\r\nI get that this pattern is centralizing the unsafe code, but I do not think that it reads well.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976444381",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T16:13:32+00:00",
        "comment_author": "tannergooding",
        "comment_body": "> I get that this pattern is centralizing the unsafe code, but I do not think that it reads well.\r\n\r\nIt doesn't today, but the long term goal would be to get something like `functional interfaces` into the language so that you can rather have something like `=> Aggregate(span, (previous, value) => Crc32(previous, value))` instead and the lambda binds to the `TOperation` given `where TOperation : IOperation<....>` so that it becomes \"prettier\"\r\n\r\nWe're not always going to be able to hit the trifecta of `safe`, `efficient`, and `pretty`. We can, however, strike a decent enough balance between them and as a long term goal push towards improving the scenarios where it falls down.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976449597",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 111643,
        "pr_file": "src/libraries/System.IO.Hashing/src/System/IO/Hashing/Crc32.Arm.cs",
        "discussion_id": "1976356858",
        "commented_code": "@@ -17,22 +17,18 @@ private static uint UpdateScalarArm64(uint crc, ReadOnlySpan<byte> source)\n             // Compute in 8 byte chunks\n             if (source.Length >= sizeof(ulong))\n             {\n-                ref byte ptr = ref MemoryMarshal.GetReference(source);\n                 int longLength = source.Length & ~0x7; // Exclude trailing bytes not a multiple of 8\n-\n-                for (int i = 0; i < longLength; i += sizeof(ulong))\n+                foreach (ulong l in MemoryMarshal.Cast<byte, ulong>(source.Slice(0, longLength)))",
        "comment_created_at": "2025-03-01T16:35:50+00:00",
        "comment_author": "EgorBo",
        "comment_body": "> I think that that best you can do using existing\r\n\r\nLooks like all of these patterns will require extra work on the JIT side to optimize them, especially the iterator one",
        "pr_file_module": null
      }
    ]
  }
]
