/**
 * Optional edge worker for awesomereviewers.com.
 *
 * The site is static files on GitHub Pages, which cannot vary a response on the
 * request's `Accept` header, cannot set a header per path, and cannot serve
 * anything but its HTML 404 page. Put this worker in front of that origin and
 * five things become true that a static host cannot do on its own:
 *
 *   1. `Accept: text/markdown` on a page returns the markdown that page is built
 *      from, with `Vary: Accept` so caches key on it.
 *      See https://acceptmarkdown.com/start.
 *   2. Error responses are RFC 9457 problem details when the client asks for
 *      JSON, and the markdown recovery body when it asks for markdown, instead
 *      of an HTML page an agent has to scrape.
 *   3. Responses advertise the quota in the RateLimit header fields, and — where
 *      a rate limiter is bound to the worker — enforce it with a 429 carrying
 *      `Retry-After`.
 *   4. A retiring endpoint carries `Deprecation` (RFC 9745), `Sunset`
 *      (RFC 8594) and a `Link` with `rel="deprecation"`.
 *   5. `/.well-known/api-catalog` is served with its RFC 9727 media type, and
 *      every response links it with `rel="api-catalog"`.
 *
 * Nothing else changes: every other request is passed through to the origin
 * untouched. The worker is not part of the Jekyll build and the site is fully
 * functional without it.
 *
 * Deploy notes are in edge/README.md.
 */

const SITE_URL = 'https://awesomereviewers.com';
const API_DOCS_URL = `${SITE_URL}/api/`;

/** Mirrors RATE_LIMIT_* in build_data.py; the tests assert they agree. */
export const RATE_LIMIT = { name: 'default', quota: 600, window: 60 };
export const RATE_LIMIT_POLICY = `"${RATE_LIMIT.name}";q=${RATE_LIMIT.quota};w=${RATE_LIMIT.window}`;

export const CATALOG_PATH = '/.well-known/api-catalog';
const CATALOG_TYPE =
  'application/linkset+json;profile="https://www.rfc-editor.org/info/rfc9727"';
const CATALOG_LINK = `<${CATALOG_PATH}>; rel="api-catalog"`;

/** The markdown recovery body the origin publishes; see build_data.py. */
const NOT_FOUND_MARKDOWN_PATH = '/404.md';

/** Mirrors PROBLEM_TYPES in build_data.py; the tests assert they agree. */
export const PROBLEMS = {
  not_found: {
    code: 'not_found',
    status: 404,
    title: 'Resource not found',
    detail: 'Nothing is published at this path.',
    resolution:
      `Every published path is listed in ${SITE_URL}/raw/index.json and ` +
      `${SITE_URL}/llms.txt. Look the slug up there and retry.`,
  },
  not_acceptable: {
    code: 'not_acceptable',
    status: 406,
    title: 'No acceptable representation',
    detail: 'The Accept header rules out every representation of this resource.',
    resolution:
      'Send Accept: text/markdown for markdown, text/html for the rendered page, ' +
      'application/json for the JSON endpoints, or */* to take whatever is served.',
  },
  rate_limited: {
    code: 'rate_limited',
    status: 429,
    title: 'Too many requests',
    detail: 'The quota for this client is exhausted.',
    resolution:
      'Wait for the number of seconds in Retry-After, then retry. The quota is ' +
      `${RATE_LIMIT.quota} requests per ${RATE_LIMIT.window} seconds and is reported on ` +
      'every response in the RateLimit-Policy and RateLimit header fields. To read the ' +
      'whole corpus, fetch one domain bundle instead of every instruction: ' +
      `${SITE_URL}/raw/bundles/<domain>.md.`,
  },
};

/**
 * Endpoints being retired, mirroring DEPRECATIONS in build_data.py and the
 * `deprecations` field of /v1/version.json. Empty while nothing is deprecated,
 * which is the current state; an entry looks like
 *
 *   { path: '/raw/index.json', deprecation: '2026-09-01', sunset: '2027-03-01',
 *     successor: '/v1/index.json' }
 */
export const DEPRECATIONS = [];

export function problemTypeUrl(code) {
  return `${API_DOCS_URL}#error-${code.replace(/_/g, '-')}`;
}

/**
 * Parse an Accept header into entries, preserving client order.
 * RFC 9110 §12.5.1.
 */
