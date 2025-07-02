---
title: Decompose complex algorithms
description: When implementing algorithms, break down complex methods that handle
  multiple concerns into smaller, more focused methods. This improves maintainability,
  makes edge cases easier to handle, and allows for more flexible reuse of algorithm
  components.
repository: dotnet/runtime
label: Algorithms
language: C
comments_count: 4
repository_stars: 16578
---

When implementing algorithms, break down complex methods that handle multiple concerns into smaller, more focused methods. This improves maintainability, makes edge cases easier to handle, and allows for more flexible reuse of algorithm components.

For example, instead of having a single method that handles multiple responsibilities:

```c
static gboolean
get_common_simd_info (MonoClass *vector_klass, MonoMethodSignature *csignature, 
                      MonoTypeEnum *atype, int *vector_size, int *arg_size, int *scalar_arg)
{
    // Complex logic handling multiple concerns:
    // 1. Getting size information
    // 2. Determining element type
    // 3. Finding scalar arguments
    // ...
}
```

Break it into focused methods with clear responsibilities:

```c
static gboolean
get_common_simd_info (MonoClass *klass, MonoTypeEnum *atype, 
                      int *klass_size, int *arg_size)
{
    // Focus only on getting class size and element type information
}

static int 
get_common_simd_scalar_arg (MonoMethodSignature *csignature)
{
    // Focus only on finding scalar arguments
}
```

This approach makes algorithms more adaptable to changing requirements, such as supporting additional intrinsics or handling different types of operations. It also simplifies testing and debugging by isolating specific functionality into well-defined methods with clearer purposes.


