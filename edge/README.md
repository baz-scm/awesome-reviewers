# Edge worker (optional)

`worker.js` is a Cloudflare Worker that sits in front of the GitHub Pages origin. The site is fully
functional without it; it is not part of the Jekyll build and `_config.yml` excludes this directory.

It exists because two things an agent expects are impossible on static hosting alone:

| Behaviour | GitHub Pages | With this worker |
| --- | --- | --- |
| `Accept: text/markdown` on `/reviewers/<slug>/` | `text/html` | `text/markdown`, `Vary: Accept`, `Content-Location: /raw/<slug>.md` |
| `Vary: Accept` on negotiable responses | absent | present |
| `Link: rel="alternate"` to the markdown twin | absent (only the in-page `<link>`) | present |
| Error responses for a JSON client | the HTML 404 page | RFC 9457 `application/problem+json` |
| Unsatisfiable `Accept` | `200` HTML | `406` |

Everything else is passed through untouched, including `/raw/**`, `/llms.txt`, `/openapi.json` and
`/assets/**`.

## What it negotiates

Only pages that have a markdown twin, because only those have markdown to serve:

| Page | Markdown |
| --- | --- |
| `/reviewers/<slug>/` | `/raw/<slug>.md` |
| `/domains/<domain>/` | `/raw/bundles/<domain>.md` |
| `/` | `/llms.txt` |

Accept parsing follows RFC 9110 §12.5.1: q-values are honoured, `q=0` is an explicit rejection, a
more specific media range beats a less specific one regardless of q, and ties are broken by the
client's own ordering. The behaviour is the one described at
[acceptmarkdown.com/start](https://acceptmarkdown.com/start).

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

curl -sI https://awesomereviewers.com/reviewers/<slug>/
# content-type: text/html; charset=utf-8
# vary: Accept
# link: </raw/<slug>.md>; rel="alternate"; type="text/markdown"

curl -s -H "Accept: application/json" https://awesomereviewers.com/nope
# {"type": "https://awesomereviewers.com/api/#error-not-found", "status": 404, ...}

curl -sI -H "Accept: application/pdf" https://awesomereviewers.com/reviewers/<slug>/
# HTTP/2 406
```

## Tests

`node --test tests/worker.test.mjs` from the repository root covers the Accept parsing, the negotiation, the
markdown mapping and the problem responses, and asserts the worker's error catalogue matches the
one `build_data.py` publishes in `openapi.json`.
