---
title: Minimize unnecessary work
description: 'Optimize performance by reducing the amount of computation performed,
  especially on data that won''t appear in the final result. Apply these strategies:'
repository: JetBrains/kotlin
label: Performance Optimization
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Optimize performance by reducing the amount of computation performed, especially on data that won't appear in the final result. Apply these strategies:

1) **Filter early**: Filter collections before performing expensive transformations like sorting
```kotlin
// Suboptimal: Sorts all elements, then removes private ones
functions.sortBy(KmFunction::name)
functions.removeIf { it.visibility.isPrivate }

// Optimized: Removes private elements first, then sorts only what's needed
functions.removeIf { it.visibility.isPrivate }
functions.sortBy(KmFunction::name)
```

2) **Short-circuit common cases**: Add early returns for special cases like empty collections or single elements
```kotlin
public fun <T> Array<out Array<out T>>.flatten(): List<T> {
    if (isEmpty()) return emptyList() // Early return for common case
    // Regular processing...
}
```

3) **Cache expensive results**: Use memoization for operations that may be called repeatedly with the same input
```kotlin
private val containsCache = mutableMapOf<IrDeclaration, Boolean>()

override fun containsDeclaration(declaration: IrDeclaration): Boolean = 
    containsCache.getOrPut(declaration) {
        // Expensive computation here
    }
```

4) **Optimize for expected usage patterns**: Special-case handle common scenarios based on benchmarks
```kotlin
// Optimization for common no-argument functions
if (parameters.isEmpty()) {
    return reflectionCall {
        caller.call(if (isSuspend) arrayOf(continuationArgument) else emptyArray()) as R
    }
}
```

Always verify your optimizations with benchmarks to ensure they provide measurable benefits in real-world scenarios.


