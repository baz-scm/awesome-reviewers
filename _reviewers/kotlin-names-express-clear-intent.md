---
title: Names express clear intent
description: Choose names that clearly express intent and follow established conventions.
  Prefer explicit, descriptive names over abbreviations or ambiguous terms. Align
  with platform-specific naming patterns and maintain consistency with existing codebase
  conventions.
repository: JetBrains/kotlin
label: Naming Conventions
language: Kotlin
comments_count: 11
repository_stars: 50857
---

Choose names that clearly express intent and follow established conventions. Prefer explicit, descriptive names over abbreviations or ambiguous terms. Align with platform-specific naming patterns and maintain consistency with existing codebase conventions.

Key guidelines:
- Use full descriptive names instead of abbreviations (e.g., `BREADTH_FIRST` over `BFS`)
- Follow platform naming conventions (e.g., `reifiedTypeParameters` for properties, `getReifiedTypeParameters()` for functions in Kotlin)
- Choose names that accurately reflect the variable's purpose (e.g., `argumentType` instead of `typeArgument`)
- Avoid terms that conflict with language keywords or have special meaning (e.g., use `child` instead of `inner`)
- Maintain consistency with similar names in the codebase

Example:
```kotlin
// Incorrect
enum class WalkAlgorithm {
    BFS,  // Abbreviated
    DFS   // Abbreviated
}

// Correct
enum class WalkAlgorithm {
    BREADTH_FIRST,  // Explicit
    DEPTH_FIRST    // Explicit
}
```


