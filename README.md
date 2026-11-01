# Awesome Verification

A catalog of verification methods found in public repository source and configuration.
Each record includes named tools, recorded commands, evidence state and source links pinned
to the inspected commit.

The project reuses the Awesome Reviewers website and its Jekyll publication pipeline.
The existing domain remains [awesomereviewers.com](https://awesomereviewers.com).
The legacy review-discussion instruction collection is preserved at its existing URLs.

## What a record establishes

| Evidence state | Meaning |
| --- | --- |
| Configured in CI | A workflow invokes the check, subject to its recorded conditions. |
| Configured locally | A command or configuration enables the check; CI invocation was not established. |
| Implementation present | Source code implements the check; invocation was not established. |

A source record does not establish a successful run, unconditional execution, or a required
merge check. Coverage is bounded and published for every repository. A missing detection
does not establish that a method is absent.

## Data and publication

`_verification/<owner>--<repo>.json` is the source for repository scan manifests.
The [manifest contract](_verification/README.md) describes the fields and evidence rules.

`build_verification.py` validates all manifests before generating:

| Output | Contents |
| --- | --- |
| `_data/verification.json` | Catalog and source coverage for the site. |
| `methods/<id>/index.html` | Method detail page. |
| `raw/verification/index.json` | Full catalog with method records and source coverage. |
| `raw/verification/<id>.json` | One method record with source evidence. |
| `raw/verification/<id>.md` | One method record as plain Markdown. |
| `raw/verification/repositories/<owner>--<repo>.json` | One complete source scan manifest. |
| `raw/verification/site.md` | Catalog overview. |
| `raw/verification/llms.txt` | Text index of method records. |
| `raw/verification/openapi.json` | OpenAPI 3.1 description. |

`build_data.py` builds the legacy corpus first, then calls the verification generator.
The new generator never reads `_reviewers/`, and the build never executes commands
from inspected repositories. Source collection is separate from publication.

The main page filters methods by technique, tool, repository, category and evidence state.
The Sources page exposes commit identifiers and scan limits.
The [Verification API](https://awesomereviewers.com/verification-api/) documents raw access.

## Development

```bash
python build_data.py
bundle install
bundle exec jekyll serve
```

For only the verification data and generated pages:

```bash
python build_verification.py
```

Both Python builders use only the standard library. The existing GitHub Actions workflow
runs the build and tests before Jekyll publishes GitHub Pages.

```bash
python -m unittest discover -s tests -t .
node --test tests/worker.test.mjs
```

The catalog tests check rejection of unpinned and mismatched evidence, scan-state claims,
legacy-data separation and removal of stale generated records.

## Legacy collection

The original instruction records remain in `_reviewers/` as Markdown and sibling
review-discussion JSON files. They retain the original public paths:

| Resource | Path |
| --- | --- |
| Instruction pages | `/reviewers/<slug>/` |
| Domain pages | `/domains/<domain>/` |
| Instruction Markdown | `/raw/<slug>.md` |
| Domain bundles | `/raw/bundles/<domain>.md` |
| Instruction index | `/raw/index.json` |
| Source discussions | `/<slug>.json` |
| Original API reference | `/api/` |
| Original API description | `/openapi.json` |
| Original text index | `/llms.txt` |

Legacy instructions are derived from review conversations. They are not reclassified
as evidence that a repository uses a verification technique.

## Contributing

Submit corrected scan manifests with exact commit-pinned evidence, or open an issue with
the record and source lines that need checking. Existing instructions can still be corrected
through their files in `_reviewers/`.

Maintained by [Baz](https://baz.ai). Apache-2.0. The catalog describes public source snapshots;
it is not official guidance or an execution attestation from the represented projects.

