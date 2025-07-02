---
title: Complete API parameter documentation
description: 'API endpoints must include comprehensive documentation for all parameters.
  For each parameter, clearly specify:


  1. Whether it''s required or optional

  2. The data type and format'
repository: elastic/elasticsearch
label: API
language: Other
comments_count: 2
repository_stars: 73104
---

API endpoints must include comprehensive documentation for all parameters. For each parameter, clearly specify:

1. Whether it's required or optional
2. The data type and format
3. Default values when omitted
4. Validation rules and constraints (e.g., maximum values, character limits)
5. Accepted formats and encoding requirements
6. Behavior details (exact matching vs pattern matching)

This ensures consistency between API implementation and documentation, prevents integration issues, and improves developer experience.

Example:
```
`connector_name`::
(Optional, string) A comma-separated list of connector names, used to filter search results.
Default: Returns all connectors if omitted.
Maximum: 100 connector names.
Format: Exact matches only, URL-encoded values required for special characters.
Validation: Names must follow the same validation rules as defined in the creation API.
```

When updating APIs, ensure that parameter behavior aligns with UI expectations and vice versa to prevent disconnects between API functionality and user experience.


[
  {
    "discussion_id": "1576203682",
    "pr_number": 107539,
    "pr_file": "docs/reference/connector/apis/list-connectors-api.asciidoc",
    "created_at": "2024-04-23T12:53:00+00:00",
    "commented_code": "[[list-connector-api-prereq]]\n==== {api-prereq-title}\n\n* To sync data using connectors, it's essential to have the Elastic connectors service running.\n* To sync data using self-managed connectors, it's required to have the Elastic connectors service running.\n\n[[list-connector-api-path-params]]\n==== {api-path-parms-title}\n\n`size`::\n(Optional, integer) Maximum number of results to retrieve.\n// Is there a default?\n\n`from`::\n(Optional, integer) The offset from the first result to fetch.\n\n`index_name`::\n(Optional, string) A comma-separated list of data index names associated with connectors, used to filter search results.\n(Optional, string) A comma-separated list of index names associated with connectors, used to filter search results.\n// What is the maximum number of index names that can be specified?\n// Does this have to be an exact match or are regexes also accepted?\n// \"data index\" - I don't believe we refer to indices as data indices anywhere else\n\n`connector_name`::\n(Optional, string) A comma-separated list of connector names, used to filter search results.\n// What is the maximum number of names that can be specified?\n// Does this have to be an exact match or are regexes also accepted?\n// If we accept any name as connector name, what encoding is accepted as parameter? e.g. how would a request for a connector named \"My test connector\" look like?",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1576203682",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107539,
        "pr_file": "docs/reference/connector/apis/list-connectors-api.asciidoc",
        "discussion_id": "1576203682",
        "commented_code": "@@ -18,25 +18,33 @@ Returns information about all stored connectors.\n [[list-connector-api-prereq]]\n ==== {api-prereq-title}\n \n-* To sync data using connectors, it's essential to have the Elastic connectors service running.\n+* To sync data using self-managed connectors, it's required to have the Elastic connectors service running.\n \n [[list-connector-api-path-params]]\n ==== {api-path-parms-title}\n \n `size`::\n (Optional, integer) Maximum number of results to retrieve.\n+// Is there a default?\n \n `from`::\n (Optional, integer) The offset from the first result to fetch.\n \n `index_name`::\n-(Optional, string) A comma-separated list of data index names associated with connectors, used to filter search results.\n+(Optional, string) A comma-separated list of index names associated with connectors, used to filter search results.\n+// What is the maximum number of index names that can be specified?\n+// Does this have to be an exact match or are regexes also accepted?\n+// \"data index\" - I don't believe we refer to indices as data indices anywhere else\n \n `connector_name`::\n (Optional, string) A comma-separated list of connector names, used to filter search results.\n+// What is the maximum number of names that can be specified?\n+// Does this have to be an exact match or are regexes also accepted?\n+// If we accept any name as connector name, what encoding is accepted as parameter? e.g. how would a request for a connector named \"My test connector\" look like?",
        "comment_created_at": "2024-04-23T12:53:00+00:00",
        "comment_author": "jedrazb",
        "comment_body": "as this is a URL param it should be encoded as `My%20test%20connector` - I don't think we should explain how URL encoding works here",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1567516376",
    "pr_number": 107344,
    "pr_file": "docs/reference/connector/apis/create-connector-api.asciidoc",
    "created_at": "2024-04-16T14:59:35+00:00",
    "commented_code": "`index_name`::\n(Required, string) The target index for syncing data by the connector.\n\n// making this required does not align with the BYOI for connectors. I believe we discussed we're making this optional. \nIn Kibana, attaching an index also creates the index, if we specify an index here, will it be created? When? \n`name`::\n(Optional, string) The name of the connector.\n// having an optional name Killed my Kibana experience. Without an index or a name, there is no way for me to go to connector Overview.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1567516376",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107344,
        "pr_file": "docs/reference/connector/apis/create-connector-api.asciidoc",
        "discussion_id": "1567516376",
        "commented_code": "@@ -66,19 +68,22 @@ Creates a connector document in the internal index and initializes its configura\n \n `index_name`::\n (Required, string) The target index for syncing data by the connector.\n-\n+// making this required does not align with the BYOI for connectors. I believe we discussed we're making this optional. \n+In Kibana, attaching an index also creates the index, if we specify an index here, will it be created? When? \n `name`::\n (Optional, string) The name of the connector.\n+// having an optional name Killed my Kibana experience. Without an index or a name, there is no way for me to go to connector Overview.",
        "comment_created_at": "2024-04-16T14:59:35+00:00",
        "comment_author": "danajuratoni",
        "comment_body": "Connector name comes with a set of validations in Kibana. What is the proposal for the next steps: relaxing Kibana validations or adding validations to the API?",
        "pr_file_module": null
      }
    ]
  }
]