[
  {
    "discussion_id": "270310587",
    "pr_number": 2232,
    "pr_file": "libraries/stdlib/jvm/src/kotlin/io/files/FileTreeWalk.kt",
    "created_at": "2019-03-29T08:09:17+00:00",
    "commented_code": "import java.io.IOException\nimport java.util.ArrayDeque\n\n/**\n * An enumeration to describe possible algorithms to traverse.\n * There are two of them: search in breadth (same directory depth)\n */\npublic enum class WalkAlgorithm {\n    /**\n     * Breadth-first search\n     */\n    BFS,",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "270310587",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 2232,
        "pr_file": "libraries/stdlib/jvm/src/kotlin/io/files/FileTreeWalk.kt",
        "discussion_id": "270310587",
        "commented_code": "@@ -12,6 +12,20 @@ import java.io.File\n import java.io.IOException\n import java.util.ArrayDeque\n \n+/**\n+ * An enumeration to describe possible algorithms to traverse.\n+ * There are two of them: search in breadth (same directory depth)\n+ */\n+public enum class WalkAlgorithm {\n+    /**\n+     * Breadth-first search\n+     */\n+    BFS,",
        "comment_created_at": "2019-03-29T08:09:17+00:00",
        "comment_author": "sschuberth",
        "comment_body": "I actually believe we should write these out as `BREADTH_FIRST` and `DEPTH_FIRST`, just like we have `TOP_DOWN` instead of `TD` below.",
        "pr_file_module": null
      },
      {
        "comment_id": "272912852",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 2232,
        "pr_file": "libraries/stdlib/jvm/src/kotlin/io/files/FileTreeWalk.kt",
        "discussion_id": "270310587",
        "commented_code": "@@ -12,6 +12,20 @@ import java.io.File\n import java.io.IOException\n import java.util.ArrayDeque\n \n+/**\n+ * An enumeration to describe possible algorithms to traverse.\n+ * There are two of them: search in breadth (same directory depth)\n+ */\n+public enum class WalkAlgorithm {\n+    /**\n+     * Breadth-first search\n+     */\n+    BFS,",
        "comment_created_at": "2019-04-08T07:24:14+00:00",
        "comment_author": "aivinog1",
        "comment_body": "Agree.",
        "pr_file_module": null
      },
      {
        "comment_id": "272967895",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 2232,
        "pr_file": "libraries/stdlib/jvm/src/kotlin/io/files/FileTreeWalk.kt",
        "discussion_id": "270310587",
        "commented_code": "@@ -12,6 +12,20 @@ import java.io.File\n import java.io.IOException\n import java.util.ArrayDeque\n \n+/**\n+ * An enumeration to describe possible algorithms to traverse.\n+ * There are two of them: search in breadth (same directory depth)\n+ */\n+public enum class WalkAlgorithm {\n+    /**\n+     * Breadth-first search\n+     */\n+    BFS,",
        "comment_created_at": "2019-04-08T09:55:30+00:00",
        "comment_author": "aivinog1",
        "comment_body": "> I actually believe we should write these out as `BREADTH_FIRST` and `DEPTH_FIRST`, just like we have `TOP_DOWN` instead of `TD` below.\r\n\r\nDone.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "936958162",
    "pr_number": 4903,
    "pr_file": "compiler/ir/backend.jvm/src/org/jetbrains/kotlin/backend/jvm/MemoizedInlineClassReplacements.kt",
    "created_at": "2022-08-03T17:28:39+00:00",
    "commented_code": "parent = irClass\n                // We ignore type arguments here, since there is no good way to go from type arguments to types in the IR anyway.\n                val typeArgument =",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "936958162",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4903,
        "pr_file": "compiler/ir/backend.jvm/src/org/jetbrains/kotlin/backend/jvm/MemoizedInlineClassReplacements.kt",
        "discussion_id": "936958162",
        "commented_code": "@@ -155,7 +165,10 @@ class MemoizedInlineClassReplacements(\n                 parent = irClass\n                 // We ignore type arguments here, since there is no good way to go from type arguments to types in the IR anyway.\n                 val typeArgument =",
        "comment_created_at": "2022-08-03T17:28:39+00:00",
        "comment_author": "sfs",
        "comment_body": "Since you're touching this code anyway, could you please rename this variable to `argumentType`? It's really not a type argument...",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "451431218",
    "pr_number": 3516,
    "pr_file": "libraries/scripting/type-providers/src/kotlin/script/experimental/typeProviders/generatedCode/GeneratedCode.kt",
    "created_at": "2020-07-08T10:07:36+00:00",
    "commented_code": "/*\n * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n */\n\npackage kotlin.script.experimental.typeProviders.generatedCode\n\nimport kotlin.reflect.KClass\nimport kotlin.script.experimental.typeProviders.generatedCode.impl.*\nimport kotlin.script.experimental.typeProviders.generatedCode.impl.Object\nimport kotlin.script.experimental.typeProviders.generatedCode.impl.writeJoined\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.Generated\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.GeneratedCodeVisitor\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.InternalGeneratedCode\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.visit\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.captureImports\nimport kotlin.script.experimental.typeProviders.generatedCode.internal.write\nimport kotlin.text.StringBuilder\n\n/**\n * Code returned by a Type Provider.\n * [GeneratedCode] is a recursive construction that allows you to build generated code as a combination of multiple types already provided\n *\n * Example:\n *\n * ```kotlin\n * data class MyObject(val name: String, val value: Int) : GeneratedCode {\n *     fun body(): GeneratedCode {\n *          return GeneratedCode.composite {\n *              +makeDataClass(name)\n *                  .withInterface(MyInterface::class)\n *\n *              +makeConstant(\"$nameConstant\", value)\n *          }\n *     }\n * }\n * ```\n *\n * [GeneratedCode] can contain any of the following:\n * - Data classes. See [makeDataClass].\n * - Objects. See [makeObject].\n * - Constants. See [makeConstant].\n * - Packages. See [makePackage].\n * - Extension functions. See [makeExtensionMethod].\n * - etc.\n */\ninterface GeneratedCode {\n    /**\n     * Generate the code that corresponds to your type\n     *\n     * @return An instance of [GeneratedCode].\n     * Important: don't return an infinite recursion in the form of return `this`\n     */\n    fun body(): GeneratedCode\n\n    /**\n     * A builder for a composite of multiple types\n     */\n    class Builder internal constructor() {\n        private val mutableCodeList = mutableListOf<GeneratedCode>()\n\n        /**\n         * Include code in your compound\n         */\n        operator fun GeneratedCode.unaryPlus() {\n            if (this is CompoundGeneratedCode) {\n                mutableCodeList.addAll(codeList)\n            } else {\n                mutableCodeList.add(this)\n            }\n        }\n\n        operator fun String.unaryPlus() {\n            mutableCodeList.add(inlineCode(this))\n        }\n\n        internal fun build(): GeneratedCode {\n            return composite(mutableCodeList)\n        }\n    }\n\n    object Empty : GeneratedCode by EmptyCode()\n\n    companion object {\n        /**\n         * Create a composition of multiple instances of Generated Code\n         */\n        fun composite(init: Builder.() -> Unit) = Builder().apply(init).build()\n\n        /**\n         * Create a composition of multiple instances of Generated Code\n         */\n        fun composite(iterable: Collection<GeneratedCode>): GeneratedCode = if (iterable.count() == 1)\n            iterable.first()\n        else\n            CompoundGeneratedCode(iterable.toList())\n\n        /**\n         * Create a composition of multiple instances of Generated Code\n         */\n        fun composite(vararg code: GeneratedCode) = composite(code.toList())\n    }\n}\n\nprivate data class CompoundGeneratedCode(val codeList: List<GeneratedCode>) : InternalGeneratedCode() {\n    override fun StringBuilder.write(indent: Int) {\n        writeJoined(codeList, \"\\n\\n\", indent)\n    }\n\n    override fun GeneratedCodeVisitor.visit() {\n        for (code in codeList) {\n            visit(code)\n        }\n    }\n}\n\n/**\n * References a member that can be used as a type\n */\ninterface IdentifiableMember {\n    val name: String\n    fun imports(): Set<String> = emptySet()\n\n    companion object {\n        private data class KClassIdentifiable(val kClass: KClass<*>) : IdentifiableMember {\n            override val name: String = kClass.simpleName ?: kClass.qualifiedName!!\n            override fun imports() = setOfNotNull(kClass.qualifiedName)\n        }\n\n        private data class NamedIdentifiable(override val name: String) : IdentifiableMember\n\n        operator fun invoke(kClass: KClass<*>): IdentifiableMember = KClassIdentifiable(kClass)\n        operator fun invoke(name: String): IdentifiableMember = NamedIdentifiable(name)\n    }\n}\n\n/**\n * References an interface that can be implemented\n */\ninterface GeneratedInterface : IdentifiableMember\n\nprivate data class CastedInterfaceMember(private val member: IdentifiableMember) : GeneratedInterface, IdentifiableMember by member\n\nfun IdentifiableMember.asInterface(): GeneratedInterface = CastedInterfaceMember(this)\n\n/**\n * Generated code that is a type that can be used as an Argument\n */\ninterface IdentifiableCode : GeneratedCode, IdentifiableMember\n\n/**\n * Builder for a provided type whose JVM Name can be set\n */\ninterface JVMNameableBuilder {\n    fun jvmName(name: String)\n}\n\n/**\n * Builder for a provided type. It can implement an interface and have some code inside.\n */\ninterface GeneratedTypeBuilder : IdentifiableMember {\n    /**\n     * Implement a generated interface\n     */\n    fun implement(generated: GeneratedInterface)\n\n    /**\n     * Add code to the namespace of the Type\n     */\n    fun inner(code: GeneratedCode)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "451431218",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3516,
        "pr_file": "libraries/scripting/type-providers/src/kotlin/script/experimental/typeProviders/generatedCode/GeneratedCode.kt",
        "discussion_id": "451431218",
        "commented_code": "@@ -0,0 +1,302 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package kotlin.script.experimental.typeProviders.generatedCode\n+\n+import kotlin.reflect.KClass\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.*\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.Object\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.writeJoined\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.Generated\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.GeneratedCodeVisitor\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.InternalGeneratedCode\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visit\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.captureImports\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.write\n+import kotlin.text.StringBuilder\n+\n+/**\n+ * Code returned by a Type Provider.\n+ * [GeneratedCode] is a recursive construction that allows you to build generated code as a combination of multiple types already provided\n+ *\n+ * Example:\n+ *\n+ * ```kotlin\n+ * data class MyObject(val name: String, val value: Int) : GeneratedCode {\n+ *     fun body(): GeneratedCode {\n+ *          return GeneratedCode.composite {\n+ *              +makeDataClass(name)\n+ *                  .withInterface(MyInterface::class)\n+ *\n+ *              +makeConstant(\"$nameConstant\", value)\n+ *          }\n+ *     }\n+ * }\n+ * ```\n+ *\n+ * [GeneratedCode] can contain any of the following:\n+ * - Data classes. See [makeDataClass].\n+ * - Objects. See [makeObject].\n+ * - Constants. See [makeConstant].\n+ * - Packages. See [makePackage].\n+ * - Extension functions. See [makeExtensionMethod].\n+ * - etc.\n+ */\n+interface GeneratedCode {\n+    /**\n+     * Generate the code that corresponds to your type\n+     *\n+     * @return An instance of [GeneratedCode].\n+     * Important: don't return an infinite recursion in the form of return `this`\n+     */\n+    fun body(): GeneratedCode\n+\n+    /**\n+     * A builder for a composite of multiple types\n+     */\n+    class Builder internal constructor() {\n+        private val mutableCodeList = mutableListOf<GeneratedCode>()\n+\n+        /**\n+         * Include code in your compound\n+         */\n+        operator fun GeneratedCode.unaryPlus() {\n+            if (this is CompoundGeneratedCode) {\n+                mutableCodeList.addAll(codeList)\n+            } else {\n+                mutableCodeList.add(this)\n+            }\n+        }\n+\n+        operator fun String.unaryPlus() {\n+            mutableCodeList.add(inlineCode(this))\n+        }\n+\n+        internal fun build(): GeneratedCode {\n+            return composite(mutableCodeList)\n+        }\n+    }\n+\n+    object Empty : GeneratedCode by EmptyCode()\n+\n+    companion object {\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(init: Builder.() -> Unit) = Builder().apply(init).build()\n+\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(iterable: Collection<GeneratedCode>): GeneratedCode = if (iterable.count() == 1)\n+            iterable.first()\n+        else\n+            CompoundGeneratedCode(iterable.toList())\n+\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(vararg code: GeneratedCode) = composite(code.toList())\n+    }\n+}\n+\n+private data class CompoundGeneratedCode(val codeList: List<GeneratedCode>) : InternalGeneratedCode() {\n+    override fun StringBuilder.write(indent: Int) {\n+        writeJoined(codeList, \"\\n\\n\", indent)\n+    }\n+\n+    override fun GeneratedCodeVisitor.visit() {\n+        for (code in codeList) {\n+            visit(code)\n+        }\n+    }\n+}\n+\n+/**\n+ * References a member that can be used as a type\n+ */\n+interface IdentifiableMember {\n+    val name: String\n+    fun imports(): Set<String> = emptySet()\n+\n+    companion object {\n+        private data class KClassIdentifiable(val kClass: KClass<*>) : IdentifiableMember {\n+            override val name: String = kClass.simpleName ?: kClass.qualifiedName!!\n+            override fun imports() = setOfNotNull(kClass.qualifiedName)\n+        }\n+\n+        private data class NamedIdentifiable(override val name: String) : IdentifiableMember\n+\n+        operator fun invoke(kClass: KClass<*>): IdentifiableMember = KClassIdentifiable(kClass)\n+        operator fun invoke(name: String): IdentifiableMember = NamedIdentifiable(name)\n+    }\n+}\n+\n+/**\n+ * References an interface that can be implemented\n+ */\n+interface GeneratedInterface : IdentifiableMember\n+\n+private data class CastedInterfaceMember(private val member: IdentifiableMember) : GeneratedInterface, IdentifiableMember by member\n+\n+fun IdentifiableMember.asInterface(): GeneratedInterface = CastedInterfaceMember(this)\n+\n+/**\n+ * Generated code that is a type that can be used as an Argument\n+ */\n+interface IdentifiableCode : GeneratedCode, IdentifiableMember\n+\n+/**\n+ * Builder for a provided type whose JVM Name can be set\n+ */\n+interface JVMNameableBuilder {\n+    fun jvmName(name: String)\n+}\n+\n+/**\n+ * Builder for a provided type. It can implement an interface and have some code inside.\n+ */\n+interface GeneratedTypeBuilder : IdentifiableMember {\n+    /**\n+     * Implement a generated interface\n+     */\n+    fun implement(generated: GeneratedInterface)\n+\n+    /**\n+     * Add code to the namespace of the Type\n+     */\n+    fun inner(code: GeneratedCode)",
        "comment_created_at": "2020-07-08T10:07:36+00:00",
        "comment_author": "ligee",
        "comment_body": "I think this is a confusing name, the word `inner` has a different meaning in the Kotlin code.\r\nIn the compiler, we're using `child`/`children`  in such places.",
        "pr_file_module": null
      },
      {
        "comment_id": "480104468",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3516,
        "pr_file": "libraries/scripting/type-providers/src/kotlin/script/experimental/typeProviders/generatedCode/GeneratedCode.kt",
        "discussion_id": "451431218",
        "commented_code": "@@ -0,0 +1,302 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package kotlin.script.experimental.typeProviders.generatedCode\n+\n+import kotlin.reflect.KClass\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.*\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.Object\n+import kotlin.script.experimental.typeProviders.generatedCode.impl.writeJoined\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.Generated\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.GeneratedCodeVisitor\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.InternalGeneratedCode\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visit\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.visitor.captureImports\n+import kotlin.script.experimental.typeProviders.generatedCode.internal.write\n+import kotlin.text.StringBuilder\n+\n+/**\n+ * Code returned by a Type Provider.\n+ * [GeneratedCode] is a recursive construction that allows you to build generated code as a combination of multiple types already provided\n+ *\n+ * Example:\n+ *\n+ * ```kotlin\n+ * data class MyObject(val name: String, val value: Int) : GeneratedCode {\n+ *     fun body(): GeneratedCode {\n+ *          return GeneratedCode.composite {\n+ *              +makeDataClass(name)\n+ *                  .withInterface(MyInterface::class)\n+ *\n+ *              +makeConstant(\"$nameConstant\", value)\n+ *          }\n+ *     }\n+ * }\n+ * ```\n+ *\n+ * [GeneratedCode] can contain any of the following:\n+ * - Data classes. See [makeDataClass].\n+ * - Objects. See [makeObject].\n+ * - Constants. See [makeConstant].\n+ * - Packages. See [makePackage].\n+ * - Extension functions. See [makeExtensionMethod].\n+ * - etc.\n+ */\n+interface GeneratedCode {\n+    /**\n+     * Generate the code that corresponds to your type\n+     *\n+     * @return An instance of [GeneratedCode].\n+     * Important: don't return an infinite recursion in the form of return `this`\n+     */\n+    fun body(): GeneratedCode\n+\n+    /**\n+     * A builder for a composite of multiple types\n+     */\n+    class Builder internal constructor() {\n+        private val mutableCodeList = mutableListOf<GeneratedCode>()\n+\n+        /**\n+         * Include code in your compound\n+         */\n+        operator fun GeneratedCode.unaryPlus() {\n+            if (this is CompoundGeneratedCode) {\n+                mutableCodeList.addAll(codeList)\n+            } else {\n+                mutableCodeList.add(this)\n+            }\n+        }\n+\n+        operator fun String.unaryPlus() {\n+            mutableCodeList.add(inlineCode(this))\n+        }\n+\n+        internal fun build(): GeneratedCode {\n+            return composite(mutableCodeList)\n+        }\n+    }\n+\n+    object Empty : GeneratedCode by EmptyCode()\n+\n+    companion object {\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(init: Builder.() -> Unit) = Builder().apply(init).build()\n+\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(iterable: Collection<GeneratedCode>): GeneratedCode = if (iterable.count() == 1)\n+            iterable.first()\n+        else\n+            CompoundGeneratedCode(iterable.toList())\n+\n+        /**\n+         * Create a composition of multiple instances of Generated Code\n+         */\n+        fun composite(vararg code: GeneratedCode) = composite(code.toList())\n+    }\n+}\n+\n+private data class CompoundGeneratedCode(val codeList: List<GeneratedCode>) : InternalGeneratedCode() {\n+    override fun StringBuilder.write(indent: Int) {\n+        writeJoined(codeList, \"\\n\\n\", indent)\n+    }\n+\n+    override fun GeneratedCodeVisitor.visit() {\n+        for (code in codeList) {\n+            visit(code)\n+        }\n+    }\n+}\n+\n+/**\n+ * References a member that can be used as a type\n+ */\n+interface IdentifiableMember {\n+    val name: String\n+    fun imports(): Set<String> = emptySet()\n+\n+    companion object {\n+        private data class KClassIdentifiable(val kClass: KClass<*>) : IdentifiableMember {\n+            override val name: String = kClass.simpleName ?: kClass.qualifiedName!!\n+            override fun imports() = setOfNotNull(kClass.qualifiedName)\n+        }\n+\n+        private data class NamedIdentifiable(override val name: String) : IdentifiableMember\n+\n+        operator fun invoke(kClass: KClass<*>): IdentifiableMember = KClassIdentifiable(kClass)\n+        operator fun invoke(name: String): IdentifiableMember = NamedIdentifiable(name)\n+    }\n+}\n+\n+/**\n+ * References an interface that can be implemented\n+ */\n+interface GeneratedInterface : IdentifiableMember\n+\n+private data class CastedInterfaceMember(private val member: IdentifiableMember) : GeneratedInterface, IdentifiableMember by member\n+\n+fun IdentifiableMember.asInterface(): GeneratedInterface = CastedInterfaceMember(this)\n+\n+/**\n+ * Generated code that is a type that can be used as an Argument\n+ */\n+interface IdentifiableCode : GeneratedCode, IdentifiableMember\n+\n+/**\n+ * Builder for a provided type whose JVM Name can be set\n+ */\n+interface JVMNameableBuilder {\n+    fun jvmName(name: String)\n+}\n+\n+/**\n+ * Builder for a provided type. It can implement an interface and have some code inside.\n+ */\n+interface GeneratedTypeBuilder : IdentifiableMember {\n+    /**\n+     * Implement a generated interface\n+     */\n+    fun implement(generated: GeneratedInterface)\n+\n+    /**\n+     * Add code to the namespace of the Type\n+     */\n+    fun inner(code: GeneratedCode)",
        "comment_created_at": "2020-08-31T12:44:02+00:00",
        "comment_author": "nerdsupremacist",
        "comment_body": "Got rid of this abstraction by making `ClassLikeBuilder` implement `GeneratedCode.Builder`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "646189172",
    "pr_number": 4432,
    "pr_file": "libraries/stdlib/src/kotlin/collections/Collections.kt",
    "created_at": "2021-06-06T21:19:33+00:00",
    "commented_code": "return -(low + 1)  // key not found\n}\n\n/**\n * If this list starts with the given [prefix], returns a view of the portion of this list without [prefix].\n * The returned list is backed by this list, so non-structural changes in the returned list are reflected in this list, and vice-versa.\n *\n * Structural changes in the base list make the behavior of the view undefined.\n */\npublic fun <T> List<T>.removePrefix(prefix: List<T>): List<T> {\n    return if (this.startWith(prefix)) {\n        this.subList(prefix.size, this.size)\n    } else {\n        this\n    }\n}\n\n/**\n * Returns `true` if this list starts with the specified prefix.\n *\n * For empty [prefix] returns true\n */\npublic fun <T> List<T>.startWith(prefix: List<T>): Boolean {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "646189172",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4432,
        "pr_file": "libraries/stdlib/src/kotlin/collections/Collections.kt",
        "discussion_id": "646189172",
        "commented_code": "@@ -434,6 +434,35 @@ public fun <T> List<T>.binarySearch(fromIndex: Int = 0, toIndex: Int = size, com\n     return -(low + 1)  // key not found\n }\n \n+/**\n+ * If this list starts with the given [prefix], returns a view of the portion of this list without [prefix].\n+ * The returned list is backed by this list, so non-structural changes in the returned list are reflected in this list, and vice-versa.\n+ *\n+ * Structural changes in the base list make the behavior of the view undefined.\n+ */\n+public fun <T> List<T>.removePrefix(prefix: List<T>): List<T> {\n+    return if (this.startWith(prefix)) {\n+        this.subList(prefix.size, this.size)\n+    } else {\n+        this\n+    }\n+}\n+\n+/**\n+ * Returns `true` if this list starts with the specified prefix.\n+ *\n+ * For empty [prefix] returns true\n+ */\n+public fun <T> List<T>.startWith(prefix: List<T>): Boolean {",
        "comment_created_at": "2021-06-06T21:19:33+00:00",
        "comment_author": "Serdnad",
        "comment_body": "Shouldn't this be \"startsWith\", to be consistent with the current implementation for String?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1471288707",
    "pr_number": 5252,
    "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
    "created_at": "2024-01-30T14:09:36+00:00",
    "commented_code": "\"outside of the compilation unit where it's declared.\",\n                false,\n            )\n\n        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1471288707",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-30T14:09:36+00:00",
        "comment_author": "madsager",
        "comment_body": "I personally have a preference for flag names without negations, so I would vote for `sortMembers` with a default of true and a comment stating that turning that off reduces stability of the ABI jar.",
        "pr_file_module": null
      },
      {
        "comment_id": "1471367973",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-30T14:50:27+00:00",
        "comment_author": "udalov",
        "comment_body": "Oh... My preference is flags which are _false by default_... \ud83d\ude43 For some reason it's easier for me to get a model of a \"default\" behavior of the system, just looking at the names of the flags, as opposed to names + their default values.",
        "pr_file_module": null
      },
      {
        "comment_id": "1471379505",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-30T14:56:48+00:00",
        "comment_author": "madsager",
        "comment_body": "!doNotShipIt  \ud83e\udd23 ",
        "pr_file_module": null
      },
      {
        "comment_id": "1471380582",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-30T14:57:24+00:00",
        "comment_author": "madsager",
        "comment_body": "More seriously, as long as there is a flag I'm happy! \ud83d\udc4d ",
        "pr_file_module": null
      },
      {
        "comment_id": "1471710838",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-30T17:59:51+00:00",
        "comment_author": "Tagakov",
        "comment_body": "What about `preserveDeclarationsOrder` ? I can rename the flag and make it disable sorting for inner classes as well to be consistent.",
        "pr_file_module": null
      },
      {
        "comment_id": "1473159544",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5252,
        "pr_file": "plugins/jvm-abi-gen/src/org/jetbrains/kotlin/jvm/abi/JvmAbiCommandLineProcessor.kt",
        "discussion_id": "1471288707",
        "commented_code": "@@ -42,13 +42,27 @@ class JvmAbiCommandLineProcessor : CommandLineProcessor {\n                         \"outside of the compilation unit where it's declared.\",\n                 false,\n             )\n+\n+        val DO_NOT_SORT_MEMBERS_OPTION: CliOption =",
        "comment_created_at": "2024-01-31T16:58:29+00:00",
        "comment_author": "udalov",
        "comment_body": "`preserveDeclarationsOrder` sounds great. `preserveDeclarationOrder` would be even better.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1440148268",
    "pr_number": 5232,
    "pr_file": "plugins/parcelize/parcelize-compiler/parcelize.backend/src/org/jetbrains/kotlin/parcelize/AndroidSymbols.kt",
    "created_at": "2024-01-03T07:36:17+00:00",
    "commented_code": "}\n    }.symbol\n\n    private val kotlinDuration: IrClassSymbol = createClass(",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1440148268",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5232,
        "pr_file": "plugins/parcelize/parcelize-compiler/parcelize.backend/src/org/jetbrains/kotlin/parcelize/AndroidSymbols.kt",
        "discussion_id": "1440148268",
        "commented_code": "@@ -185,6 +186,12 @@ class AndroidSymbols(\n         }\n     }.symbol\n \n+    private val kotlinDuration: IrClassSymbol = createClass(",
        "comment_created_at": "2024-01-03T07:36:17+00:00",
        "comment_author": "madsager",
        "comment_body": "Maybe call this `kotlinTimeDuration` to follow other naming such as `androidOsParcel`?",
        "pr_file_module": null
      },
      {
        "comment_id": "1440481155",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5232,
        "pr_file": "plugins/parcelize/parcelize-compiler/parcelize.backend/src/org/jetbrains/kotlin/parcelize/AndroidSymbols.kt",
        "discussion_id": "1440148268",
        "commented_code": "@@ -185,6 +186,12 @@ class AndroidSymbols(\n         }\n     }.symbol\n \n+    private val kotlinDuration: IrClassSymbol = createClass(",
        "comment_created_at": "2024-01-03T13:57:31+00:00",
        "comment_author": "gala377",
        "comment_body": "Done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1051654064",
    "pr_number": 5046,
    "pr_file": "compiler/ir/backend.jvm/codegen/src/org/jetbrains/kotlin/backend/jvm/codegen/irCodegenUtils.kt",
    "created_at": "2022-12-18T19:34:39+00:00",
    "commented_code": "val property = callee.correspondingPropertySymbol?.owner ?: return false\n    return property.isDeprecatedCallable(context)\n}\n\nval IrClass.getReifiedTypeParameters: ReifiedTypeParametersUsages",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "1051654064",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5046,
        "pr_file": "compiler/ir/backend.jvm/codegen/src/org/jetbrains/kotlin/backend/jvm/codegen/irCodegenUtils.kt",
        "discussion_id": "1051654064",
        "commented_code": "@@ -320,3 +317,27 @@ private fun IrFunction.isAccessorForDeprecatedJvmStaticProperty(context: JvmBack\n     val property = callee.correspondingPropertySymbol?.owner ?: return false\n     return property.isDeprecatedCallable(context)\n }\n+\n+val IrClass.getReifiedTypeParameters: ReifiedTypeParametersUsages",
        "comment_created_at": "2022-12-18T19:34:39+00:00",
        "comment_author": "ilmirus",
        "comment_body": "Please, stick to official code style - `getReifiedTypeParameters` is a function, if you use a property, use `reifiedTypeParameters`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1051770691",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 5046,
        "pr_file": "compiler/ir/backend.jvm/codegen/src/org/jetbrains/kotlin/backend/jvm/codegen/irCodegenUtils.kt",
        "discussion_id": "1051654064",
        "commented_code": "@@ -320,3 +317,27 @@ private fun IrFunction.isAccessorForDeprecatedJvmStaticProperty(context: JvmBack\n     val property = callee.correspondingPropertySymbol?.owner ?: return false\n     return property.isDeprecatedCallable(context)\n }\n+\n+val IrClass.getReifiedTypeParameters: ReifiedTypeParametersUsages",
        "comment_created_at": "2022-12-19T03:51:10+00:00",
        "comment_author": "larryxiao625",
        "comment_body": "Thanks for you suggestion, I have modified it~. Could you please review again :)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695778850",
    "pr_number": 4535,
    "pr_file": "core/compiler.common.jvm/src/org/jetbrains/kotlin/load/java/AbstractAnnotationTypeQualifierResolver.kt",
    "created_at": "2021-08-25T13:56:30+00:00",
    "commented_code": "/*\n * Copyright 2010-2021 JetBrains s.r.o. and Kotlin Programming Language contributors.\n * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n */\n\npackage org.jetbrains.kotlin.load.java\n\nimport org.jetbrains.kotlin.builtins.StandardNames\nimport org.jetbrains.kotlin.descriptors.annotations.KotlinTarget\nimport org.jetbrains.kotlin.name.FqName\nimport java.util.concurrent.ConcurrentHashMap\n\ntypealias TypeQualifierWithApplicability<Annotation> = Pair<Annotation, Set<AnnotationQualifierApplicabilityType>>",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "695778850",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4535,
        "pr_file": "core/compiler.common.jvm/src/org/jetbrains/kotlin/load/java/AbstractAnnotationTypeQualifierResolver.kt",
        "discussion_id": "695778850",
        "commented_code": "@@ -0,0 +1,113 @@\n+/*\n+ * Copyright 2010-2021 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package org.jetbrains.kotlin.load.java\n+\n+import org.jetbrains.kotlin.builtins.StandardNames\n+import org.jetbrains.kotlin.descriptors.annotations.KotlinTarget\n+import org.jetbrains.kotlin.name.FqName\n+import java.util.concurrent.ConcurrentHashMap\n+\n+typealias TypeQualifierWithApplicability<Annotation> = Pair<Annotation, Set<AnnotationQualifierApplicabilityType>>",
        "comment_created_at": "2021-08-25T13:56:30+00:00",
        "comment_author": "dzharkov",
        "comment_body": "I don't insist here, but we're trying to use one-capital-letter names for type parameters (e.g. `A` here)\nSame for AbstractAnnotationTypeQualifierResolver\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "454246644",
    "pr_number": 3544,
    "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/resolverNamedOptions.kt",
    "created_at": "2020-07-14T10:05:07+00:00",
    "commented_code": "/*\n * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n */\n\npackage kotlin.script.experimental.dependencies\n\nfun ExternalDependenciesResolver.Options.value(name: DependenciesResolverOptionsName) =\n    value(name.key)\n\nfun ExternalDependenciesResolver.Options.flag(name: DependenciesResolverOptionsName) =\n    flag(name.key)\n\noperator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName, value: String) {\n    put(key.key, value)\n}\n\n\nenum class DependenciesResolverOptionsName {\n    TRANSITIVE,\n    DEPENDENCY_SCOPES;",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "454246644",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3544,
        "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/resolverNamedOptions.kt",
        "discussion_id": "454246644",
        "commented_code": "@@ -0,0 +1,31 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package kotlin.script.experimental.dependencies\n+\n+fun ExternalDependenciesResolver.Options.value(name: DependenciesResolverOptionsName) =\n+    value(name.key)\n+\n+fun ExternalDependenciesResolver.Options.flag(name: DependenciesResolverOptionsName) =\n+    flag(name.key)\n+\n+operator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName, value: String) {\n+    put(key.key, value)\n+}\n+\n+\n+enum class DependenciesResolverOptionsName {\n+    TRANSITIVE,\n+    DEPENDENCY_SCOPES;",
        "comment_created_at": "2020-07-14T10:05:07+00:00",
        "comment_author": "ligee",
        "comment_body": "Using underscores seems unusual for the maven configuration, and in maven this parameter called just `scope`, so I'd rename it, so the people can guess the param name easier.\r\nIf we want to have the naming flexibility - I'd add the string name parameter to the enum (and use `toLowerCase` as a default value).",
        "pr_file_module": null
      },
      {
        "comment_id": "454329232",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3544,
        "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/resolverNamedOptions.kt",
        "discussion_id": "454246644",
        "commented_code": "@@ -0,0 +1,31 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package kotlin.script.experimental.dependencies\n+\n+fun ExternalDependenciesResolver.Options.value(name: DependenciesResolverOptionsName) =\n+    value(name.key)\n+\n+fun ExternalDependenciesResolver.Options.flag(name: DependenciesResolverOptionsName) =\n+    flag(name.key)\n+\n+operator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName, value: String) {\n+    put(key.key, value)\n+}\n+\n+\n+enum class DependenciesResolverOptionsName {\n+    TRANSITIVE,\n+    DEPENDENCY_SCOPES;",
        "comment_created_at": "2020-07-14T12:45:42+00:00",
        "comment_author": "ileasile",
        "comment_body": "Fixed this name and added a parameter",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "632467374",
    "pr_number": 4383,
    "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/impl/resolverNamedOptions.kt",
    "created_at": "2021-05-14T11:33:55+00:00",
    "commented_code": "*/\nenum class DependenciesResolverOptionsName(optionName: String? = null) {\n    TRANSITIVE,\n    SCOPE;\n    SCOPE,\n    USERNAME,\n    PASSWORD,\n    PRIVATE_KEY_FILE,",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "632467374",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/impl/resolverNamedOptions.kt",
        "discussion_id": "632467374",
        "commented_code": "@@ -23,7 +23,11 @@ operator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName\n  */\n enum class DependenciesResolverOptionsName(optionName: String? = null) {\n     TRANSITIVE,\n-    SCOPE;\n+    SCOPE,\n+    USERNAME,\n+    PASSWORD,\n+    PRIVATE_KEY_FILE,",
        "comment_created_at": "2021-05-14T11:33:55+00:00",
        "comment_author": "ligee",
        "comment_body": "I don't like the names, taking into account that they will be used (in the lowercased form) in the annotations in the actual scripts. But I don't have much better suggestions either. Maybe `AUTH_KEY_FILE`/`AUTH_KEY_PASSPHRASE` will be a bit better, but I'm not sure. Maybe we should discuss it.",
        "pr_file_module": null
      },
      {
        "comment_id": "632602786",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/impl/resolverNamedOptions.kt",
        "discussion_id": "632467374",
        "commented_code": "@@ -23,7 +23,11 @@ operator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName\n  */\n enum class DependenciesResolverOptionsName(optionName: String? = null) {\n     TRANSITIVE,\n-    SCOPE;\n+    SCOPE,\n+    USERNAME,\n+    PASSWORD,\n+    PRIVATE_KEY_FILE,",
        "comment_created_at": "2021-05-14T15:19:36+00:00",
        "comment_author": "ileasile",
        "comment_body": "I'm ok with the names you suggested, maybe it's even worth getting rid of `AUTH_` prefix",
        "pr_file_module": null
      },
      {
        "comment_id": "633292977",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies/src/kotlin/script/experimental/dependencies/impl/resolverNamedOptions.kt",
        "discussion_id": "632467374",
        "commented_code": "@@ -23,7 +23,11 @@ operator fun MutableMap<String, String>.set(key: DependenciesResolverOptionsName\n  */\n enum class DependenciesResolverOptionsName(optionName: String? = null) {\n     TRANSITIVE,\n-    SCOPE;\n+    SCOPE,\n+    USERNAME,\n+    PASSWORD,\n+    PRIVATE_KEY_FILE,",
        "comment_created_at": "2021-05-17T07:41:19+00:00",
        "comment_author": "ligee",
        "comment_body": "Ok, let it be `KEY_FILE`/`KEY_PASSPHRASE`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "441753939",
    "pr_number": 3486,
    "pr_file": "compiler/frontend/src/org/jetbrains/kotlin/resolve/extensions/SyntheticResolveExtension.kt",
    "created_at": "2020-06-17T18:44:52+00:00",
    "commented_code": "fun getSyntheticNestedClassNames(thisDescriptor: ClassDescriptor): List<Name> = emptyList()\n\n    /**\n     * This method should return either superset of what [getSyntheticNestedClassNames] returns,\n     * or null in case it needs to run resolution and inference and/or it is very costly.\n     * Override this method if resolution started to fail with recursion.\n     */\n    fun maybeGetSyntheticNestedClassNames(thisDescriptor: ClassDescriptor): List<Name>? = getSyntheticNestedClassNames(thisDescriptor)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "441753939",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3486,
        "pr_file": "compiler/frontend/src/org/jetbrains/kotlin/resolve/extensions/SyntheticResolveExtension.kt",
        "discussion_id": "441753939",
        "commented_code": "@@ -136,6 +144,13 @@ interface SyntheticResolveExtension {\n \n     fun getSyntheticNestedClassNames(thisDescriptor: ClassDescriptor): List<Name> = emptyList()\n \n+    /**\n+     * This method should return either superset of what [getSyntheticNestedClassNames] returns,\n+     * or null in case it needs to run resolution and inference and/or it is very costly.\n+     * Override this method if resolution started to fail with recursion.\n+     */\n+    fun maybeGetSyntheticNestedClassNames(thisDescriptor: ClassDescriptor): List<Name>? = getSyntheticNestedClassNames(thisDescriptor)",
        "comment_created_at": "2020-06-17T18:44:52+00:00",
        "comment_author": "sandwwraith",
        "comment_body": "imo, `getPossibleSyntheticNestedClassNames` is a slightly better name for this method",
        "pr_file_module": null
      }
    ]
  }
]
