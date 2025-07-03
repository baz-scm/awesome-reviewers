---
title: Effective API samples
description: "Create clear, comprehensive, and properly structured code samples to\
  \ document API usage. Follow these principles:\n\n1. **Organize samples properly:**\n\
  \   - Place samples after doc blocks"
repository: JetBrains/kotlin
label: Documentation
language: Kotlin
comments_count: 8
repository_stars: 50857
---

Create clear, comprehensive, and properly structured code samples to document API usage. Follow these principles:

1. **Organize samples properly:**
   - Place samples after doc blocks
   - For specialized variants, include the main sample first, then add specialized versions:
   ```kotlin
   sample("samples.collections.Collections.Elements.find")
   specialFor(CharSequences) {
       sample("samples.text.Strings.find")
   }
   ```

2. **Create focused examples:**
   - Use separate samples for different overloads of the same function
   - Each sample should clearly demonstrate a specific API feature
   ```kotlin
   @Sample
   fun substring() { // Basic substring usage
       val str = "abcde"
       assertPrints(str.substring(0), "abcde")
       assertPrints(str.substring(1), "bcde")
   }
   
   @Sample
   fun substringWithRange() { // Overload with range
       val str = "abcde"
       assertPrints(str.substring(0, 3), "abc")
       assertPrints(str.substring(0, 0), "")
   }
   ```

3. **Include comprehensive examples:**
   - Demonstrate different parameter combinations
   - Show edge cases and common usage patterns
   - Add explanatory comments for assertions and edge cases
   ```kotlin
   @Sample
   fun lastIndexOf() {
       val inputString = "Never ever give up"
       val toFind = "ever"
       
       // Basic usage from start
       assertPrints(inputString.lastIndexOf(toFind), "6")
       // With specific start position
       assertPrints(inputString.lastIndexOf(toFind, 5), "6")
       // Start position after all occurrences
       assertFails { inputString.lastIndexOf(toFind, 10) } // No occurrence after position 10
   }
   ```

4. **Use standard formatting:**
   - Use `assertPrints()` which converts to readable documentation output
   ```kotlin
   // This:
   assertPrints(value, "stringRepresentation")
   // Converts to:
   println(value) // stringRepresentation
   ```

5. **Ensure samples are properly referenced:**
   - Add `@sample` tags to all relevant function variants, including expect/actual declarations
   - For generated code, update samples by running appropriate generation commands