[
  {
    "discussion_id": "1655202643",
    "pr_number": 104049,
    "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
    "created_at": "2024-06-26T16:37:02+00:00",
    "commented_code": "simd_opcode = MINT_SIMD_INTRINS_P_PP;\n\t\t\tsimd_intrins = INTERP_SIMD_INTRINSIC_V128_AND_NOT;\n\t\t\tbreak;\n\t\tcase SN_As:\n\t\tcase SN_AsByte:\n\t\tcase SN_AsDouble:\n\t\tcase SN_AsInt16:\n\t\tcase SN_AsInt32:\n\t\tcase SN_AsInt64:\n\t\tcase SN_AsNInt:\n\t\tcase SN_AsNUInt:\n\t\tcase SN_AsPlane:\n\t\tcase SN_AsQuaternion:\n\t\tcase SN_AsSByte:\n\t\tcase SN_AsSingle:\n\t\tcase SN_AsUInt16:\n\t\tcase SN_AsUInt32:\n\t\tcase SN_AsUInt64:\n\t\tcase SN_AsVector: {\n\t\t\treturn FALSE;",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1655202643",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1655202643",
        "commented_code": "@@ -387,6 +408,37 @@ emit_sri_vector128 (TransformData *td, MonoMethod *cmethod, MonoMethodSignature\n \t\t\tsimd_opcode = MINT_SIMD_INTRINS_P_PP;\n \t\t\tsimd_intrins = INTERP_SIMD_INTRINSIC_V128_AND_NOT;\n \t\t\tbreak;\n+\t\tcase SN_As:\n+\t\tcase SN_AsByte:\n+\t\tcase SN_AsDouble:\n+\t\tcase SN_AsInt16:\n+\t\tcase SN_AsInt32:\n+\t\tcase SN_AsInt64:\n+\t\tcase SN_AsNInt:\n+\t\tcase SN_AsNUInt:\n+\t\tcase SN_AsPlane:\n+\t\tcase SN_AsQuaternion:\n+\t\tcase SN_AsSByte:\n+\t\tcase SN_AsSingle:\n+\t\tcase SN_AsUInt16:\n+\t\tcase SN_AsUInt32:\n+\t\tcase SN_AsUInt64:\n+\t\tcase SN_AsVector: {\n+\t\t\treturn FALSE;",
        "comment_created_at": "2024-06-26T16:37:02+00:00",
        "comment_author": "tannergooding",
        "comment_body": "@kg, I don't see any obvious existing handlers for what is effectively \"bitcast\" (that is the input is returned directly with no change, the API only exists to satisfy the type system).\r\n\r\nDo you have a pointer to any similar handling that might exist?",
        "pr_file_module": null
      },
      {
        "comment_id": "1655258436",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1655202643",
        "commented_code": "@@ -387,6 +408,37 @@ emit_sri_vector128 (TransformData *td, MonoMethod *cmethod, MonoMethodSignature\n \t\t\tsimd_opcode = MINT_SIMD_INTRINS_P_PP;\n \t\t\tsimd_intrins = INTERP_SIMD_INTRINSIC_V128_AND_NOT;\n \t\t\tbreak;\n+\t\tcase SN_As:\n+\t\tcase SN_AsByte:\n+\t\tcase SN_AsDouble:\n+\t\tcase SN_AsInt16:\n+\t\tcase SN_AsInt32:\n+\t\tcase SN_AsInt64:\n+\t\tcase SN_AsNInt:\n+\t\tcase SN_AsNUInt:\n+\t\tcase SN_AsPlane:\n+\t\tcase SN_AsQuaternion:\n+\t\tcase SN_AsSByte:\n+\t\tcase SN_AsSingle:\n+\t\tcase SN_AsUInt16:\n+\t\tcase SN_AsUInt32:\n+\t\tcase SN_AsUInt64:\n+\t\tcase SN_AsVector: {\n+\t\t\treturn FALSE;",
        "comment_created_at": "2024-06-26T17:16:24+00:00",
        "comment_author": "kg",
        "comment_body": "simd-methods.def and transform-simd are where most of the supported names are, iirc. i don't see support for bitcast and don't remember implementing it.",
        "pr_file_module": null
      },
      {
        "comment_id": "1655353770",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1655202643",
        "commented_code": "@@ -387,6 +408,37 @@ emit_sri_vector128 (TransformData *td, MonoMethod *cmethod, MonoMethodSignature\n \t\t\tsimd_opcode = MINT_SIMD_INTRINS_P_PP;\n \t\t\tsimd_intrins = INTERP_SIMD_INTRINSIC_V128_AND_NOT;\n \t\t\tbreak;\n+\t\tcase SN_As:\n+\t\tcase SN_AsByte:\n+\t\tcase SN_AsDouble:\n+\t\tcase SN_AsInt16:\n+\t\tcase SN_AsInt32:\n+\t\tcase SN_AsInt64:\n+\t\tcase SN_AsNInt:\n+\t\tcase SN_AsNUInt:\n+\t\tcase SN_AsPlane:\n+\t\tcase SN_AsQuaternion:\n+\t\tcase SN_AsSByte:\n+\t\tcase SN_AsSingle:\n+\t\tcase SN_AsUInt16:\n+\t\tcase SN_AsUInt32:\n+\t\tcase SN_AsUInt64:\n+\t\tcase SN_AsVector: {\n+\t\t\treturn FALSE;",
        "comment_created_at": "2024-06-26T18:33:22+00:00",
        "comment_author": "tannergooding",
        "comment_body": "I ended up following what `op_UnaryNegation` does and adding handlers that basically do memcpy to handle it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1656224573",
    "pr_number": 104049,
    "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
    "created_at": "2024-06-27T03:32:57+00:00",
    "commented_code": "}\n\nstatic gboolean\nget_common_simd_info (MonoClass *vector_klass, MonoMethodSignature *csignature, MonoTypeEnum *atype, int *vector_size, int *arg_size, int *scalar_arg)\nget_common_simd_info (MonoClass *klass, MonoTypeEnum *atype, int *klass_size, int *arg_size)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1656224573",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1656224573",
        "commented_code": "@@ -283,47 +304,49 @@ emit_common_simd_operations (TransformData *td, int id, int atype, int vector_si\n }\n \n static gboolean\n-get_common_simd_info (MonoClass *vector_klass, MonoMethodSignature *csignature, MonoTypeEnum *atype, int *vector_size, int *arg_size, int *scalar_arg)\n+get_common_simd_info (MonoClass *klass, MonoTypeEnum *atype, int *klass_size, int *arg_size)",
        "comment_created_at": "2024-06-27T03:32:57+00:00",
        "comment_author": "tannergooding",
        "comment_body": "This file ended up needing a bit of a refactoring as there were some assumptions in place that don't hold when supporting additional intrinsics.\r\n\r\nIn particular, there are various intrinsics where:\r\n* one of the SIMD types may not be generic at all (`Vector2`, `Vector3`, `Vector4`)\r\n* multiple generic types exist (`As<TFrom, TTo>`)\r\n* the return type may not be a 128-bit vector (`AsVector2`, `AsVector3`)\r\n\r\nSo, what I did here was I broke this `get_common_simd_info` method into two:\r\n* `get_common_simd_info`\r\n* `get_common_simd_scalar_arg`\r\n\r\nThe former now always gets the size of the input klass and secondly determines if it is a SIMD type and what the underlying element type is if so. While the latter identifies the first non-SIMD argument, if one exists.\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1656227647",
    "pr_number": 104049,
    "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
    "created_at": "2024-06-27T03:33:35+00:00",
    "commented_code": "}\n\nstatic gboolean\nget_common_simd_info (MonoClass *vector_klass, MonoMethodSignature *csignature, MonoTypeEnum *atype, int *vector_size, int *arg_size, int *scalar_arg)\nget_common_simd_info (MonoClass *klass, MonoTypeEnum *atype, int *klass_size, int *arg_size)\n{\n\tif (!m_class_is_simd_type (vector_klass) && csignature->param_count)\n\t\tvector_klass = mono_class_from_mono_type_internal (csignature->params [0]);\n\tif (!m_class_is_simd_type (vector_klass))\n\t*klass_size = mono_class_value_size (klass, NULL);\n\tif (!m_class_is_simd_type (klass))\n\t\treturn FALSE;\n\n\tMonoType *arg_type = mono_class_get_context (vector_klass)->class_inst->type_argv [0];\n\tif (!mono_type_is_primitive (arg_type))\n\t\treturn FALSE;\n\t*atype = arg_type->type;\n\tif (*atype == MONO_TYPE_BOOLEAN)\n\t\treturn FALSE;\n\t*vector_size = mono_class_value_size (vector_klass, NULL);\n\tg_assert (*vector_size == SIZEOF_V128);\n\tif (arg_size)\n\tif (mono_class_is_ginst (klass)) {\n\t\tMonoType *arg_type = mono_class_get_context (klass)->class_inst->type_argv [0];\n\t\tif (!mono_type_is_primitive (arg_type))\n\t\t\treturn FALSE;\n\t\t*atype = arg_type->type;\n\t\t*arg_size = mono_class_value_size (mono_class_from_mono_type_internal (arg_type), NULL);\n\t\tif (*atype == MONO_TYPE_BOOLEAN)\n\t\t\treturn FALSE;\n\t} else {\n\t\t*atype = MONO_TYPE_R4;\n\t\t*arg_size = sizeof (float);\n\t}\n\treturn TRUE;\n}\n\n\t*scalar_arg = -1;\nstatic int get_common_simd_scalar_arg (MonoMethodSignature *csignature)\n{\n\tfor (int i = 0; i < csignature->param_count; i++) {\n\t\tif (csignature->params [i]->type != MONO_TYPE_GENERICINST)\n\t\t\t*scalar_arg = i;\n\t\tif (MONO_TYPE_IS_PRIMITIVE(csignature->params [i]))\n\t\t\treturn i;\n\t}\n\n\treturn TRUE;\n\treturn -1;\n}\n\nstatic void\nemit_common_simd_epilogue (TransformData *td, MonoClass *vector_klass, MonoMethodSignature *csignature, int vector_size, gboolean allow_void)\nemit_common_simd_epilogue (TransformData *td, MonoMethodSignature *csignature)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1656227647",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1656227647",
        "commented_code": "@@ -283,47 +304,49 @@ emit_common_simd_operations (TransformData *td, int id, int atype, int vector_si\n }\n \n static gboolean\n-get_common_simd_info (MonoClass *vector_klass, MonoMethodSignature *csignature, MonoTypeEnum *atype, int *vector_size, int *arg_size, int *scalar_arg)\n+get_common_simd_info (MonoClass *klass, MonoTypeEnum *atype, int *klass_size, int *arg_size)\n {\n-\tif (!m_class_is_simd_type (vector_klass) && csignature->param_count)\n-\t\tvector_klass = mono_class_from_mono_type_internal (csignature->params [0]);\n-\tif (!m_class_is_simd_type (vector_klass))\n+\t*klass_size = mono_class_value_size (klass, NULL);\n+\tif (!m_class_is_simd_type (klass))\n \t\treturn FALSE;\n-\n-\tMonoType *arg_type = mono_class_get_context (vector_klass)->class_inst->type_argv [0];\n-\tif (!mono_type_is_primitive (arg_type))\n-\t\treturn FALSE;\n-\t*atype = arg_type->type;\n-\tif (*atype == MONO_TYPE_BOOLEAN)\n-\t\treturn FALSE;\n-\t*vector_size = mono_class_value_size (vector_klass, NULL);\n-\tg_assert (*vector_size == SIZEOF_V128);\n-\tif (arg_size)\n+\tif (mono_class_is_ginst (klass)) {\n+\t\tMonoType *arg_type = mono_class_get_context (klass)->class_inst->type_argv [0];\n+\t\tif (!mono_type_is_primitive (arg_type))\n+\t\t\treturn FALSE;\n+\t\t*atype = arg_type->type;\n \t\t*arg_size = mono_class_value_size (mono_class_from_mono_type_internal (arg_type), NULL);\n+\t\tif (*atype == MONO_TYPE_BOOLEAN)\n+\t\t\treturn FALSE;\n+\t} else {\n+\t\t*atype = MONO_TYPE_R4;\n+\t\t*arg_size = sizeof (float);\n+\t}\n+\treturn TRUE;\n+}\n \n-\t*scalar_arg = -1;\n+static int get_common_simd_scalar_arg (MonoMethodSignature *csignature)\n+{\n \tfor (int i = 0; i < csignature->param_count; i++) {\n-\t\tif (csignature->params [i]->type != MONO_TYPE_GENERICINST)\n-\t\t\t*scalar_arg = i;\n+\t\tif (MONO_TYPE_IS_PRIMITIVE(csignature->params [i]))\n+\t\t\treturn i;\n \t}\n-\n-\treturn TRUE;\n+\treturn -1;\n }\n \n static void\n-emit_common_simd_epilogue (TransformData *td, MonoClass *vector_klass, MonoMethodSignature *csignature, int vector_size, gboolean allow_void)\n+emit_common_simd_epilogue (TransformData *td, MonoMethodSignature *csignature)",
        "comment_created_at": "2024-06-27T03:33:35+00:00",
        "comment_author": "tannergooding",
        "comment_body": "To support methods which return a value type, but where that isn't a 128-bit vector, this explicitly gets the return type from the signature to ensure there can be no accidents",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1656246224",
    "pr_number": 104049,
    "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
    "created_at": "2024-06-27T03:37:29+00:00",
    "commented_code": "gint16 simd_opcode = -1;\n\tgint16 simd_intrins = -1;\n\n\tvector_klass = mono_class_from_mono_type_internal (csignature->ret);\n\tMonoTypeEnum ret_atype;",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1656246224",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 104049,
        "pr_file": "src/mono/mono/mini/interp/transform-simd.c",
        "discussion_id": "1656246224",
        "commented_code": "@@ -375,124 +395,246 @@ emit_sri_vector128 (TransformData *td, MonoMethod *cmethod, MonoMethodSignature\n \tgint16 simd_opcode = -1;\n \tgint16 simd_intrins = -1;\n \n-\tvector_klass = mono_class_from_mono_type_internal (csignature->ret);\n+\tMonoTypeEnum ret_atype;",
        "comment_created_at": "2024-06-27T03:37:29+00:00",
        "comment_author": "tannergooding",
        "comment_body": "In here, we consistently query the relevant simd information of the return type and if it exists the simd information of the  first parameter (this is enough to correctly handle all the cases that currently exist).\r\n\r\nThere's actually quite a bit of logic in this function that *could* be moved down into `emit_common_simd_operations`, as APIs like `AndNot` exist for `Vector128<T>` and `Vector<T>`, they may also exist for types like `Vector4` in the future. I opted to not move that down in this PR, to try and keep the total churn under control.\r\n\r\nBut, I did add some basic validation that the encountered signatures are roughly as expected to help ensure we don't hit issues in the future as new overloads are introduced or the general SIMD support in Mono is expanded.",
        "pr_file_module": null
      }
    ]
  }
]
