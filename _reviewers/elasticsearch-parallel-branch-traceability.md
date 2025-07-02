---
title: Parallel branch traceability
description: 'When implementing algorithms with parallel processing branches, ensure
  proper traceability and data consistency across all branches to facilitate result
  analysis and debugging:'
repository: elastic/elasticsearch
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 73104
---

When implementing algorithms with parallel processing branches, ensure proper traceability and data consistency across all branches to facilitate result analysis and debugging:

1. Add discriminator fields to identify the source branch for each result entry
2. Maintain consistent data types for identical field names across all branches
3. Establish a clear strategy for handling missing fields (e.g., null values)
4. Preserve the ordering of results within each branch while providing mechanisms to control inter-branch ordering

Example implementation:
```
function processBranches(input) {
  // Create parallel branches
  const branches = [branchA(input), branchB(input), branchC(input)];
  
  // Combine results with branch identifiers
  const results = [];
  branches.forEach((branchResult, index) => {
    branchResult.forEach(item => {
      // Add discriminator field
      item.branchId = `branch${index + 1}`;
      // Ensure all fields exist (with nulls if needed)
      ensureConsistentFields(item, getAllFieldsAcrossBranches(branches));
      results.push(item);
    });
  });
  
  // Option to sort by branch for clearer output
  return sortByBranchIfNeeded(results);
}
```

This approach ensures that outputs from complex multi-branch algorithms remain traceable, consistent, and analyzable, which is critical for debugging and maintaining algorithmic correctness.


