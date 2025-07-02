---
title: Configure type serialization
description: When working with databases that exchange data with other systems, ensure
  proper serialization and deserialization of data types like UUIDs, dates, or complex
  objects. System-specific representation differences can lead to data corruption,
  query failures, or incorrect results.
repository: elastic/elasticsearch
label: Database
language: Markdown
comments_count: 4
repository_stars: 73104
---

When working with databases that exchange data with other systems, ensure proper serialization and deserialization of data types like UUIDs, dates, or complex objects. System-specific representation differences can lead to data corruption, query failures, or incorrect results.

For example, when working with MongoDB and UUIDs:

```
# Specify UUID representation in connection string
mongodb+srv://username:password@cluster.mongodb.net/mydb?uuidRepresentation=standard

# For legacy UUID representations, use appropriate parameters:
# - C#: uuidRepresentation=csharpLegacy
# - Java: uuidRepresentation=javaLegacy
# - Python: uuidRepresentation=pythonLegacy
```

When joining data across different sources, ensure join keys have compatible data types:
- Integer types (`byte`, `short`, `integer`) can typically be joined
- Float types (`half_float`, `float`, `scaled_float`, `double`) are often interchangeable
- Date types often require exact matching or explicit conversion
- Text/string types may require specific formatting or normalization

Always document data type compatibility requirements in your schema design and provide conversion functions where needed to ensure consistent data handling across systems.