[
  {
    "discussion_id": "1866663166",
    "pr_number": 5368,
    "pr_file": "libraries/tools/kotlin-stdlib-gen/src/templates/Elements.kt",
    "created_at": "2024-12-02T21:42:42+00:00",
    "commented_code": "} builder {\n        inline(Inline.Only)\n        doc { \"Returns the first ${f.element} matching the given [predicate], or `null` if no such ${f.element} was found.\" }\n        sample(\"samples.collections.Collections.Elements.find\")\n        specialFor(CharSequences) {\n            sample(\"samples.text.Strings.find\")\n        }\n        specialFor(ArraysOfUnsigned) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1866663166",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5368,
        "pr_file": "libraries/tools/kotlin-stdlib-gen/src/templates/Elements.kt",
        "discussion_id": "1866663166",
        "commented_code": "@@ -607,7 +607,12 @@ object Elements : TemplateGroupBase() {\n     } builder {\n         inline(Inline.Only)\n         doc { \"Returns the first ${f.element} matching the given [predicate], or `null` if no such ${f.element} was found.\" }\n-        sample(\"samples.collections.Collections.Elements.find\")\n+        specialFor(CharSequences) {\n+            sample(\"samples.text.Strings.find\")\n+        }\n+        specialFor(ArraysOfUnsigned) {",
        "comment_created_at": "2024-12-02T21:42:42+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "The original `sample` call should be left as is, without any additional `specialFor` predicates, and the call generating a sample specialized for char sequences should be placed right after it (wrapped into a predicate):\r\n```\r\nsample(\"samples.collections.Collections.Elements.find\")\r\nspecialFor(CharSequences) {\r\n    sample(\"samples.text.Strings.find\")\r\n}\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1870204716",
    "pr_number": 3977,
    "pr_file": "libraries/stdlib/jvm/src/kotlin/text/StringsJVM.kt",
    "created_at": "2024-12-04T19:59:04+00:00",
    "commented_code": "* If [ignoreCase] is true, the result of `Char.uppercaseChar().lowercaseChar()` on each character is compared.\n *\n * @param ignoreCase `true` to ignore character case when comparing strings. By default `false`.\n * @sample samples.text.Strings.equals",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1870204716",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/jvm/src/kotlin/text/StringsJVM.kt",
        "discussion_id": "1870204716",
        "commented_code": "@@ -48,6 +48,7 @@ internal actual inline fun String.nativeLastIndexOf(str: String, fromIndex: Int)\n  * If [ignoreCase] is true, the result of `Char.uppercaseChar().lowercaseChar()` on each character is compared.\n  *\n  * @param ignoreCase `true` to ignore character case when comparing strings. By default `false`.\n+ * @sample samples.text.Strings.equals",
        "comment_created_at": "2024-12-04T19:59:04+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "For all the actual declarations, samples need to be added to the corresponding expect declaration and all other actualizations.\r\n\r\nCheck `CharSequence?.contentEquals` as an example. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1870237260",
    "pr_number": 3977,
    "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
    "created_at": "2024-12-04T20:26:49+00:00",
    "commented_code": "assertPrints(mixedColor, \"brown&blue\")\n    }\n\n    @Sample\n    fun toPattern() {\n        val string = \"this is a regex\"\n        val pattern = string.toPattern(1)\n        assertPrints(pattern.pattern(), string)\n        assertTrue(pattern.flags() == 1)\n    }\n\n    @Sample\n    fun encodeToByteArray() {\n        val str = \"Hello\"\n        val byteArray = str.encodeToByteArray()\n        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n\n        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1870237260",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1870237260",
        "commented_code": "@@ -508,6 +508,104 @@ class Strings {\n         assertPrints(mixedColor, \"brown&blue\")\n     }\n \n+    @Sample\n+    fun toPattern() {\n+        val string = \"this is a regex\"\n+        val pattern = string.toPattern(1)\n+        assertPrints(pattern.pattern(), string)\n+        assertTrue(pattern.flags() == 1)\n+    }\n+\n+    @Sample\n+    fun encodeToByteArray() {\n+        val str = \"Hello\"\n+        val byteArray = str.encodeToByteArray()\n+        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n+        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n+\n+        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)",
        "comment_created_at": "2024-12-04T20:26:49+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "The sample is used for the different overload.",
        "pr_file_module": null
      },
      {
        "comment_id": "1883936376",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1870237260",
        "commented_code": "@@ -508,6 +508,104 @@ class Strings {\n         assertPrints(mixedColor, \"brown&blue\")\n     }\n \n+    @Sample\n+    fun toPattern() {\n+        val string = \"this is a regex\"\n+        val pattern = string.toPattern(1)\n+        assertPrints(pattern.pattern(), string)\n+        assertTrue(pattern.flags() == 1)\n+    }\n+\n+    @Sample\n+    fun encodeToByteArray() {\n+        val str = \"Hello\"\n+        val byteArray = str.encodeToByteArray()\n+        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n+        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n+\n+        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)",
        "comment_created_at": "2024-12-13T13:27:15+00:00",
        "comment_author": "CharlesLgn",
        "comment_body": "I do not understant what you are asking here \ud83d\ude15",
        "pr_file_module": null
      },
      {
        "comment_id": "1883961726",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1870237260",
        "commented_code": "@@ -508,6 +508,104 @@ class Strings {\n         assertPrints(mixedColor, \"brown&blue\")\n     }\n \n+    @Sample\n+    fun toPattern() {\n+        val string = \"this is a regex\"\n+        val pattern = string.toPattern(1)\n+        assertPrints(pattern.pattern(), string)\n+        assertTrue(pattern.flags() == 1)\n+    }\n+\n+    @Sample\n+    fun encodeToByteArray() {\n+        val str = \"Hello\"\n+        val byteArray = str.encodeToByteArray()\n+        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n+        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n+\n+        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)",
        "comment_created_at": "2024-12-13T13:47:00+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "Sorry for the obscure comment. There are two `String.encodeToByteArray` overloads: one that does not accepts any parameters, and the one that does.\r\nThe sample showcases both these overloads, but the `@sample` tag referring the sample was placed only on one of those overloads.\r\n\r\nSo either the sample should not use the second overload, or the tag should be placed in KDoc for both of these functions.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1870241917",
    "pr_number": 3977,
    "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
    "created_at": "2024-12-04T20:30:36+00:00",
    "commented_code": "assertPrints(mixedColor, \"brown&blue\")\n    }\n\n    @Sample\n    fun toPattern() {\n        val string = \"this is a regex\"\n        val pattern = string.toPattern(1)\n        assertPrints(pattern.pattern(), string)\n        assertTrue(pattern.flags() == 1)\n    }\n\n    @Sample\n    fun encodeToByteArray() {\n        val str = \"Hello\"\n        val byteArray = str.encodeToByteArray()\n        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n\n        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)\n        assertPrints(byteArrayWithoutFirstLetter.contentToString(), \"[101, 108, 108, 111]\")\n        assertPrints(byteArrayWithoutFirstLetter.toString(Charsets.UTF_8), \"ello\")\n\n        val byteArrayWithoutLastLetter = str.encodeToByteArray(startIndex = 0, endIndex = str.length - 1)\n        assertPrints(byteArrayWithoutLastLetter.contentToString(), \"[72, 101, 108, 108]\")\n        assertPrints(byteArrayWithoutLastLetter.toString(Charsets.UTF_8), \"Hell\")\n    }\n\n    @Sample\n    fun subString() {\n        val str = \"abcde\"\n        assertPrints(str.substring(0), \"abcde\")\n        assertPrints(str.substring(1), \"bcde\")\n        assertFails { str.substring(6) }",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1870241917",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1870241917",
        "commented_code": "@@ -508,6 +508,104 @@ class Strings {\n         assertPrints(mixedColor, \"brown&blue\")\n     }\n \n+    @Sample\n+    fun toPattern() {\n+        val string = \"this is a regex\"\n+        val pattern = string.toPattern(1)\n+        assertPrints(pattern.pattern(), string)\n+        assertTrue(pattern.flags() == 1)\n+    }\n+\n+    @Sample\n+    fun encodeToByteArray() {\n+        val str = \"Hello\"\n+        val byteArray = str.encodeToByteArray()\n+        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n+        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n+\n+        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)\n+        assertPrints(byteArrayWithoutFirstLetter.contentToString(), \"[101, 108, 108, 111]\")\n+        assertPrints(byteArrayWithoutFirstLetter.toString(Charsets.UTF_8), \"ello\")\n+\n+        val byteArrayWithoutLastLetter = str.encodeToByteArray(startIndex = 0, endIndex = str.length - 1)\n+        assertPrints(byteArrayWithoutLastLetter.contentToString(), \"[72, 101, 108, 108]\")\n+        assertPrints(byteArrayWithoutLastLetter.toString(Charsets.UTF_8), \"Hell\")\n+    }\n+\n+    @Sample\n+    fun subString() {\n+        val str = \"abcde\"\n+        assertPrints(str.substring(0), \"abcde\")\n+        assertPrints(str.substring(1), \"bcde\")\n+        assertFails { str.substring(6) }",
        "comment_created_at": "2024-12-04T20:30:36+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "For all `assertFails` it is better to add a comment describing the reason of the failure. Here, for example, it could be `// index exceeds string length`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1870244939",
    "pr_number": 3977,
    "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
    "created_at": "2024-12-04T20:33:48+00:00",
    "commented_code": "assertPrints(mixedColor, \"brown&blue\")\n    }\n\n    @Sample\n    fun toPattern() {\n        val string = \"this is a regex\"\n        val pattern = string.toPattern(1)\n        assertPrints(pattern.pattern(), string)\n        assertTrue(pattern.flags() == 1)\n    }\n\n    @Sample\n    fun encodeToByteArray() {\n        val str = \"Hello\"\n        val byteArray = str.encodeToByteArray()\n        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n\n        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)\n        assertPrints(byteArrayWithoutFirstLetter.contentToString(), \"[101, 108, 108, 111]\")\n        assertPrints(byteArrayWithoutFirstLetter.toString(Charsets.UTF_8), \"ello\")\n\n        val byteArrayWithoutLastLetter = str.encodeToByteArray(startIndex = 0, endIndex = str.length - 1)\n        assertPrints(byteArrayWithoutLastLetter.contentToString(), \"[72, 101, 108, 108]\")\n        assertPrints(byteArrayWithoutLastLetter.toString(Charsets.UTF_8), \"Hell\")\n    }\n\n    @Sample\n    fun subString() {\n        val str = \"abcde\"\n        assertPrints(str.substring(0), \"abcde\")\n        assertPrints(str.substring(1), \"bcde\")\n        assertFails { str.substring(6) }\n        assertPrints(str.substring(0, 0), \"\")",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1870244939",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3977,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1870244939",
        "commented_code": "@@ -508,6 +508,104 @@ class Strings {\n         assertPrints(mixedColor, \"brown&blue\")\n     }\n \n+    @Sample\n+    fun toPattern() {\n+        val string = \"this is a regex\"\n+        val pattern = string.toPattern(1)\n+        assertPrints(pattern.pattern(), string)\n+        assertTrue(pattern.flags() == 1)\n+    }\n+\n+    @Sample\n+    fun encodeToByteArray() {\n+        val str = \"Hello\"\n+        val byteArray = str.encodeToByteArray()\n+        assertPrints(byteArray.contentToString(), \"[72, 101, 108, 108, 111]\")\n+        assertPrints(byteArray.toString(Charsets.UTF_8), str)\n+\n+        val byteArrayWithoutFirstLetter = str.encodeToByteArray(startIndex = 1, endIndex = str.length)\n+        assertPrints(byteArrayWithoutFirstLetter.contentToString(), \"[101, 108, 108, 111]\")\n+        assertPrints(byteArrayWithoutFirstLetter.toString(Charsets.UTF_8), \"ello\")\n+\n+        val byteArrayWithoutLastLetter = str.encodeToByteArray(startIndex = 0, endIndex = str.length - 1)\n+        assertPrints(byteArrayWithoutLastLetter.contentToString(), \"[72, 101, 108, 108]\")\n+        assertPrints(byteArrayWithoutLastLetter.toString(Charsets.UTF_8), \"Hell\")\n+    }\n+\n+    @Sample\n+    fun subString() {\n+        val str = \"abcde\"\n+        assertPrints(str.substring(0), \"abcde\")\n+        assertPrints(str.substring(1), \"bcde\")\n+        assertFails { str.substring(6) }\n+        assertPrints(str.substring(0, 0), \"\")",
        "comment_created_at": "2024-12-04T20:33:48+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "There are quite a few examples here, so it's better to split the function in two and provide samples dedicated to each particular `substring` overload.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1987938136",
    "pr_number": 5411,
    "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
    "created_at": "2025-03-10T19:59:51+00:00",
    "commented_code": "assertPrints(matchDetails(inputString, toFind, 10), \"Searching for 'ever' in 'Never ever give up' starting at position 10: Not found\")\n    }\n\n    @Sample\n    fun lastIndexOf() {\n        fun matchDetails(inputString: String, whatToFind: String, startIndex: Int = 0): String {\n            val matchIndex = inputString.lastIndexOf(whatToFind, startIndex)\n            return \"Searching for '$whatToFind' in '$inputString' starting at position $startIndex: \" +\n                    if (matchIndex >= 0) \"Found at $matchIndex\" else \"Not found\"\n        }\n\n        val inputString = \"Never ever give up\"\n        val toFind = \"ever\"\n\n        assertPrints(matchDetails(inputString, toFind), \"Searching for 'ever' in 'Never ever give up' starting at position 0: Found at 6\")\n        assertPrints(matchDetails(inputString, toFind, 10), \"Searching for 'ever' in 'Never ever give up' starting at position 10: Not found\")\n    }",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1987938136",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5411,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "1987938136",
        "commented_code": "@@ -444,6 +444,33 @@ class Strings {\n         assertPrints(matchDetails(inputString, toFind, 10), \"Searching for 'ever' in 'Never ever give up' starting at position 10: Not found\")\n     }\n \n+    @Sample\n+    fun lastIndexOf() {\n+        fun matchDetails(inputString: String, whatToFind: String, startIndex: Int = 0): String {\n+            val matchIndex = inputString.lastIndexOf(whatToFind, startIndex)\n+            return \"Searching for '$whatToFind' in '$inputString' starting at position $startIndex: \" +\n+                    if (matchIndex >= 0) \"Found at $matchIndex\" else \"Not found\"\n+        }\n+\n+        val inputString = \"Never ever give up\"\n+        val toFind = \"ever\"\n+\n+        assertPrints(matchDetails(inputString, toFind), \"Searching for 'ever' in 'Never ever give up' starting at position 0: Found at 6\")\n+        assertPrints(matchDetails(inputString, toFind, 10), \"Searching for 'ever' in 'Never ever give up' starting at position 10: Not found\")\n+    }",
        "comment_created_at": "2025-03-10T19:59:51+00:00",
        "comment_author": "fzhinkin",
        "comment_body": "Could you please also add an example with `startPosition = 5`?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "764231663",
    "pr_number": 4565,
    "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
    "created_at": "2021-12-07T17:48:04+00:00",
    "commented_code": "assertPrints(mixedColor, \"brown&blue\")\n    }\n\n    @Sample\n    fun all() {\n        val name = \"fatima\"\n        val containsWhiteSpace: Boolean = name.any{\n            it.isWhitespace()\n        }\n        assertFalse(containsWhiteSpace)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "764231663",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4565,
        "pr_file": "libraries/stdlib/samples/test/samples/text/strings.kt",
        "discussion_id": "764231663",
        "commented_code": "@@ -507,4 +507,29 @@ class Strings {\n \n         assertPrints(mixedColor, \"brown&blue\")\n     }\n+\n+    @Sample\n+    fun all() {\n+        val name = \"fatima\"\n+        val containsWhiteSpace: Boolean = name.any{\n+            it.isWhitespace()\n+        }\n+        assertFalse(containsWhiteSpace)",
        "comment_created_at": "2021-12-07T17:48:04+00:00",
        "comment_author": "qurbonzoda",
        "comment_body": "In samples we use `assertPrints(value, stringRepresentation)` which is converted to \r\n```\r\nprintln(value) // stringRepresentation\r\n```\r\nin Kotlin website. E.g. the `splitToSequence` sample above is converted to this runnable code in docs website: https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.text/split-to-sequence.html",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1299179286",
    "pr_number": 5169,
    "pr_file": "libraries/tools/kotlin-stdlib-gen/src/templates/Ranges.kt",
    "created_at": "2023-08-19T12:13:11+00:00",
    "commented_code": "return TProgression.fromClosedRange(first, last, if (this.step > 0) step else -step)\n            \"\"\"\n        }\n        sample(\"samples.ranges.Ranges.step${primitive!!.stepType}\")",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1299179286",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5169,
        "pr_file": "libraries/tools/kotlin-stdlib-gen/src/templates/Ranges.kt",
        "discussion_id": "1299179286",
        "commented_code": "@@ -76,6 +76,7 @@ object RangeOps : TemplateGroupBase() {\n             return TProgression.fromClosedRange(first, last, if (this.step > 0) step else -step)\n             \"\"\"\n         }\n+        sample(\"samples.ranges.Ranges.step${primitive!!.stepType}\")",
        "comment_created_at": "2023-08-19T12:13:11+00:00",
        "comment_author": "ilya-g",
        "comment_body": "Minor: please place it after `doc { }` block, because a sample is a part of function documentation. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1304693658",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5169,
        "pr_file": "libraries/tools/kotlin-stdlib-gen/src/templates/Ranges.kt",
        "discussion_id": "1299179286",
        "commented_code": "@@ -76,6 +76,7 @@ object RangeOps : TemplateGroupBase() {\n             return TProgression.fromClosedRange(first, last, if (this.step > 0) step else -step)\n             \"\"\"\n         }\n+        sample(\"samples.ranges.Ranges.step${primitive!!.stepType}\")",
        "comment_created_at": "2023-08-24T18:07:19+00:00",
        "comment_author": "AlexCue987",
        "comment_body": "fixed",
        "pr_file_module": null
      }
    ]
  }
]