[
  {
    "discussion_id": "2174959398",
    "pr_number": 130314,
    "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
    "created_at": "2025-06-30T12:28:57+00:00",
    "commented_code": "## `FORK` [esql-fork]\n\n```yaml {applies_to}\nserverless: preview\nstack: preview 9.1.0\n```\n\nThe `FORK` processing command runs multiple execution branches and outputs the\nresults back into a single table.\n\n**Syntax**\n\n```esql\nFORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n```\n\n**Description**\n\nThe `FORK` processing command feeds the input rows into multiple execution\nbranches and outputs the results into a single table, enhanced with a\ndiscriminator column called `_fork`.\n\nThe values of the discriminator column `_fork` are `fork1`, `fork2`, ... and\nthey designate which `FORK` branch the current row is coming from.\nThe values of the `_fork` column always start with `fork1`, which indicates that\nthe row is coming from the first branch.\n\nThe `FORK` branches can output different columns as long as there exists no\ncolumn with the same name and different data types in two different `FORK`\nbranches.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2174959398",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2174959398",
        "commented_code": "@@ -0,0 +1,67 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command runs multiple execution branches and outputs the\n+results back into a single table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, enhanced with a\n+discriminator column called `_fork`.\n+\n+The values of the discriminator column `_fork` are `fork1`, `fork2`, ... and\n+they designate which `FORK` branch the current row is coming from.\n+The values of the `_fork` column always start with `fork1`, which indicates that\n+the row is coming from the first branch.\n+\n+The `FORK` branches can output different columns as long as there exists no\n+column with the same name and different data types in two different `FORK`\n+branches.",
        "comment_created_at": "2025-06-30T12:28:57+00:00",
        "comment_author": "leemthompo",
        "comment_body": "```suggestion\r\n`FORK` branches can output different columns, but columns with the \r\nsame name must have the same data type across all branches.\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2174959864",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2174959398",
        "commented_code": "@@ -0,0 +1,67 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command runs multiple execution branches and outputs the\n+results back into a single table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, enhanced with a\n+discriminator column called `_fork`.\n+\n+The values of the discriminator column `_fork` are `fork1`, `fork2`, ... and\n+they designate which `FORK` branch the current row is coming from.\n+The values of the `_fork` column always start with `fork1`, which indicates that\n+the row is coming from the first branch.\n+\n+The `FORK` branches can output different columns as long as there exists no\n+column with the same name and different data types in two different `FORK`\n+branches.",
        "comment_created_at": "2025-06-30T12:29:11+00:00",
        "comment_author": "leemthompo",
        "comment_body": "I _think_ this is saying the same thing, more concisely",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2175125088",
    "pr_number": 130314,
    "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
    "created_at": "2025-06-30T13:46:38+00:00",
    "commented_code": "## `FORK` [esql-fork]\n\n```yaml {applies_to}\nserverless: preview\nstack: preview 9.1.0\n```\n\nThe `FORK` processing command creates multiple execution branches to operate\non the same input data and combines the results in a single output table.\n\n**Syntax**\n\n```esql\nFORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n```\n\n**Description**\n\nThe `FORK` processing command feeds the input rows into multiple execution\nbranches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2175125088",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2175125088",
        "commented_code": "@@ -0,0 +1,58 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command creates multiple execution branches to operate\n+on the same input data and combines the results in a single output table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.",
        "comment_created_at": "2025-06-30T13:46:38+00:00",
        "comment_author": "leemthompo",
        "comment_body": "```suggestion\r\nThe `FORK` processing command creates multiple execution branches to operate\r\non the same input data and combines the results in a single output table. A discriminator column (`_fork`) is added to identify which branch each row came from.\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2175125515",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2175125088",
        "commented_code": "@@ -0,0 +1,58 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command creates multiple execution branches to operate\n+on the same input data and combines the results in a single output table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.",
        "comment_created_at": "2025-06-30T13:46:50+00:00",
        "comment_author": "leemthompo",
        "comment_body": "keeping same verbiage as opening sentence",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2175137002",
    "pr_number": 130314,
    "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
    "created_at": "2025-06-30T13:52:20+00:00",
    "commented_code": "## `FORK` [esql-fork]\n\n```yaml {applies_to}\nserverless: preview\nstack: preview 9.1.0\n```\n\nThe `FORK` processing command creates multiple execution branches to operate\non the same input data and combines the results in a single output table.\n\n**Syntax**\n\n```esql\nFORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n```\n\n**Description**\n\nThe `FORK` processing command feeds the input rows into multiple execution\nbranches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.\n\nThe values of the discriminator column `_fork` are `fork1`, `fork2`, etc. and\nthey designate which `FORK` branch the current row comes from.\nThe values of the `_fork` column always start with `fork1`, which indicates that\nthe row comes from the first branch.\n\n`FORK` branches can output different columns, but columns with the\nsame name must have the same data type across all branches.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2175137002",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2175137002",
        "commented_code": "@@ -0,0 +1,58 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command creates multiple execution branches to operate\n+on the same input data and combines the results in a single output table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.\n+\n+The values of the discriminator column `_fork` are `fork1`, `fork2`, etc. and\n+they designate which `FORK` branch the current row comes from.\n+The values of the `_fork` column always start with `fork1`, which indicates that\n+the row comes from the first branch.\n+\n+`FORK` branches can output different columns, but columns with the\n+same name must have the same data type across all branches.",
        "comment_created_at": "2025-06-30T13:52:20+00:00",
        "comment_author": "leemthompo",
        "comment_body": "```suggestion\r\n**Branch identification:**\r\n- The `_fork` column identifies each branch with values like `fork1`, `fork2`, `fork3`\r\n- Values correspond to the order branches are defined\r\n- `fork1` always indicates the first branch\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2175138062",
    "pr_number": 130314,
    "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
    "created_at": "2025-06-30T13:52:48+00:00",
    "commented_code": "## `FORK` [esql-fork]\n\n```yaml {applies_to}\nserverless: preview\nstack: preview 9.1.0\n```\n\nThe `FORK` processing command creates multiple execution branches to operate\non the same input data and combines the results in a single output table.\n\n**Syntax**\n\n```esql\nFORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n```\n\n**Description**\n\nThe `FORK` processing command feeds the input rows into multiple execution\nbranches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.\n\nThe values of the discriminator column `_fork` are `fork1`, `fork2`, etc. and\nthey designate which `FORK` branch the current row comes from.\nThe values of the `_fork` column always start with `fork1`, which indicates that\nthe row comes from the first branch.\n\n`FORK` branches can output different columns, but columns with the\nsame name must have the same data type across all branches.\n\nWhen a column does not exist in a `FORK` branch, but it exists in the output of\nother branches, `FORK` will add `null` values to the rows that have missing\ncolumns.\n\n`FORK` preserves the order of the rows from each subset, but it does not\nguarantee that the rows will follow the same order in which the `FORK` branches\nare defined. The rows from the first branch can be interleaved with the rows\nfrom subsequent branches. Use `SORT _fork` after `FORK` if you need to change\nthis behaviour.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2175138062",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130314,
        "pr_file": "docs/reference/query-languages/esql/_snippets/commands/layout/fork.md",
        "discussion_id": "2175138062",
        "commented_code": "@@ -0,0 +1,58 @@\n+## `FORK` [esql-fork]\n+\n+```yaml {applies_to}\n+serverless: preview\n+stack: preview 9.1.0\n+```\n+\n+The `FORK` processing command creates multiple execution branches to operate\n+on the same input data and combines the results in a single output table.\n+\n+**Syntax**\n+\n+```esql\n+FORK ( <processing_commands> ) ( <processing_commands> ) ... ( <processing_commands> )\n+```\n+\n+**Description**\n+\n+The `FORK` processing command feeds the input rows into multiple execution\n+branches and outputs the results into a single table, with a discriminator column (`_fork`) to identify which branch each row came from.\n+\n+The values of the discriminator column `_fork` are `fork1`, `fork2`, etc. and\n+they designate which `FORK` branch the current row comes from.\n+The values of the `_fork` column always start with `fork1`, which indicates that\n+the row comes from the first branch.\n+\n+`FORK` branches can output different columns, but columns with the\n+same name must have the same data type across all branches.\n+\n+When a column does not exist in a `FORK` branch, but it exists in the output of\n+other branches, `FORK` will add `null` values to the rows that have missing\n+columns.\n+\n+`FORK` preserves the order of the rows from each subset, but it does not\n+guarantee that the rows will follow the same order in which the `FORK` branches\n+are defined. The rows from the first branch can be interleaved with the rows\n+from subsequent branches. Use `SORT _fork` after `FORK` if you need to change\n+this behaviour.",
        "comment_created_at": "2025-06-30T13:52:48+00:00",
        "comment_author": "leemthompo",
        "comment_body": "```suggestion\r\n**Column handling:**\r\n- `FORK` branches can output different columns\r\n- Columns with the same name must have the same data type across all branches  \r\n- Missing columns are filled with `null` values\r\n\r\n**Row ordering:**\r\n- `FORK` preserves row order within each branch\r\n- Rows from different branches may be interleaved\r\n- Use `SORT _fork` to group results by branch\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
