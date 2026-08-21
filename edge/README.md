# Edge worker (optional)

`worker.js` is a Cloudflare Worker that sits in front of the GitHub Pages origin. The site is fully
functional without it; it is not part of the Jekyll build and `_config.yml` excludes this directory.

It exists because several things an agent expects are impossible on static hosting alone:

| Behaviour | GitHub Pages | With this worker |
| --- | --- | --- |
| `Accept: text/markdown` on `/reviewers/<slug>/` | `text/html` | `text/markdown`, `Vary: Accept`, `Content-Location: /raw/<slug>.md` |
| `Vary: Accept` on negotiable responses | absent | present |
| `Link: rel="alternate"` to the markdown twin | absent (only the in-page `<link>`) | present |
| Error responses for a JSON client | the HTML 404 page | RFC 9457 `application/problem+json` |
| Error responses for a markdown client | the HTML 404 page | `404` with the `/404.md` recovery body |
| Unsatisfiable `Accept` | `200` HTML | `406` |
| `RateLimit-Policy` on every response | absent | present |
| Quota enforcement | none | `429` with `Retry-After` and `RateLimit`, when the limiter is bound |
| `Deprecation` / `Sunset` on a retiring endpoint | impossible | present, from `DEPRECATIONS` |
| `/.well-known/api-catalog` media type | extensionless, so untyped | `application/linkset+json;profile="…rfc9727"` |
| `Link: rel="api-catalog"` | absent | present on every response |

Everything else is passed through untouched, including `/raw/**`, `/v1/**`, `/llms.txt`,
`/openapi.json` and `/assets/**`.

## What it negotiates

Only pages that have a markdown twin, because only those have markdown to serve:

| Page | Markdown |
| --- | --- |
| `/reviewers/<slug>/` | `/raw/<slug>.md` |
| `/domains/<domain>/` | `/raw/bundles/<domain>.md` |
| `/developers/`, `/about/`, `/contact/`, `/privacy/` | `/raw/<page>.md` |
| `/` | `/raw/site.md` |
| anything missing | `/404.md`, returned with a `404` status |

Accept parsing follows RFC 9110 §12.5.1: q-values are honoured, `q=0` is an explicit rejection, a
more specific media range beats a less specific one regardless of q, and ties are broken by the
client's own ordering. The behaviour is the one described at
[acceptmarkdown.com/start](https://acceptmarkdown.com/start).

## Rate limits

`RATE_LIMIT` in `worker.js` mirrors `RATE_LIMIT_*` in `build_data.py`, which publishes the same
numbers in `/v1/version.json` and on `/api/#rate-limits`. Every response carries

```http
RateLimit-Policy: "default";q=600;w=60
```

Enforcement needs the `RATE_LIMITER` binding in `wrangler.jsonc`. With it, a client over quota gets
`429` with `Retry-After: 60`, `RateLimit: "default";r=0;t=60` and an RFC 9457 body. The binding
reports only whether a request is inside the quota, so the worker never claims a remaining count it
cannot know: `r=0` appears on the 429 and nowhere else.

## Deprecations

`DEPRECATIONS` in `worker.js` mirrors the `deprecations` field of `/v1/version.json` — empty while
nothing is deprecated. Adding an entry makes the matching paths answer with `Deprecation` (RFC 9745,
a structured-field date), `Sunset` (RFC 8594, an HTTP date) and `Link: rel="deprecation"`. Keep the
two lists in step: the field is what clients poll, the worker is what they feel.

## Deploying

Requires a Cloudflare account with `awesomereviewers.com` as a zone, DNS proxied through Cloudflare
with GitHub Pages as the origin, and a Wrangler login. None of that is needed to develop the site.

```bash
cd edge
npx wrangler deploy
```

Set `ORIGIN` in `wrangler.jsonc` only if a subrequest to the worker's own route comes back to the
worker instead of reaching the origin.

Add a Cache Rule that keys on `Accept` (normalised to `html` or `md`) before serving production
traffic — `Vary: Accept` alone is not enough on every CDN, and without it the first variant cached
is served to everyone. See [acceptmarkdown.com/guides/caching-cdn](https://acceptmarkdown.com/guides/caching-cdn).

## Verifying

```bash
curl -sI -H "Accept: text/markdown" https://awesomereviewers.com/reviewers/<slug>/
# content-type: text/markdown; charset=utf-8
# vary: Accept
# ratelimit-policy: "default";q=600;w=60

curl -sI https://awesomereviewers.com/reviewers/<slug>/
# content-type: text/html; charset=utf-8
# vary: Accept
# link: </raw/<slug>.md>; rel="alternate"; type="text/markdown", </.well-known/api-catalog>; rel="api-catalog"

curl -s -H "Accept: application/json" https://awesomereviewers.com/nope
# {"type": "https://awesomereviewers.com/api/#error-not-found", "status": 404, ...}

curl -si -H "Accept: text/markdown" https://awesomereviewers.com/nope | head -5
# HTTP/2 404 … content-type: text/markdown; charset=utf-8 … "# 404 Not Found"

curl -sI -H "Accept: application/pdf" https://awesomereviewers.com/reviewers/<slug>/
# HTTP/2 406

curl -sI https://awesomereviewers.com/.well-known/api-catalog
# content-type: application/linkset+json;profile="https://www.rfc-editor.org/info/rfc9727"
```

## Tests

`node --test tests/worker.test.mjs` from the repository root covers the Accept parsing, the
negotiation, the markdown mapping, the problem responses, the rate-limit headers and the deprecation
headers, and asserts the worker's error catalogue and quota match the ones `build_data.py` publishes
in `openapi.json`.
