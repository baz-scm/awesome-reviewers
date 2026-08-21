---
layout: page
title: Developers
permalink: /developers/
description: Quickstart, versioning and deprecation policy, rate limits, error format, the CLI, and how to run the whole thing locally.
lead: "Everything needed to integrate against the corpus: the four calls that cover most jobs, what may change and when, how to pace yourself, and how to run it locally."
---

## Quickstart

No key, no account, no authentication. Every endpoint is a static file served over HTTPS, GET only.

```bash
# 1. what this interface is, and what may change
curl -sS https://awesomereviewers.com/v1/version.json

# 2. the index: every instruction, with its markdown and JSON URLs
curl -sS https://awesomereviewers.com/v1/index.json | jq '.count'

# 3. one instruction as typed JSON, body included
curl -sS https://awesomereviewers.com/v1/instructions/<slug>.json

# 4. a whole domain in one request, as markdown you can paste into a prompt
curl -sS https://awesomereviewers.com/raw/bundles/llm-infra.md
```

Machine-readable descriptions: [/openapi.json](/openapi.json) (OpenAPI 3.1),
[/.well-known/api-catalog](/.well-known/api-catalog) (RFC 9727),
[/agents.md](/agents.md) (when to use this, and what to call), and the full
endpoint table on the [API page](/api/).

## Authentication

There is none, and there is nothing to authenticate: the corpus is public, read-only and identical
for every client. No key is issued, no `Authorization` header is read, and no endpoint accepts a
method other than GET. If you are being asked for a credential, you are not talking to this site.

## Versioning

The interface is versioned in the URL path. `/v1/**` keeps its response shapes; a breaking change
ships as `/v2/**` beside it rather than replacing anything in place. The unversioned paths
(`/raw/**`, `/llms.txt`, `/openapi.json`) predate the prefix and are maintained as aliases of the v1
shapes.

Two different versions travel with a response, and they answer different questions:

| Field | Where | Answers |
| --- | --- | --- |
| `api_version` | `/v1/version.json`, `x-api-version` in the OpenAPI document | what shape the response comes in |
| `corpus_version` | `/v1/version.json`, `info.version` in the OpenAPI document | how fresh the content is (the newest review comment in the corpus) |

Compatible changes ship without notice: a new endpoint, a new optional field, a new domain, topic or
language value, new instructions and new dates on existing ones. Removing or renaming a field,
changing a field's type, removing an endpoint or changing what an existing field means are breaking
changes and do not happen inside `/v1/**`.

## Deprecation

A retiring endpoint says so in its own responses, so a client finds out by calling rather than by
reading a changelog:

- `Deprecation` ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745)) — the date the deprecation took
  effect.
- `Sunset` ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)) — the date it stops answering, never
  less than 180 days after the deprecation date.
- `Link: <…>; rel="deprecation"` — where to read what replaced it.

Live deprecations are listed in the `deprecations` field of
[/v1/version.json](/v1/version.json), which is empty while there are none. That field, not this page,
is the thing to poll.

## Rate limits

The static origin does not throttle. Where the optional edge tier is deployed in front of it, the
quota is 600 requests per 60 seconds per client IP address, advertised on every response in the
[RateLimit header fields](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers):

```http
RateLimit-Policy: "default";q=600;w=60
RateLimit: "default";r=573;t=41
```

Over the quota you get `429` with `Retry-After` in seconds and an RFC 9457 problem body. Two habits
keep any client well inside it: fetch a domain bundle instead of every instruction in it, and diff
the `updated` field from the index against your last run instead of refetching the corpus.

## Errors

Errors are [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem details with two extension
members — `code`, stable for matching, and `resolution`, saying what to do next. Every type is also
published as a document, so you can read the shape without provoking it:
[/v1/errors/index.json](/v1/errors/index.json). A missing path returns a real `404`, whose body is
also published as markdown at [/404.md](/404.md).

Because the origin is a static host, a browser asking for HTML gets the
[404 page](/404.html) rather than a JSON body; it carries the same problem details in a
`<script type="application/problem+json">` element. The edge tier returns real
`application/problem+json` to a client that asks for JSON.

## Markdown negotiation

Every page that is built from markdown advertises that markdown with
`<link rel="alternate" type="text/markdown">`, and the mapping is mechanical, so a client can rewrite
a URL instead of parsing HTML: `/reviewers/<slug>/` → `/raw/<slug>.md`, `/domains/<domain>/` →
`/raw/bundles/<domain>.md`, `/developers/` → `/raw/developers.md`, `/` → `/raw/site.md`. Behind the
edge tier the same URLs answer `Accept: text/markdown` directly, with `Vary: Accept` so caches keep
the variants apart.

## CLI

A single-file CLI over these endpoints, Python 3.9+, no dependencies:

```bash
curl -sSO https://awesomereviewers.com/cli/awesome-reviewers.py
chmod +x awesome-reviewers.py

./awesome-reviewers.py domains                        # every domain, with counts
./awesome-reviewers.py search "kv cache" --limit 5    # search titles and descriptions
./awesome-reviewers.py get <slug>                     # one instruction as markdown
./awesome-reviewers.py bundle llm-infra -o rubric.md  # a whole domain in one file
./awesome-reviewers.py sync ./corpus --domain security  # mirror a domain to disk
```

`sync` writes only what changed, using the `updated` date of each instruction, so it is safe on a
schedule. The source is in
[`cli/`](https://github.com/baz-scm/awesome-reviewers/tree/main/cli) — it is not published to a
package registry yet, so there is nothing to `npm install` or `pip install` today.

## Run it locally

The whole site, including every endpoint above, builds from the corpus with the standard library and
Jekyll. This is the sandbox: no key, no service to sign up for, and nothing that talks to a network
at build time.

```bash
git clone https://github.com/baz-scm/awesome-reviewers
cd awesome-reviewers
python build_data.py                  # regenerate every derived artifact
bundle install && bundle exec jekyll serve
```

To exercise the negotiation and error behaviour that needs a real server, run the edge worker in
front of a local or remote origin:

```bash
cd edge && npx wrangler dev          # then curl -H 'Accept: text/markdown' localhost:8787/
```

Tests for both halves:

```bash
python -m unittest discover -s tests -t .   # the machine interface
node --test tests/worker.test.mjs           # the edge worker
```

## Support

- Bugs, corrections and repository requests: [GitHub issues](https://github.com/baz-scm/awesome-reviewers/issues).
- Anything about the corpus itself: the [method](/methodology/) page explains how instructions are
  derived, dated and classified.
- Everything else: [contact](/contact/).

Apache-2.0. The instructions are distilled from public review discussions and are not official
guidance from the projects they came out of.