[
  {
    "discussion_id": "2154405635",
    "pr_number": 129492,
    "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
    "created_at": "2025-06-18T11:52:39+00:00",
    "commented_code": "See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n\n#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n\nMongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n\nWith 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2154405635",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154405635",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.",
        "comment_created_at": "2025-06-18T11:52:39+00:00",
        "comment_author": "charlotte-hoblik",
        "comment_body": "```suggestion\r\nWith connector framework version 9.0.3, we improved how standard UUIDs are handled. Now, the MongoDB connector can correctly deserialize UUIDs into valid Elasticsearch values. However, for legacy UUIDs or older connector versions, you might need to adjust the connection string to specify the UUID representation.\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2154645835",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154405635",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.",
        "comment_created_at": "2025-06-18T13:41:10+00:00",
        "comment_author": "artem-shelkovnikov",
        "comment_body": "Currently the change has been backported to 8.18 branch which should make it available in 8.18.3 release.",
        "pr_file_module": null
      },
      {
        "comment_id": "2154655180",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154405635",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.",
        "comment_created_at": "2025-06-18T13:45:04+00:00",
        "comment_author": "charlotte-hoblik",
        "comment_body": "You\u2019re absolutely right, the change has been backported to 8.18.3. That said, due to a documentation system shift between the 8.x and 9.x, we\u2019re currently maintaining this doc version against the 9.x branches. We\u2019re still adding 8.18.3 info to the 8.x docs where relevant, so it\u2019s covered in both places.",
        "pr_file_module": null
      },
      {
        "comment_id": "2154658977",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154405635",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.",
        "comment_created_at": "2025-06-18T13:46:41+00:00",
        "comment_author": "artem-shelkovnikov",
        "comment_body": "Ah sorry, I got confused by it - thank you for the suggestions, accepted all!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2154429939",
    "pr_number": 129492,
    "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
    "created_at": "2025-06-18T12:06:08+00:00",
    "commented_code": "See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n\n#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n\nMongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n\nWith 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.\n\nFor example, if you are using modern UUID representation, adding `uuidRepresentation=standard` query parameter into the URL in the `host` Rich Configurable Field will make the connector properly handle UUIDs. With this change the full `host` Rich Configurable Field value could look like this: `mongodb+srv://my_username:my_password@cluster0.mongodb.net/mydb?w=majority&uuidRepresentation=standard`",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2154429939",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154429939",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.\n+\n+For example, if you are using modern UUID representation, adding `uuidRepresentation=standard` query parameter into the URL in the `host` Rich Configurable Field will make the connector properly handle UUIDs. With this change the full `host` Rich Configurable Field value could look like this: `mongodb+srv://my_username:my_password@cluster0.mongodb.net/mydb?w=majority&uuidRepresentation=standard`",
        "comment_created_at": "2025-06-18T12:06:08+00:00",
        "comment_author": "charlotte-hoblik",
        "comment_body": "```suggestion\r\nFor example, if you are using the modern UUID representation, adding the `uuidRepresentation=standard` query parameter to the MongoDB connection URI in the `host` Rich Configurable Field will allow the connector to properly handle UUIDs. With this change, the full `host` Rich Configurable Field value could look like this:`mongodb+srv://my_username:my_password@cluster0.mongodb.net/mydb?w=majority&uuidRepresentation=standard`\r\n```\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2154435770",
    "pr_number": 129492,
    "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
    "created_at": "2025-06-18T12:09:22+00:00",
    "commented_code": "See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n\n#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n\nMongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n\nWith 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.\n\nFor example, if you are using modern UUID representation, adding `uuidRepresentation=standard` query parameter into the URL in the `host` Rich Configurable Field will make the connector properly handle UUIDs. With this change the full `host` Rich Configurable Field value could look like this: `mongodb+srv://my_username:my_password@cluster0.mongodb.net/mydb?w=majority&uuidRepresentation=standard`\n\nIf you are using, for example, legacy C# representation of UUIDs, then you should add `uuidRepresentation=csharpLegacy`, for Java it'll be `uuidRepresentation=javaLegacy` and for Python it'll be `uuidRepresentation=pythonLegacy`. Full explanation can be found in [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html#configuring-a-uuid-representation).",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2154435770",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129492,
        "pr_file": "docs/reference/search-connectors/es-connectors-mongodb.md",
        "discussion_id": "2154435770",
        "commented_code": "@@ -251,6 +251,15 @@ A bug introduced in **8.12.0** causes the Connectors docker image to error out i\n \n See [Known issues](/release-notes/known-issues.md) for any issues affecting all connectors.\n \n+#### UUIDs are not correctly deserialised causing problems with ingesting documents into Elasticsearch\n+\n+MongoDB has special handling of UUID type: there is a legacy and a modern approach. You can read [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html) about the details.\n+\n+With 8.18.3 better handling of standard UUID representation has been implemented - now MongoDB connector is able to properly deserialise them into valid UUIDs. However, for legacy UUIDs or older versions of the connector you might need to adjust the connection string to specify the UUID representation.\n+\n+For example, if you are using modern UUID representation, adding `uuidRepresentation=standard` query parameter into the URL in the `host` Rich Configurable Field will make the connector properly handle UUIDs. With this change the full `host` Rich Configurable Field value could look like this: `mongodb+srv://my_username:my_password@cluster0.mongodb.net/mydb?w=majority&uuidRepresentation=standard`\n+\n+If you are using, for example, legacy C# representation of UUIDs, then you should add `uuidRepresentation=csharpLegacy`, for Java it'll be `uuidRepresentation=javaLegacy` and for Python it'll be `uuidRepresentation=pythonLegacy`. Full explanation can be found in [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html#configuring-a-uuid-representation).",
        "comment_created_at": "2025-06-18T12:09:22+00:00",
        "comment_author": "charlotte-hoblik",
        "comment_body": "```suggestion\r\nIf you\u2019re using a legacy UUID representation, you should adjust the connection URI accordingly. For example:\r\n\r\n- C#: `uuidRepresentation=csharpLegacy`\r\n- Java: `uuidRepresentation=javaLegacy`\r\n- Python: `uuidRepresentation=pythonLegacy`\r\n\r\nYou can find a full explanation in the [official docs](https://pymongo.readthedocs.io/en/stable/examples/uuid.html#configuring-a-uuid-representation).\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2180393094",
    "pr_number": 130410,
    "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
    "created_at": "2025-07-02T15:42:40+00:00",
    "commented_code": "* `short` and `byte` are compatible with `integer` (all represented as `int`)\n    * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n  * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n\nTo obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n\nFor a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\nThe list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2180393094",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130410,
        "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
        "discussion_id": "2180393094",
        "commented_code": "@@ -151,10 +151,15 @@ To use `LOOKUP JOIN`, the following requirements must be met:\n     * `short` and `byte` are compatible with `integer` (all represented as `int`)\n     * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n   * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n+  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n \n To obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n \n-For a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\n+The list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
        "comment_created_at": "2025-07-02T15:42:40+00:00",
        "comment_author": "leemthompo",
        "comment_body": "@craigtaverner I think this section is a little messy now, and technically this should be all part of the bulleted list\r\n\r\nI suggest we revamp the **Prerequisites** section and use subheadings, and instead of prose/list items for the supported/unsupported types, perhaps a table would be a good alternative?\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2180396635",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130410,
        "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
        "discussion_id": "2180393094",
        "commented_code": "@@ -151,10 +151,15 @@ To use `LOOKUP JOIN`, the following requirements must be met:\n     * `short` and `byte` are compatible with `integer` (all represented as `int`)\n     * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n   * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n+  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n \n To obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n \n-For a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\n+The list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
        "comment_created_at": "2025-07-02T15:44:36+00:00",
        "comment_author": "leemthompo",
        "comment_body": "Here's an approach, in docsv3 syntax:\r\n\r\n\r\n## Prerequisites\r\n\r\n### Index configuration\r\nIndices used for lookups must be configured with the [`lookup` index mode](/reference/elasticsearch/index-settings/index-modules.md#index-mode-setting).\r\n\r\n### Data type compatibility\r\nJoin keys must have compatible data types between the source and lookup indices. Types within the same compatibility group can be joined together:\r\n\r\n| Compatibility group | Types | Notes |\r\n|---------------------|-------|--------|\r\n| **Integer family** | `byte`, `short`, `integer` | All interchangeable |\r\n| **Float family** | `half_float`, `float`, `scaled_float`, `double` | All interchangeable |\r\n| **Keyword family** | `keyword`, `text.keyword` | Text fields only as join key on left-hand side and must have `.keyword` subfield |\r\n| **Date (Exact)** | `DATE` | Must match exactly |\r\n| **Date Nanos (Exact)** | `DATE_NANOS` | Must match exactly |\r\n| **Boolean** | `boolean` | Must match exactly |\r\n\r\n```{note}\r\nFor a complete list of all types supported in `LOOKUP JOIN`, refer to the [`LOOKUP JOIN` supported types table](/reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join).\r\n```\r\n\r\n```{tip}\r\nTo obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\r\n```\r\n\r\n### Unsupported Types\r\nIn addition to the [{{esql}} unsupported field types](/reference/query-languages/esql/limitations.md#_unsupported_types), `LOOKUP JOIN` does not support:\r\n\r\n* `VERSION`\r\n* `UNSIGNED_LONG` \r\n* Spatial types like `GEO_POINT`, `GEO_SHAPE`\r\n* Temporal intervals like `DURATION`, `PERIOD`\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2180418260",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130410,
        "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
        "discussion_id": "2180393094",
        "commented_code": "@@ -151,10 +151,15 @@ To use `LOOKUP JOIN`, the following requirements must be met:\n     * `short` and `byte` are compatible with `integer` (all represented as `int`)\n     * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n   * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n+  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n \n To obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n \n-For a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\n+The list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
        "comment_created_at": "2025-07-02T15:53:47+00:00",
        "comment_author": "leemthompo",
        "comment_body": "Or perhaps we can lose the overview table/list entirely and delegate to the new autogenerated table?",
        "pr_file_module": null
      },
      {
        "comment_id": "2180435815",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130410,
        "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
        "discussion_id": "2180393094",
        "commented_code": "@@ -151,10 +151,15 @@ To use `LOOKUP JOIN`, the following requirements must be met:\n     * `short` and `byte` are compatible with `integer` (all represented as `int`)\n     * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n   * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n+  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n \n To obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n \n-For a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\n+The list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
        "comment_created_at": "2025-07-02T15:59:14+00:00",
        "comment_author": "leemthompo",
        "comment_body": "anyways just food for thought, I think the data type compatibility info should be a standalone section in any case, whether it's under prerequisites or not :)",
        "pr_file_module": null
      },
      {
        "comment_id": "2180453560",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130410,
        "pr_file": "docs/reference/query-languages/esql/esql-lookup-join.md",
        "discussion_id": "2180393094",
        "commented_code": "@@ -151,10 +151,15 @@ To use `LOOKUP JOIN`, the following requirements must be met:\n     * `short` and `byte` are compatible with `integer` (all represented as `int`)\n     * `float`, `half_float`, and `scaled_float` are compatible with `double` (all represented as `double`)\n   * For text fields: You can only use text fields as the join key on the left-hand side of the join and only if they have a `.keyword` subfield\n+  * `DATE` and `DATE_NANOS` can only be joined against the exact same type.\n \n To obtain a join key with a compatible type, use a [conversion function](/reference/query-languages/esql/functions-operators/type-conversion-functions.md) if needed.\n \n-For a complete list of supported data types and their internal representations, see the [Supported Field Types documentation](/reference/query-languages/esql/limitations.md#_supported_types).\n+The list of unsupported fields includes all types not supported by {{esql}} as described in the [Unsupported Field Types documentation](/reference/query-languages/esql/limitations.md#_unsupported_types).",
        "comment_created_at": "2025-07-02T16:07:59+00:00",
        "comment_author": "craigtaverner",
        "comment_body": "I incorporated your changes. I agree it makes things look more similar with two tables. But I think users might find both places independently, so it is not too bad to have two ways. The generated one is more up-to-date. I did make one fix to your table, because we can join between integers and float now too.",
        "pr_file_module": null
      }
    ]
  }
]