export function parseAccept(header) {
  return header
    .split(',')
    .map((raw) => {
      const parts = raw.trim().split(';').map((s) => s.trim());
      const type = parts[0].toLowerCase();
      if (!type) return null;
      let q = 1;
      for (const param of parts.slice(1)) {
        const [name, value] = param.split('=').map((s) => s.trim());
        if (name === 'q') {
          const parsed = Number(value);
          if (!Number.isNaN(parsed)) q = Math.max(0, Math.min(1, parsed));
        }
      }
      const specificity = type === '*/*' ? 0 : type.endsWith('/*') ? 1 : 2;
      return { type, q, specificity };
    })
    .filter((entry) => entry !== null);
}

function matches(entry, candidate) {
  if (entry.type === '*/*') return true;
  if (entry.type.endsWith('/*')) return candidate.startsWith(entry.type.slice(0, -1));
  return entry.type === candidate;
}

/**
 * Pick the representation to serve, or null if the client rejected all of them.
 *
 * A more specific media range overrides a less specific one regardless of q, so
 * `text/html;q=0, *\/*` does not smuggle HTML back in through the wildcard.
 * Across candidates the highest q wins, ties broken by the client's own order.
 */
export function preferredType(header, produces) {
  if (!header) return produces[0] ?? null;
  const entries = parseAccept(header);
  if (entries.length === 0) return produces[0] ?? null;

  let bestType = null;
  let bestQ = -1;
  let bestPosition = Infinity;

  for (const candidate of produces) {
    let matched = null;
    let matchedPosition = Infinity;
    for (let index = 0; index < entries.length; index++) {
      const entry = entries[index];
      if (!matches(entry, candidate)) continue;
      if (
        matched === null ||
        entry.specificity > matched.specificity ||
        (entry.specificity === matched.specificity && index < matchedPosition)
      ) {
        matched = entry;
        matchedPosition = index;
      }
    }
    if (matched === null || matched.q <= 0) continue;

    if (matched.q > bestQ || (matched.q === bestQ && matchedPosition < bestPosition)) {
      bestQ = matched.q;
      bestPosition = matchedPosition;
      bestType = candidate;
    }
  }

  return bestType;
}

export function appendVaryAccept(headers) {
  const existing = headers.get('vary');
  if (!existing) {
    headers.set('Vary', 'Accept');
    return;
  }
  const tokens = existing.split(',').map((token) => token.trim().toLowerCase());
  if (!tokens.includes('accept') && !tokens.includes('*')) {
    headers.set('Vary', `${existing}, Accept`);
  }
}

function appendLink(headers, link) {
  const existing = headers.get('link');
  if (existing?.includes(link)) return;
  headers.set('Link', existing ? `${existing}, ${link}` : link);
}

/** Every response says what the quota is, whether or not one is enforced. */
function annotate(headers, pathname) {
  headers.set('RateLimit-Policy', RATE_LIMIT_POLICY);
  appendLink(headers, CATALOG_LINK);
  for (const [name, value] of Object.entries(deprecationHeaders(pathname))) {
    headers.set(name, value);
  }
  return headers;
}

/**
 * `Deprecation`, `Sunset` and a `Link` for a path being retired, or {} for the
 * paths that are not — which is all of them today.
 *
 * `Deprecation` is a structured-field date (RFC 9745 §2): an `@` sigil and a
 * Unix timestamp. `Sunset` is an HTTP date (RFC 8594).
 */
export function deprecationHeaders(pathname, deprecations = DEPRECATIONS) {
  const entry = deprecations.find(
    (candidate) => pathname === candidate.path || pathname.startsWith(candidate.path),
  );
  if (!entry) return {};

  const headers = {
    Deprecation: `@${Math.floor(Date.parse(`${entry.deprecation}T00:00:00Z`) / 1000)}`,
    Sunset: new Date(`${entry.sunset}T00:00:00Z`).toUTCString(),
  };
  const target = entry.successor ?? `${API_DOCS_URL}#versioning`;
  headers.Link = `<${target}>; rel="deprecation"`;
  return headers;
}

