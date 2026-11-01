# Verification source manifests

One JSON file represents one inspected repository snapshot. Name it
`<owner>--<repository>.json`. The collector replaces that snapshot when rescanning.
The website never treats legacy `_reviewers/` instructions as verification records.

## Manifest contract

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`. |
| `repository` | GitHub `owner/repository`. |
| `commit_sha` | Full 40-character commit identifier resolved before files are fetched. |
| `default_branch` | Default branch observed during the scan. |
| `scanned_at` | ISO timestamp with timezone, normalized to UTC by the build. |
| `coverage` | `tree_complete`, `files_considered`, `candidate_files`, `files_fetched`, `files_skipped` and `limitations`. |
| `methods` | Method records. An empty array is a valid scan result and remains visible in source coverage. |

Each method has `id`, `method`, `title`, `category`, `summary`, `tools`,
`commands`, `status` and a nonempty `evidence` array. IDs equal the lowercase
`owner--repository--` prefix followed by the exact method identifier, for example
`example--project--property_based_testing`.

Each evidence item has `path`, `start_line`, `end_line`, `excerpt`, `url`
and `kind`. The URL must point to the same repository, exact commit, path and
line range. Optional `conditions`, `working_directory` and `environment` are
scoped to that evidence item, because different jobs can invoke the same method
under different constraints.

## Evidence states

| Value | Claim supported |
| --- | --- |
| `ci_configured` | A CI definition invokes the check, subject to the recorded conditions. |
| `configured` | A command or configuration enables the check; CI invocation was not established. |
| `implemented` | Code implements the check; its invocation was not established. |

A method's status must have a matching evidence item. These states never imply
a passed run, unconditional execution or a required merge check. Dependency names,
prose mentions and agent instructions alone do not establish usage.

## Building

`python build_verification.py` validates all manifests before replacing the
generated catalog, method pages and files below `raw/verification/`.
`python build_data.py` builds both the legacy instruction collection and this
verification catalog for Jekyll. Generated outputs are ignored by git.

Source collection is read-only. Commands found in a repository are recorded as
text and are never executed by the website build.