[
  {
    "discussion_id": "2030201923",
    "pr_number": 5426,
    "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
    "created_at": "2025-04-06T16:43:45+00:00",
    "commented_code": "* @sample samples.collections.Collections.Transformations.take\n */\npublic inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "2030201923",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
        "discussion_id": "2030201923",
        "commented_code": "@@ -5295,13 +5285,16 @@ public inline fun CharArray.takeLastWhile(predicate: (Char) -> Boolean): List<Ch\n  * @sample samples.collections.Collections.Transformations.take\n  */\n public inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
        "comment_created_at": "2025-04-06T16:43:45+00:00",
        "comment_author": "hoangchungk53qx1",
        "comment_body": " it will be easier to read, i think, with equivalent performance \r\n```suggestion\r\npublic inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {\r\n    var i = 0\r\n    while (i < size && predicate(this[i])) i++\r\n    return if (i == 0) emptyList() else this.copyOfRange(0, i).asList()\r\n}\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2034023407",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
        "discussion_id": "2030201923",
        "commented_code": "@@ -5295,13 +5285,16 @@ public inline fun CharArray.takeLastWhile(predicate: (Char) -> Boolean): List<Ch\n  * @sample samples.collections.Collections.Transformations.take\n  */\n public inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
        "comment_created_at": "2025-04-08T20:57:31+00:00",
        "comment_author": "alexismanin",
        "comment_body": "I've checked the impact of removing the special case handling, and it looks like it is noticeable. On the benchmark result below, your suggestion is the \"takeWhileSuggestion\" case. We see that for array size 0 and 1, it is a little less fast than the proposed optimization : \r\n\r\n![image](https://github.com/user-attachments/assets/6658ed62-7e86-405e-882d-14aeb94e6e7b)\r\n\r\nTherefore, I think we should keep the when as it is now.\r\n\r\nP.S: If you want to double-check this, I've added the suggestions in my benchmark project [on the `test-pr-suggestions` branch](https://github.com/alexismanin/kt-benchmark-array-to-list/tree/test-pr-suggestions)",
        "pr_file_module": null
      },
      {
        "comment_id": "2034521735",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
        "discussion_id": "2030201923",
        "commented_code": "@@ -5295,13 +5285,16 @@ public inline fun CharArray.takeLastWhile(predicate: (Char) -> Boolean): List<Ch\n  * @sample samples.collections.Collections.Transformations.take\n  */\n public inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
        "comment_created_at": "2025-04-09T06:16:18+00:00",
        "comment_author": "alexismanin",
        "comment_body": "@hoangchungk53qx1 : After second thought, your simplification makes sense.\r\n\r\nI realized that it just miss a condition to improve its performance when *output list has only one element* (which is a broader case than my current implementation, which only accounts for cases when *input* array has only one element) : \r\n\r\n```kt\r\nreturn if (i == 0) emptyList()\r\n       else if (i == 1) listOf(this[0])\r\n       else copyOfRange(0, i).asList()\r\n```\r\n\r\nI've launched a benchmark by modifying your suggestion so that the final return condition accounts for cases where i is 1. It greatly improves performance, for two cases of the benchmark : \r\n\r\n  1. Input array has one element\r\n  2. Output list has only one element (in the benchmark, this is the case where input array is of size 3. We only take the first element from it)\r\n\r\nI will soon apply you suggestion with this tweak, and I think we will be good then.\r\n\r\nHere is a glimpse of updated benchmark results:\r\n\r\n![image](https://github.com/user-attachments/assets/93635032-d766-4869-b4ad-748f4f27c63a)\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2034602921",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
        "discussion_id": "2030201923",
        "commented_code": "@@ -5295,13 +5285,16 @@ public inline fun CharArray.takeLastWhile(predicate: (Char) -> Boolean): List<Ch\n  * @sample samples.collections.Collections.Transformations.take\n  */\n public inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
        "comment_created_at": "2025-04-09T06:55:23+00:00",
        "comment_author": "hoangchungk53qx1",
        "comment_body": "Nice @alexismanin ",
        "pr_file_module": null
      },
      {
        "comment_id": "2035221456",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/common/src/generated/_Arrays.kt",
        "discussion_id": "2030201923",
        "commented_code": "@@ -5295,13 +5285,16 @@ public inline fun CharArray.takeLastWhile(predicate: (Char) -> Boolean): List<Ch\n  * @sample samples.collections.Collections.Transformations.take\n  */\n public inline fun <T> Array<out T>.takeWhile(predicate: (T) -> Boolean): List<T> {",
        "comment_created_at": "2025-04-09T12:03:13+00:00",
        "comment_author": "alexismanin",
        "comment_body": "I've pushed the change to `takeWhile` function.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2030205112",
    "pr_number": 5426,
    "pr_file": "libraries/stdlib/src/kotlin/collections/Arrays.kt",
    "created_at": "2025-04-06T16:57:37+00:00",
    "commented_code": "* @sample samples.collections.Arrays.Transformations.flattenArray\n */\npublic fun <T> Array<out Array<out T>>.flatten(): List<T> {\n    val result = ArrayList<T>(sumOf { it.size })\n    for (element in this) {\n        result.addAll(element)\n    return when (size) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "2030205112",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5426,
        "pr_file": "libraries/stdlib/src/kotlin/collections/Arrays.kt",
        "discussion_id": "2030205112",
        "commented_code": "@@ -17,11 +17,26 @@ import kotlin.contracts.*\n  * @sample samples.collections.Arrays.Transformations.flattenArray\n  */\n public fun <T> Array<out Array<out T>>.flatten(): List<T> {\n-    val result = ArrayList<T>(sumOf { it.size })\n-    for (element in this) {\n-        result.addAll(element)\n+    return when (size) {",
        "comment_created_at": "2025-04-06T16:57:37+00:00",
        "comment_author": "hoangchungk53qx1",
        "comment_body": "can early return \r\n\r\nif (isEmpty()) return emptyList()\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1437223453",
    "pr_number": 5233,
    "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiMetadataProcessor.kt",
    "created_at": "2023-12-27T19:44:29+00:00",
    "commented_code": "}\n\nprivate fun KmDeclarationContainer.removePrivateDeclarations() {\n    functions.sortBy(KmFunction::name)\n    properties.sortBy(KmProperty::name)\n\n    functions.removeIf { it.visibility.isPrivate }\n    properties.removeIf { it.visibility.isPrivate }",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1437223453",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5233,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiMetadataProcessor.kt",
        "discussion_id": "1437223453",
        "commented_code": "@@ -163,6 +163,9 @@ private fun KmPackage.removePrivateDeclarations() {\n }\n \n private fun KmDeclarationContainer.removePrivateDeclarations() {\n+    functions.sortBy(KmFunction::name)\n+    properties.sortBy(KmProperty::name)\n+\n     functions.removeIf { it.visibility.isPrivate }\n     properties.removeIf { it.visibility.isPrivate }",
        "comment_created_at": "2023-12-27T19:44:29+00:00",
        "comment_author": "JakeWharton",
        "comment_body": "```suggestion\n    functions.removeIf { it.visibility.isPrivate }\n    properties.removeIf { it.visibility.isPrivate }\n\n    functions.sortBy(KmFunction::name)\n    properties.sortBy(KmProperty::name)\n```\nMight as well sort after removal. Otherwise you're wasting time on sorting entries that are destined to be removed anyway.\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1437256954",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5233,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiMetadataProcessor.kt",
        "discussion_id": "1437223453",
        "commented_code": "@@ -163,6 +163,9 @@ private fun KmPackage.removePrivateDeclarations() {\n }\n \n private fun KmDeclarationContainer.removePrivateDeclarations() {\n+    functions.sortBy(KmFunction::name)\n+    properties.sortBy(KmProperty::name)\n+\n     functions.removeIf { it.visibility.isPrivate }\n     properties.removeIf { it.visibility.isPrivate }",
        "comment_created_at": "2023-12-27T21:18:43+00:00",
        "comment_author": "Tagakov",
        "comment_body": "Thanks for catching it, noticed it after creating the PR but forgot to push.",
        "pr_file_module": null
      },
      {
        "comment_id": "1440951272",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5233,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiMetadataProcessor.kt",
        "discussion_id": "1437223453",
        "commented_code": "@@ -163,6 +163,9 @@ private fun KmPackage.removePrivateDeclarations() {\n }\n \n private fun KmDeclarationContainer.removePrivateDeclarations() {\n+    functions.sortBy(KmFunction::name)\n+    properties.sortBy(KmProperty::name)\n+\n     functions.removeIf { it.visibility.isPrivate }\n     properties.removeIf { it.visibility.isPrivate }",
        "comment_created_at": "2024-01-03T21:07:15+00:00",
        "comment_author": "Tagakov",
        "comment_body": "My dog ate it! I swear!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1263892613",
    "pr_number": 5156,
    "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
    "created_at": "2023-07-14T15:58:00+00:00",
    "commented_code": "override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n            packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n\n    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n                    // When producing per-file caches, some declarations might be generated by the stub generator.\n                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n\n    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1263892613",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-14T15:58:00+00:00",
        "comment_author": "homuroll",
        "comment_body": "What is the purpose of inlining of `declaration.konanLibrary` here?",
        "pr_file_module": null
      },
      {
        "comment_id": "1264212481",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-14T22:15:53+00:00",
        "comment_author": "MarkCMann",
        "comment_body": "To memoize more of the calls, by inlining the konan library recursive calls here we can store the result for the top level class in addition to all nested classes. \r\n\r\nOverall this method showed up on the profiler as being very heavy due to the repeated recursive calls in KonanLibrary -- I opted to memoize the data in the llvm module specification class instead of trying to add it to the IrDeclaration or adding a global cache to konanLibrary in IrUtils. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1265352329",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-17T13:26:09+00:00",
        "comment_author": "ddolovov",
        "comment_body": "Just a question (I don't know the right answer):\r\n\r\nIs `fun containsDeclaration(declaration: IrDeclaration)` actually called for the same declaration multiple times? If no, then probably we should cache per `KotlinLibrary` or per smth else but not per `IrDeclaration`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1265458783",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-17T14:32:30+00:00",
        "comment_author": "homuroll",
        "comment_body": "Got it. Please, add a comment here explaining this, and probably some short comment/reference to here from `declaration.konanLibrary` (in case someone decides to change it).",
        "pr_file_module": null
      },
      {
        "comment_id": "1265950218",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-17T22:10:13+00:00",
        "comment_author": "MarkCMann",
        "comment_body": "@ddolovov I'm not sure that I understand your concern here. Is this more related to the size of the cache? \r\n\r\nWith this change I've moved the recursive calls into the llvm contains declaration function so now that function should be called multiple times for `IrDeclarations`. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1266570240",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-18T10:22:19+00:00",
        "comment_author": "ddolovov",
        "comment_body": "> so now that function should be called multiple times for IrDeclarations.\r\n\r\nYou mean it could be called multiple times for the same instance of `IrDeclaration` (and therefore it makes sense to cache per-declaration), right?",
        "pr_file_module": null
      },
      {
        "comment_id": "1269759652",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/LlvmModuleSpecificationImpl.kt",
        "discussion_id": "1263892613",
        "commented_code": "@@ -28,10 +29,18 @@ internal abstract class LlvmModuleSpecificationBase(protected val cachedLibrarie\n     override fun containsPackageFragment(packageFragment: IrPackageFragment): Boolean =\n             packageFragment.konanLibrary.let { it == null || containsLibrary(it) }\n \n-    override fun containsDeclaration(declaration: IrDeclaration): Boolean =\n-            declaration.konanLibrary.let { it == null || containsLibrary(it) }\n-                    // When producing per-file caches, some declarations might be generated by the stub generator.\n-                    && declaration.getPackageFragment() !is IrExternalPackageFragment\n+    private val containsCache = mutableMapOf<IrDeclaration, Boolean>()\n+\n+    override fun containsDeclaration(declaration: IrDeclaration): Boolean = containsCache.getOrPut(declaration) {",
        "comment_created_at": "2023-07-20T17:24:07+00:00",
        "comment_author": "MarkCMann",
        "comment_body": "That's correct, especially for parent IrDeclarations they would be called repeatedly",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1265278095",
    "pr_number": 5156,
    "pr_file": "compiler/ir/serialization.common/src/org/jetbrains/kotlin/backend/common/overrides/FakeOverrides.kt",
    "created_at": "2023-07-17T12:24:19+00:00",
    "commented_code": "}\n\n    fun provideFakeOverrides() {\n        val entries = fakeOverrideCandidates.entries\n        val entries = fakeOverrideCandidates.entries.toMutableList()",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1265278095",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "compiler/ir/serialization.common/src/org/jetbrains/kotlin/backend/common/overrides/FakeOverrides.kt",
        "discussion_id": "1265278095",
        "commented_code": "@@ -286,10 +286,9 @@ class FakeOverrideBuilder(\n     }\n \n     fun provideFakeOverrides() {\n-        val entries = fakeOverrideCandidates.entries\n+        val entries = fakeOverrideCandidates.entries.toMutableList()",
        "comment_created_at": "2023-07-17T12:24:19+00:00",
        "comment_author": "ddolovov",
        "comment_body": "The `fakeOverrideCandidates` map should be cleaned at the exit from `provideFakeOverrides()`. Otherwise we would have repeated work each time we deserialize body of inline function: https://github.com/JetBrains/kotlin/blob/883102c4c68d1b73216c6ebebed0b288f0fa7978/kotlin-native/backend.native/compiler/ir/backend.native/src/org/jetbrains/kotlin/backend/konan/serialization/KonanIrlinker.kt#L938",
        "pr_file_module": null
      },
      {
        "comment_id": "1265940209",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5156,
        "pr_file": "compiler/ir/serialization.common/src/org/jetbrains/kotlin/backend/common/overrides/FakeOverrides.kt",
        "discussion_id": "1265278095",
        "commented_code": "@@ -286,10 +286,9 @@ class FakeOverrideBuilder(\n     }\n \n     fun provideFakeOverrides() {\n-        val entries = fakeOverrideCandidates.entries\n+        val entries = fakeOverrideCandidates.entries.toMutableList()",
        "comment_created_at": "2023-07-17T21:53:22+00:00",
        "comment_author": "MarkCMann",
        "comment_body": "Ah okay it wasn't obvious to me if the entry set returned was the actual underlying entryset for the map and could therefore mutate the entries in the map. I can add a call to clear the fakeOverrideCandidates here",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1020631690",
    "pr_number": 4840,
    "pr_file": "core/reflection.jvm/src/kotlin/reflect/jvm/internal/KCallableImpl.kt",
    "created_at": "2022-11-12T01:19:53+00:00",
    "commented_code": "return if (isAnnotationConstructor) callAnnotationConstructor(args) else callDefaultMethod(args, null)\n    }\n\n    private val _absentArguments = ReflectProperties.lazySoft {\n        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\n        val maskSize = (parameters.size + Integer.SIZE - 1) / Integer.SIZE\n\n        // arguments with masks and DefaultConstructorMarker or MethodHandle\n        // +1 is argument for DefaultConstructorMarker or MethodHandle\n        val arguments = arrayOfNulls<Any?>(parameterSize + maskSize + 1)\n\n        // set absent values\n        parameters.forEach { parameter ->\n            if (parameter.isOptional && !parameter.type.isInlineClassType) {\n                // For inline class types, the javaType refers to the underlying type of the inline class,\n                // but we have to pass null in order to mark the argument as absent for InlineClassAwareCaller.\n                arguments[parameter.index] = defaultPrimitiveValue(parameter.type.javaType)\n            } else if (parameter.isVararg) {\n                arguments[parameter.index] = defaultEmptyArray(parameter.type)\n            }\n        }\n\n        for (i in 0 until maskSize) {\n            arguments[parameterSize + i] = 0\n        }\n\n        arguments\n    }\n\n    private fun getAbsentArguments(): Array<Any?> = _absentArguments().clone()\n\n    // See ArgumentGenerator#generate\n    internal fun callDefaultMethod(args: Map<KParameter, Any?>, continuationArgument: Continuation<*>?): R {\n        val parameters = parameters\n        val arguments = ArrayList<Any?>(parameters.size)\n        var mask = 0\n        val masks = ArrayList<Int>(1)\n        var index = 0\n        var anyOptional = false\n        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1020631690",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4840,
        "pr_file": "core/reflection.jvm/src/kotlin/reflect/jvm/internal/KCallableImpl.kt",
        "discussion_id": "1020631690",
        "commented_code": "@@ -112,65 +112,87 @@ internal abstract class KCallableImpl<out R> : KCallable<R>, KTypeParameterOwner\n         return if (isAnnotationConstructor) callAnnotationConstructor(args) else callDefaultMethod(args, null)\n     }\n \n+    private val _absentArguments = ReflectProperties.lazySoft {\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\n+        val maskSize = (parameters.size + Integer.SIZE - 1) / Integer.SIZE\n+\n+        // arguments with masks and DefaultConstructorMarker or MethodHandle\n+        // +1 is argument for DefaultConstructorMarker or MethodHandle\n+        val arguments = arrayOfNulls<Any?>(parameterSize + maskSize + 1)\n+\n+        // set absent values\n+        parameters.forEach { parameter ->\n+            if (parameter.isOptional && !parameter.type.isInlineClassType) {\n+                // For inline class types, the javaType refers to the underlying type of the inline class,\n+                // but we have to pass null in order to mark the argument as absent for InlineClassAwareCaller.\n+                arguments[parameter.index] = defaultPrimitiveValue(parameter.type.javaType)\n+            } else if (parameter.isVararg) {\n+                arguments[parameter.index] = defaultEmptyArray(parameter.type)\n+            }\n+        }\n+\n+        for (i in 0 until maskSize) {\n+            arguments[parameterSize + i] = 0\n+        }\n+\n+        arguments\n+    }\n+\n+    private fun getAbsentArguments(): Array<Any?> = _absentArguments().clone()\n+\n     // See ArgumentGenerator#generate\n     internal fun callDefaultMethod(args: Map<KParameter, Any?>, continuationArgument: Continuation<*>?): R {\n         val parameters = parameters\n-        val arguments = ArrayList<Any?>(parameters.size)\n-        var mask = 0\n-        val masks = ArrayList<Int>(1)\n-        var index = 0\n-        var anyOptional = false\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)",
        "comment_created_at": "2022-11-12T01:19:53+00:00",
        "comment_author": "k163377",
        "comment_body": "The following optimization to no-argument functions was found to be nearly twice as fast as 638d89c.\r\nDoes this optimization look like it should be incorporated?\r\n\r\n```\r\nBenchmark                          Mode  Cnt         Score         Error  Units\r\nMeasurement.zero                  thrpt    4  22299885.316 \u00b1  295995.533  ops/s\r\nMeasurement.fiveWithDefault       thrpt    4   1927106.356 \u00b1  225032.224  ops/s\r\nMeasurement.fiveWithoutDefault    thrpt    4   2460623.502 \u00b1   96649.714  ops/s\r\nMeasurement.oneWithDefault        thrpt    4   5384826.666 \u00b1  340254.100  ops/s\r\nMeasurement.oneWithoutDefault     thrpt    4   5654229.984 \u00b1 5914104.417  ops/s\r\nMeasurement.twentyWithDefault     thrpt    4    510341.805 \u00b1    2940.113  ops/s\r\nMeasurement.twentyWithoutDefault  thrpt    4    739231.653 \u00b1   21298.002  ops/s\r\n```\r\n\r\n```suggestion\r\n        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\r\n\r\n        // Optimization for general no-argument functions.        \r\n        if (parameters.isEmpty()) {\r\n            @Suppress(\"UNCHECKED_CAST\")\r\n            return reflectionCall {\r\n                caller.call(if (isSuspend) arrayOf(continuationArgument) else emptyArray()) as R\r\n            }\r\n        } else if (parameters.size == 1) {\r\n            parameters.first().takeIf { it.kind != KParameter.Kind.VALUE }?.let { parameter ->\r\n                @Suppress(\"UNCHECKED_CAST\")\r\n                return reflectionCall {\r\n                    caller.call(if (isSuspend) arrayOf(args[parameter], continuationArgument) else arrayOf(args[parameter])) as R\r\n                }\r\n            }\r\n        }\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1031902832",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4840,
        "pr_file": "core/reflection.jvm/src/kotlin/reflect/jvm/internal/KCallableImpl.kt",
        "discussion_id": "1020631690",
        "commented_code": "@@ -112,65 +112,87 @@ internal abstract class KCallableImpl<out R> : KCallable<R>, KTypeParameterOwner\n         return if (isAnnotationConstructor) callAnnotationConstructor(args) else callDefaultMethod(args, null)\n     }\n \n+    private val _absentArguments = ReflectProperties.lazySoft {\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\n+        val maskSize = (parameters.size + Integer.SIZE - 1) / Integer.SIZE\n+\n+        // arguments with masks and DefaultConstructorMarker or MethodHandle\n+        // +1 is argument for DefaultConstructorMarker or MethodHandle\n+        val arguments = arrayOfNulls<Any?>(parameterSize + maskSize + 1)\n+\n+        // set absent values\n+        parameters.forEach { parameter ->\n+            if (parameter.isOptional && !parameter.type.isInlineClassType) {\n+                // For inline class types, the javaType refers to the underlying type of the inline class,\n+                // but we have to pass null in order to mark the argument as absent for InlineClassAwareCaller.\n+                arguments[parameter.index] = defaultPrimitiveValue(parameter.type.javaType)\n+            } else if (parameter.isVararg) {\n+                arguments[parameter.index] = defaultEmptyArray(parameter.type)\n+            }\n+        }\n+\n+        for (i in 0 until maskSize) {\n+            arguments[parameterSize + i] = 0\n+        }\n+\n+        arguments\n+    }\n+\n+    private fun getAbsentArguments(): Array<Any?> = _absentArguments().clone()\n+\n     // See ArgumentGenerator#generate\n     internal fun callDefaultMethod(args: Map<KParameter, Any?>, continuationArgument: Continuation<*>?): R {\n         val parameters = parameters\n-        val arguments = ArrayList<Any?>(parameters.size)\n-        var mask = 0\n-        val masks = ArrayList<Int>(1)\n-        var index = 0\n-        var anyOptional = false\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)",
        "comment_created_at": "2022-11-24T23:02:29+00:00",
        "comment_author": "udalov",
        "comment_body": "For the 0-parameters case, it looks good! But for the 1 parameter, I'm not really sure, the code is getting quite complicated already. Besides, `Measurement.oneWithoutDefault` regressed in your results after this change, if I understand them correctly? I propose to keep the 0-parameter case only.",
        "pr_file_module": null
      },
      {
        "comment_id": "1031954118",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4840,
        "pr_file": "core/reflection.jvm/src/kotlin/reflect/jvm/internal/KCallableImpl.kt",
        "discussion_id": "1020631690",
        "commented_code": "@@ -112,65 +112,87 @@ internal abstract class KCallableImpl<out R> : KCallable<R>, KTypeParameterOwner\n         return if (isAnnotationConstructor) callAnnotationConstructor(args) else callDefaultMethod(args, null)\n     }\n \n+    private val _absentArguments = ReflectProperties.lazySoft {\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\n+        val maskSize = (parameters.size + Integer.SIZE - 1) / Integer.SIZE\n+\n+        // arguments with masks and DefaultConstructorMarker or MethodHandle\n+        // +1 is argument for DefaultConstructorMarker or MethodHandle\n+        val arguments = arrayOfNulls<Any?>(parameterSize + maskSize + 1)\n+\n+        // set absent values\n+        parameters.forEach { parameter ->\n+            if (parameter.isOptional && !parameter.type.isInlineClassType) {\n+                // For inline class types, the javaType refers to the underlying type of the inline class,\n+                // but we have to pass null in order to mark the argument as absent for InlineClassAwareCaller.\n+                arguments[parameter.index] = defaultPrimitiveValue(parameter.type.javaType)\n+            } else if (parameter.isVararg) {\n+                arguments[parameter.index] = defaultEmptyArray(parameter.type)\n+            }\n+        }\n+\n+        for (i in 0 until maskSize) {\n+            arguments[parameterSize + i] = 0\n+        }\n+\n+        arguments\n+    }\n+\n+    private fun getAbsentArguments(): Array<Any?> = _absentArguments().clone()\n+\n     // See ArgumentGenerator#generate\n     internal fun callDefaultMethod(args: Map<KParameter, Any?>, continuationArgument: Continuation<*>?): R {\n         val parameters = parameters\n-        val arguments = ArrayList<Any?>(parameters.size)\n-        var mask = 0\n-        val masks = ArrayList<Int>(1)\n-        var index = 0\n-        var anyOptional = false\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)",
        "comment_created_at": "2022-11-25T02:21:59+00:00",
        "comment_author": "k163377",
        "comment_body": "> Measurement.oneWithoutDefault regressed in your results after this change, if I understand them correctly?\r\n\r\nI ran the benchmark again with almost the same content, but there did not seem to be any regression in performance.\r\nSince the benchmark was run on a local machine, there must have been something going on in the background during this measurement.\r\n\r\n**1e1cd3a**\r\n\r\n```\r\nBenchmark                          Mode  Cnt         Score         Error  Units\r\nMeasurement.fiveWithDefault       thrpt    4   1713974.649 \u00b1  807978.785  ops/s\r\nMeasurement.fiveWithoutDefault    thrpt    4   2402911.282 \u00b1  116905.232  ops/s\r\nMeasurement.oneWithDefault        thrpt    4   5018352.177 \u00b1 3050333.309  ops/s\r\nMeasurement.oneWithoutDefault     thrpt    4   6338081.662 \u00b1  384633.083  ops/s\r\nMeasurement.twentyWithDefault     thrpt    4    506022.842 \u00b1   28381.148  ops/s\r\nMeasurement.twentyWithoutDefault  thrpt    4    721987.591 \u00b1   78852.517  ops/s\r\nMeasurement.zero                  thrpt    4  12727105.089 \u00b1  188029.864  ops/s\r\n```\r\n\r\n**after-zero-arg-opt2**\r\n\r\n```\r\nBenchmark                          Mode  Cnt         Score         Error  Units\r\nMeasurement.fiveWithDefault       thrpt    4   1880153.629 \u00b1  232291.891  ops/s\r\nMeasurement.fiveWithoutDefault    thrpt    4   2388820.000 \u00b1   97785.718  ops/s\r\nMeasurement.oneWithDefault        thrpt    4   5276216.078 \u00b1  327025.056  ops/s\r\nMeasurement.oneWithoutDefault     thrpt    4   6251850.821 \u00b1  497046.067  ops/s\r\nMeasurement.twentyWithDefault     thrpt    4    516927.278 \u00b1   13448.841  ops/s\r\nMeasurement.twentyWithoutDefault  thrpt    4    728619.156 \u00b1   36904.744  ops/s\r\nMeasurement.zero                  thrpt    4  21774799.243 \u00b1 1534253.147  ops/s\r\n```\r\n\r\n---\r\n\r\nI agree that it is complicated.\r\nI have pushed for a fix.\r\n[68a9741](https://github.com/JetBrains/kotlin/pull/4840/commits/68a9741ee2307eb0d27b2a77c1124c8aa267597a)\r\n\r\nI did not measure benchmark results with the one-parameter branch removed, but at least there is no reason for the score to drop since the target of the measurement is a top-level function.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1031956945",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4840,
        "pr_file": "core/reflection.jvm/src/kotlin/reflect/jvm/internal/KCallableImpl.kt",
        "discussion_id": "1020631690",
        "commented_code": "@@ -112,65 +112,87 @@ internal abstract class KCallableImpl<out R> : KCallable<R>, KTypeParameterOwner\n         return if (isAnnotationConstructor) callAnnotationConstructor(args) else callDefaultMethod(args, null)\n     }\n \n+    private val _absentArguments = ReflectProperties.lazySoft {\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)\n+        val maskSize = (parameters.size + Integer.SIZE - 1) / Integer.SIZE\n+\n+        // arguments with masks and DefaultConstructorMarker or MethodHandle\n+        // +1 is argument for DefaultConstructorMarker or MethodHandle\n+        val arguments = arrayOfNulls<Any?>(parameterSize + maskSize + 1)\n+\n+        // set absent values\n+        parameters.forEach { parameter ->\n+            if (parameter.isOptional && !parameter.type.isInlineClassType) {\n+                // For inline class types, the javaType refers to the underlying type of the inline class,\n+                // but we have to pass null in order to mark the argument as absent for InlineClassAwareCaller.\n+                arguments[parameter.index] = defaultPrimitiveValue(parameter.type.javaType)\n+            } else if (parameter.isVararg) {\n+                arguments[parameter.index] = defaultEmptyArray(parameter.type)\n+            }\n+        }\n+\n+        for (i in 0 until maskSize) {\n+            arguments[parameterSize + i] = 0\n+        }\n+\n+        arguments\n+    }\n+\n+    private fun getAbsentArguments(): Array<Any?> = _absentArguments().clone()\n+\n     // See ArgumentGenerator#generate\n     internal fun callDefaultMethod(args: Map<KParameter, Any?>, continuationArgument: Continuation<*>?): R {\n         val parameters = parameters\n-        val arguments = ArrayList<Any?>(parameters.size)\n-        var mask = 0\n-        val masks = ArrayList<Int>(1)\n-        var index = 0\n-        var anyOptional = false\n+        val parameterSize = parameters.size + (if (isSuspend) 1 else 0)",
        "comment_created_at": "2022-11-25T02:30:17+00:00",
        "comment_author": "k163377",
        "comment_body": "As a side note, the reason I proposed the original form is that `getter` is a typical example of a function that takes only instances as arguments.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "994632200",
    "pr_number": 4982,
    "pr_file": "compiler/fir/providers/src/org/jetbrains/kotlin/fir/scopes/impl/FirTypeIntersectionScopeContext.kt",
    "created_at": "2022-10-13T13:16:48+00:00",
    "commented_code": "val result = mutableListOf<ResultOfIntersection<D>>()\n\n        while (allMembersWithScope.size > 1) {\n            val maxByVisibility = findMemberWithMaxVisibility(allMembersWithScope)\n            val extractBothWaysWithPrivate = overrideService.extractBothWaysOverridable(maxByVisibility, allMembersWithScope, overrideChecker)\n            val extractedOverrides = extractBothWaysWithPrivate.filterNotTo(mutableListOf()) {\n                Visibilities.isPrivate((it.member.fir as FirMemberDeclaration).visibility)\n            }.takeIf { it.isNotEmpty() } ?: extractBothWaysWithPrivate\n            val baseMembersForIntersection = extractedOverrides.calcBaseMembersForIntersectionOverride()\n            if (baseMembersForIntersection.size > 1) {\n                val (mostSpecific, scopeForMostSpecific) = overrideService.selectMostSpecificMember(\n                    baseMembersForIntersection,\n                    ReturnTypeCalculatorForFullBodyResolve\n                )\n                val intersectionOverrideContext = ContextForIntersectionOverrideConstruction(\n                    mostSpecific,\n                    this,\n                    extractedOverrides,\n                    scopeForMostSpecific\n                )\n                result += ResultOfIntersection.NonTrivial(\n                    intersectionOverrides,\n                    intersectionOverrideContext,\n                    extractedOverrides,\n                    containingScope = null\n                )\n            val groupWithPrivate =\n                overrideService.extractBothWaysOverridable(allMembersWithScope.maxByVisibility(), allMembersWithScope, overrideChecker)\n            val group = groupWithPrivate.filter { !Visibilities.isPrivate(it.member.fir.visibility) }.ifEmpty { groupWithPrivate }\n            val singleRealImplementation = group.size == 1 ||\n                    group.mapTo(mutableSetOf()) { it.member.fir.unwrapSubstitutionOverrides().symbol }.size == 1\n            val directOverrides = if (singleRealImplementation) group else group.onlyDirectlyInherited()",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "994632200",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4982,
        "pr_file": "compiler/fir/providers/src/org/jetbrains/kotlin/fir/scopes/impl/FirTypeIntersectionScopeContext.kt",
        "discussion_id": "994632200",
        "commented_code": "@@ -161,32 +156,21 @@ class FirTypeIntersectionScopeContext(\n         val result = mutableListOf<ResultOfIntersection<D>>()\n \n         while (allMembersWithScope.size > 1) {\n-            val maxByVisibility = findMemberWithMaxVisibility(allMembersWithScope)\n-            val extractBothWaysWithPrivate = overrideService.extractBothWaysOverridable(maxByVisibility, allMembersWithScope, overrideChecker)\n-            val extractedOverrides = extractBothWaysWithPrivate.filterNotTo(mutableListOf()) {\n-                Visibilities.isPrivate((it.member.fir as FirMemberDeclaration).visibility)\n-            }.takeIf { it.isNotEmpty() } ?: extractBothWaysWithPrivate\n-            val baseMembersForIntersection = extractedOverrides.calcBaseMembersForIntersectionOverride()\n-            if (baseMembersForIntersection.size > 1) {\n-                val (mostSpecific, scopeForMostSpecific) = overrideService.selectMostSpecificMember(\n-                    baseMembersForIntersection,\n-                    ReturnTypeCalculatorForFullBodyResolve\n-                )\n-                val intersectionOverrideContext = ContextForIntersectionOverrideConstruction(\n-                    mostSpecific,\n-                    this,\n-                    extractedOverrides,\n-                    scopeForMostSpecific\n-                )\n-                result += ResultOfIntersection.NonTrivial(\n-                    intersectionOverrides,\n-                    intersectionOverrideContext,\n-                    extractedOverrides,\n-                    containingScope = null\n-                )\n+            val groupWithPrivate =\n+                overrideService.extractBothWaysOverridable(allMembersWithScope.maxByVisibility(), allMembersWithScope, overrideChecker)\n+            val group = groupWithPrivate.filter { !Visibilities.isPrivate(it.member.fir.visibility) }.ifEmpty { groupWithPrivate }\n+            val singleRealImplementation = group.size == 1 ||\n+                    group.mapTo(mutableSetOf()) { it.member.fir.unwrapSubstitutionOverrides().symbol }.size == 1\n+            val directOverrides = if (singleRealImplementation) group else group.onlyDirectlyInherited()",
        "comment_created_at": "2022-10-13T13:16:48+00:00",
        "comment_author": "dzharkov",
        "comment_body": "I would add a comment that this `if` looks more like an optimization than a semantically necessary thing.\nOr, probably I would just use `group.onlyDirectlyInherited()` unconditionally.\n",
        "pr_file_module": null
      },
      {
        "comment_id": "994734316",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4982,
        "pr_file": "compiler/fir/providers/src/org/jetbrains/kotlin/fir/scopes/impl/FirTypeIntersectionScopeContext.kt",
        "discussion_id": "994632200",
        "commented_code": "@@ -161,32 +156,21 @@ class FirTypeIntersectionScopeContext(\n         val result = mutableListOf<ResultOfIntersection<D>>()\n \n         while (allMembersWithScope.size > 1) {\n-            val maxByVisibility = findMemberWithMaxVisibility(allMembersWithScope)\n-            val extractBothWaysWithPrivate = overrideService.extractBothWaysOverridable(maxByVisibility, allMembersWithScope, overrideChecker)\n-            val extractedOverrides = extractBothWaysWithPrivate.filterNotTo(mutableListOf()) {\n-                Visibilities.isPrivate((it.member.fir as FirMemberDeclaration).visibility)\n-            }.takeIf { it.isNotEmpty() } ?: extractBothWaysWithPrivate\n-            val baseMembersForIntersection = extractedOverrides.calcBaseMembersForIntersectionOverride()\n-            if (baseMembersForIntersection.size > 1) {\n-                val (mostSpecific, scopeForMostSpecific) = overrideService.selectMostSpecificMember(\n-                    baseMembersForIntersection,\n-                    ReturnTypeCalculatorForFullBodyResolve\n-                )\n-                val intersectionOverrideContext = ContextForIntersectionOverrideConstruction(\n-                    mostSpecific,\n-                    this,\n-                    extractedOverrides,\n-                    scopeForMostSpecific\n-                )\n-                result += ResultOfIntersection.NonTrivial(\n-                    intersectionOverrides,\n-                    intersectionOverrideContext,\n-                    extractedOverrides,\n-                    containingScope = null\n-                )\n+            val groupWithPrivate =\n+                overrideService.extractBothWaysOverridable(allMembersWithScope.maxByVisibility(), allMembersWithScope, overrideChecker)\n+            val group = groupWithPrivate.filter { !Visibilities.isPrivate(it.member.fir.visibility) }.ifEmpty { groupWithPrivate }\n+            val singleRealImplementation = group.size == 1 ||\n+                    group.mapTo(mutableSetOf()) { it.member.fir.unwrapSubstitutionOverrides().symbol }.size == 1\n+            val directOverrides = if (singleRealImplementation) group else group.onlyDirectlyInherited()",
        "comment_created_at": "2022-10-13T14:39:12+00:00",
        "comment_author": "pyos",
        "comment_body": "BTW I'm also wondering here if `singleRealImplementation` should be computed *after* removing transitively inherited declarations, but I'm not familiar enough with this code to come up with different test cases.",
        "pr_file_module": null
      },
      {
        "comment_id": "994749406",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4982,
        "pr_file": "compiler/fir/providers/src/org/jetbrains/kotlin/fir/scopes/impl/FirTypeIntersectionScopeContext.kt",
        "discussion_id": "994632200",
        "commented_code": "@@ -161,32 +156,21 @@ class FirTypeIntersectionScopeContext(\n         val result = mutableListOf<ResultOfIntersection<D>>()\n \n         while (allMembersWithScope.size > 1) {\n-            val maxByVisibility = findMemberWithMaxVisibility(allMembersWithScope)\n-            val extractBothWaysWithPrivate = overrideService.extractBothWaysOverridable(maxByVisibility, allMembersWithScope, overrideChecker)\n-            val extractedOverrides = extractBothWaysWithPrivate.filterNotTo(mutableListOf()) {\n-                Visibilities.isPrivate((it.member.fir as FirMemberDeclaration).visibility)\n-            }.takeIf { it.isNotEmpty() } ?: extractBothWaysWithPrivate\n-            val baseMembersForIntersection = extractedOverrides.calcBaseMembersForIntersectionOverride()\n-            if (baseMembersForIntersection.size > 1) {\n-                val (mostSpecific, scopeForMostSpecific) = overrideService.selectMostSpecificMember(\n-                    baseMembersForIntersection,\n-                    ReturnTypeCalculatorForFullBodyResolve\n-                )\n-                val intersectionOverrideContext = ContextForIntersectionOverrideConstruction(\n-                    mostSpecific,\n-                    this,\n-                    extractedOverrides,\n-                    scopeForMostSpecific\n-                )\n-                result += ResultOfIntersection.NonTrivial(\n-                    intersectionOverrides,\n-                    intersectionOverrideContext,\n-                    extractedOverrides,\n-                    containingScope = null\n-                )\n+            val groupWithPrivate =\n+                overrideService.extractBothWaysOverridable(allMembersWithScope.maxByVisibility(), allMembersWithScope, overrideChecker)\n+            val group = groupWithPrivate.filter { !Visibilities.isPrivate(it.member.fir.visibility) }.ifEmpty { groupWithPrivate }\n+            val singleRealImplementation = group.size == 1 ||\n+                    group.mapTo(mutableSetOf()) { it.member.fir.unwrapSubstitutionOverrides().symbol }.size == 1\n+            val directOverrides = if (singleRealImplementation) group else group.onlyDirectlyInherited()",
        "comment_created_at": "2022-10-13T14:48:26+00:00",
        "comment_author": "dzharkov",
        "comment_body": "TBH I'm not sure here too, so I would move it without a clear reason",
        "pr_file_module": null
      },
      {
        "comment_id": "994798498",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4982,
        "pr_file": "compiler/fir/providers/src/org/jetbrains/kotlin/fir/scopes/impl/FirTypeIntersectionScopeContext.kt",
        "discussion_id": "994632200",
        "commented_code": "@@ -161,32 +156,21 @@ class FirTypeIntersectionScopeContext(\n         val result = mutableListOf<ResultOfIntersection<D>>()\n \n         while (allMembersWithScope.size > 1) {\n-            val maxByVisibility = findMemberWithMaxVisibility(allMembersWithScope)\n-            val extractBothWaysWithPrivate = overrideService.extractBothWaysOverridable(maxByVisibility, allMembersWithScope, overrideChecker)\n-            val extractedOverrides = extractBothWaysWithPrivate.filterNotTo(mutableListOf()) {\n-                Visibilities.isPrivate((it.member.fir as FirMemberDeclaration).visibility)\n-            }.takeIf { it.isNotEmpty() } ?: extractBothWaysWithPrivate\n-            val baseMembersForIntersection = extractedOverrides.calcBaseMembersForIntersectionOverride()\n-            if (baseMembersForIntersection.size > 1) {\n-                val (mostSpecific, scopeForMostSpecific) = overrideService.selectMostSpecificMember(\n-                    baseMembersForIntersection,\n-                    ReturnTypeCalculatorForFullBodyResolve\n-                )\n-                val intersectionOverrideContext = ContextForIntersectionOverrideConstruction(\n-                    mostSpecific,\n-                    this,\n-                    extractedOverrides,\n-                    scopeForMostSpecific\n-                )\n-                result += ResultOfIntersection.NonTrivial(\n-                    intersectionOverrides,\n-                    intersectionOverrideContext,\n-                    extractedOverrides,\n-                    containingScope = null\n-                )\n+            val groupWithPrivate =\n+                overrideService.extractBothWaysOverridable(allMembersWithScope.maxByVisibility(), allMembersWithScope, overrideChecker)\n+            val group = groupWithPrivate.filter { !Visibilities.isPrivate(it.member.fir.visibility) }.ifEmpty { groupWithPrivate }\n+            val singleRealImplementation = group.size == 1 ||\n+                    group.mapTo(mutableSetOf()) { it.member.fir.unwrapSubstitutionOverrides().symbol }.size == 1\n+            val directOverrides = if (singleRealImplementation) group else group.onlyDirectlyInherited()",
        "comment_created_at": "2022-10-13T15:26:17+00:00",
        "comment_author": "pyos",
        "comment_body": "done",
        "pr_file_module": null
      }
    ]
  }
]