/**
 * The markdown this page is built from, or null when it has no twin.
 *
 *   /reviewers/<slug>/  -> /raw/<slug>.md
 *   /domains/<domain>/  -> /raw/bundles/<domain>.md
 *   /developers/ etc.   -> /raw/<page>.md
 *   /                   -> /raw/site.md
 */
export const PROSE_PAGES = ['developers', 'about', 'contact', 'privacy'];

export function markdownTwin(pathname) {
  const clean = pathname.replace(/\/+$/, '');
  if (clean === '') return '/raw/site.md';
  const reviewer = clean.match(/^\/reviewers\/([a-z0-9-]+)$/);
  if (reviewer) return `/raw/${reviewer[1]}.md`;
  const domain = clean.match(/^\/domains\/([a-z0-9-]+)$/);
  if (domain) return `/raw/bundles/${domain[1]}.md`;
  const page = clean.match(/^\/([a-z0-9-]+)$/);
  if (page && PROSE_PAGES.includes(page[1])) return `/raw/${page[1]}.md`;
  return null;
}

/** Paths the worker never negotiates: they already are the machine interface. */
export function isPassThrough(pathname) {
  if (pathname === CATALOG_PATH) return false;
  return /\.[a-z0-9]+$/i.test(pathname) || pathname.startsWith('/assets/');
}

function problemResponse(code, instance, extra = {}) {
  const problem = PROBLEMS[code];
  const body = {
    type: problemTypeUrl(code),
    title: problem.title,
    status: problem.status,
    detail: problem.detail,
    instance,
    code: problem.code,
    resolution: problem.resolution,
    ...extra,
  };
  const response = new Response(`${JSON.stringify(body, null, 2)}\n`, {
    status: problem.status,
    headers: {
      'Content-Type': 'application/problem+json; charset=utf-8',
      'Content-Language': 'en',
    },
  });
  appendVaryAccept(response.headers);
  annotate(response.headers, instance);
  return response;
}

/** True when the client would rather have JSON than HTML. */
function wantsJson(accept) {
  if (!accept) return false;
  const chosen = preferredType(accept, ['text/html', 'application/problem+json', 'application/json']);
  return chosen === 'application/problem+json' || chosen === 'application/json';
}

/** True when the client would rather have markdown than HTML or JSON. */
function wantsMarkdown(accept) {
  if (!accept) return false;
  return (
    preferredType(accept, ['text/html', 'application/json', 'text/markdown']) === 'text/markdown'
  );
}

/**
 * The 404 an agent can act on: problem details for a JSON client, the published
 * markdown recovery body for a markdown one, the HTML page for everyone else.
 */
async function notFound(request, origin, url, accept) {
  if (wantsJson(accept)) return problemResponse('not_found', url.pathname);

  if (wantsMarkdown(accept)) {
    const recoveryUrl = new URL(url);
    recoveryUrl.pathname = NOT_FOUND_MARKDOWN_PATH;
    recoveryUrl.search = '';
    const recovery = await origin(new Request(recoveryUrl.toString(), request));
    if (recovery.status === 200) {
      const response = new Response(recovery.body, { status: 404, headers: recovery.headers });
      response.headers.set('Content-Type', 'text/markdown; charset=utf-8');
      response.headers.set('Content-Location', NOT_FOUND_MARKDOWN_PATH);
      appendVaryAccept(response.headers);
      annotate(response.headers, url.pathname);
      return response;
    }
  }
  return null;
}

/**
 * Ask the bound rate limiter whether this client may proceed.
 *
 * Cloudflare's rate-limiting binding reports only whether the request is inside
 * the quota, so the 429 states the one count it can state honestly: none left,
 * and the window to wait out.
 */
