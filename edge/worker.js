/**
 * Optional edge worker for awesomereviewers.com.
 *
 * The site is static files on GitHub Pages, which cannot vary a response on the
 * request's `Accept` header and cannot serve anything but its HTML 404 page.
 * Put this worker in front of that origin and two things become true that a
 * static host cannot do on its own:
 *
 *   1. `Accept: text/markdown` on an instruction or domain page returns the
 *      markdown that page is built from, with `Vary: Accept` so caches key on
 *      it. See https://acceptmarkdown.com/start.
 *   2. Error responses are RFC 9457 problem details when the client asks for
 *      JSON, instead of an HTML page an agent has to scrape.
 *
 * Nothing else changes: every other request is passed through to the origin
 * untouched. The worker is not part of the Jekyll build and the site is fully
 * functional without it.
 *
 * Deploy notes are in edge/README.md.
 */

const SITE_URL = 'https://awesomereviewers.com';
const API_DOCS_URL = `${SITE_URL}/api/`;

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
};

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

/**
 * The markdown this page is built from, or null when it has no twin.
 *
 *   /reviewers/<slug>/  -> /raw/<slug>.md
 *   /domains/<domain>/  -> /raw/bundles/<domain>.md
 *   /                   -> /raw/site.md
 */
export function markdownTwin(pathname) {
  const clean = pathname.replace(/\/+$/, '');
  if (clean === '') return '/raw/site.md';
  const reviewer = clean.match(/^\/reviewers\/([a-z0-9-]+)$/);
  if (reviewer) return `/raw/${reviewer[1]}.md`;
  const domain = clean.match(/^\/domains\/([a-z0-9-]+)$/);
  if (domain) return `/raw/bundles/${domain[1]}.md`;
  return null;
}

/** Paths the worker never negotiates: they already are the machine interface. */
export function isPassThrough(pathname) {
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
  return response;
}

/** True when the client would rather have JSON than HTML. */
function wantsJson(accept) {
  if (!accept) return false;
  const chosen = preferredType(accept, ['text/html', 'application/problem+json', 'application/json']);
  return chosen === 'application/problem+json' || chosen === 'application/json';
}

export async function handle(request, origin) {
  const url = new URL(request.url);
  const accept = request.headers.get('accept');

  if (isPassThrough(url.pathname)) {
    const passed = await origin(request);
    return passed.status >= 400 && wantsJson(accept)
      ? problemResponse('not_found', url.pathname)
      : passed;
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
      return response;
    }
    // No markdown after all: fall through and let the HTML path decide.
  }

  const upstream = await origin(request);

  // Whether the resource exists is settled before whether it is acceptable: a
  // client that asked for JSON and guessed a slug wants 404, not 406.
  if (upstream.status >= 400) {
    if (wantsJson(accept)) return problemResponse('not_found', url.pathname);
    const response = new Response(upstream.body, upstream);
    appendVaryAccept(response.headers);
    return response;
  }

  // The client rejected every representation this path has.
  if (preferredType(accept, ['text/html']) === null) {
    return wantsJson(accept)
      ? problemResponse('not_acceptable', url.pathname, { produces })
      : new Response(
          `406 Not Acceptable\n\nAvailable: ${produces.join(', ')}\n${problemTypeUrl('not_acceptable')}\n`,
          {
            status: 406,
            headers: { 'Content-Type': 'text/plain; charset=utf-8', Vary: 'Accept' },
          },
        );
  }

  const response = new Response(upstream.body, upstream);
  appendVaryAccept(response.headers);
  if (twin && response.headers.get('content-type')?.includes('text/html')) {
    const link = `<${twin}>; rel="alternate"; type="text/markdown"`;
    const existing = response.headers.get('link');
    response.headers.set('Link', existing ? `${existing}, ${link}` : link);
  }
  return response;
}

export default {
  /**
   * `env.ORIGIN` overrides where the origin fetch goes, for the case where a
   * subrequest to the worker's own route would come back to the worker. Left
   * unset, requests go to the zone's origin as usual.
   */
  fetch(request, env = {}) {
    return handle(request, (upstream) => {
      if (!env.ORIGIN) return fetch(upstream);
      const target = new URL(upstream.url);
      const origin = new URL(env.ORIGIN);
      target.protocol = origin.protocol;
      target.host = origin.host;
      return fetch(new Request(target.toString(), upstream));
    });
  },
};