async function rateLimited(request, env, url) {
  const limiter = env?.RATE_LIMITER;
  if (!limiter?.limit) return null;

  const key =
    request.headers.get('cf-connecting-ip') ??
    request.headers.get('x-forwarded-for') ??
    'anonymous';
  const { success } = await limiter.limit({ key });
  if (success) return null;

  const accept = request.headers.get('accept');
  const response = wantsJson(accept)
    ? problemResponse('rate_limited', url.pathname, { violated_policies: [RATE_LIMIT.name] })
    : new Response(
        `429 Too Many Requests\n\n${PROBLEMS.rate_limited.resolution}\n${problemTypeUrl('rate_limited')}\n`,
        { status: 429, headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
      );
  response.headers.set('Retry-After', String(RATE_LIMIT.window));
  response.headers.set('RateLimit', `"${RATE_LIMIT.name}";r=0;t=${RATE_LIMIT.window}`);
  annotate(response.headers, url.pathname);
  return response;
}

export async function handle(request, origin, env = {}) {
  const url = new URL(request.url);
  const accept = request.headers.get('accept');

  const throttled = await rateLimited(request, env, url);
  if (throttled) return throttled;

  // The API catalogue is a linkset, and static hosting serves an extensionless
  // file without a usable type. Give it the one RFC 9727 asks for.
  if (url.pathname === CATALOG_PATH) {
    const catalog = await origin(request);
    if (catalog.status >= 400) {
      return (await notFound(request, origin, url, accept)) ?? annotateResponse(catalog, url);
    }
    const response = new Response(catalog.body, catalog);
    response.headers.set('Content-Type', CATALOG_TYPE);
    annotate(response.headers, url.pathname);
    return response;
  }

  if (isPassThrough(url.pathname)) {
    const passed = await origin(request);
    if (passed.status >= 400) {
      const recovered = await notFound(request, origin, url, accept);
      if (recovered) return recovered;
    }
    return annotateResponse(passed, url);
  }

  const twin = markdownTwin(url.pathname);
  const produces = twin ? ['text/html', 'text/markdown'] : ['text/html'];

  if (preferredType(accept, produces) === 'text/markdown') {
    const markdownUrl = new URL(url);
    markdownUrl.pathname = twin;
    const markdown = await origin(new Request(markdownUrl.toString(), request));
    if (markdown.status === 200) {
      const response = new Response(markdown.body, markdown);
      response.headers.set('Content-Type', 'text/markdown; charset=utf-8');
      response.headers.set('Content-Location', twin);
      appendVaryAccept(response.headers);
      annotate(response.headers, url.pathname);
      return response;
    }
    // No markdown after all: fall through and let the HTML path decide.
  }

  const upstream = await origin(request);

  // Whether the resource exists is settled before whether it is acceptable: a
  // client that asked for JSON and guessed a slug wants 404, not 406.
  if (upstream.status >= 400) {
    const recovered = await notFound(request, origin, url, accept);
    if (recovered) return recovered;
    const response = new Response(upstream.body, upstream);
    appendVaryAccept(response.headers);
    annotate(response.headers, url.pathname);
    return response;
  }

  // The client rejected every representation this path has.
  if (preferredType(accept, ['text/html']) === null) {
    if (wantsJson(accept)) {
      return problemResponse('not_acceptable', url.pathname, { produces });
    }
    const response = new Response(
      `406 Not Acceptable\n\nAvailable: ${produces.join(', ')}\n${problemTypeUrl('not_acceptable')}\n`,
      {
        status: 406,
        headers: { 'Content-Type': 'text/plain; charset=utf-8', Vary: 'Accept' },
      },
    );
    annotate(response.headers, url.pathname);
    return response;
  }

  const response = new Response(upstream.body, upstream);
  appendVaryAccept(response.headers);
  annotate(response.headers, url.pathname);
  if (twin && response.headers.get('content-type')?.includes('text/html')) {
    appendLink(response.headers, `<${twin}>; rel="alternate"; type="text/markdown"`);
  }
  return response;
}

/** Copy an origin response through, adding only the headers the worker owns. */
function annotateResponse(upstream, url) {
  const response = new Response(upstream.body, upstream);
  annotate(response.headers, url.pathname);
  return response;
}

export default {
  /**
   * `env.ORIGIN` overrides where the origin fetch goes, for the case where a
   * subrequest to the worker's own route would come back to the worker. Left
   * unset, requests go to the zone's origin as usual. `env.RATE_LIMITER` is an
   * optional rate-limiting binding; without it the worker advertises the quota
   * but enforces nothing.
   */
  fetch(request, env = {}) {
    return handle(
      request,
      (upstream) => {
        if (!env.ORIGIN) return fetch(upstream);
        const target = new URL(upstream.url);
        const origin = new URL(env.ORIGIN);
        target.protocol = origin.protocol;
        target.host = origin.host;
        return fetch(new Request(target.toString(), upstream));
      },
      env,
    );
  },
};
