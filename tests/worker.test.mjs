/**
 * Tests for the optional edge worker in edge/worker.js.
 *
 * Run from the repository root:
 *
 *     node --test tests/worker.test.mjs
 *
 * The origin is stubbed, so nothing here reaches the network.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import test, { describe } from 'node:test';

import {
  PROBLEMS,
  appendVaryAccept,
  handle,
  isPassThrough,
  markdownTwin,
  parseAccept,
  preferredType,
  problemTypeUrl,
} from '../edge/worker.js';

const ROOT = new URL('../', import.meta.url);

/** Origin that serves a fixed set of paths and 404s everything else. */
function stubOrigin(files) {
  const seen = [];
  const origin = async (request) => {
    const { pathname } = new URL(request.url);
    seen.push(pathname);
    const file = files[pathname];
    if (!file) {
      return new Response('<!DOCTYPE html><title>404</title>', {
        status: 404,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      });
    }
    return new Response(file.body, {
      status: 200,
      headers: { 'Content-Type': file.type, ...(file.headers ?? {}) },
    });
  };
  origin.seen = seen;
  return origin;
}

const SITE = {
  '/reviewers/example-instruction/': {
    body: '<!DOCTYPE html><title>Example</title>',
    type: 'text/html; charset=utf-8',
  },
  '/raw/example-instruction.md': { body: '# Example\n', type: 'text/markdown' },
  '/domains/ai-agents/': {
    body: '<!DOCTYPE html><title>AI Agents</title>',
    type: 'text/html; charset=utf-8',
  },
  '/raw/bundles/ai-agents.md': { body: '# AI Agents\n', type: 'text/markdown' },
  '/methodology/': {
    body: '<!DOCTYPE html><title>Method</title>',
    type: 'text/html; charset=utf-8',
  },
  '/openapi.json': { body: '{}', type: 'application/json' },
  '/llms.txt': { body: '# Awesome Reviewers\n', type: 'text/plain' },
  '/raw/site.md': { body: '# Awesome Reviewers\n\n## Developer resources\n', type: 'text/markdown' },
  '/': { body: '<!DOCTYPE html><title>Awesome Reviewers</title>', type: 'text/html; charset=utf-8' },
};

const get = (path, accept) =>
  new Request(`https://awesomereviewers.com${path}`, {
    headers: accept ? { Accept: accept } : {},
  });

describe('Accept parsing', () => {
  test('reads q-values and defaults them to 1', () => {
    assert.deepEqual(parseAccept('text/html;q=0.8, text/markdown'), [
      { type: 'text/html', q: 0.8, specificity: 2 },
      { type: 'text/markdown', q: 1, specificity: 2 },
    ]);
  });

  test('ranks wildcards below concrete types', () => {
    const [any, subtype, exact] = parseAccept('*/*, text/*, text/markdown');
    assert.equal(any.specificity, 0);
    assert.equal(subtype.specificity, 1);
    assert.equal(exact.specificity, 2);
  });

  test('clamps out-of-range q-values', () => {
    assert.equal(parseAccept('text/html;q=9')[0].q, 1);
    assert.equal(parseAccept('text/html;q=-1')[0].q, 0);
  });
});

describe('representation choice', () => {
  const produces = ['text/html', 'text/markdown'];

  test('serves the first representation when Accept is absent', () => {
    assert.equal(preferredType(null, produces), 'text/html');
  });

  test('honours an explicit markdown request', () => {
    assert.equal(preferredType('text/markdown', produces), 'text/markdown');
  });

  test('breaks q ties on the client ordering', () => {
    assert.equal(preferredType('text/markdown, text/html, */*', produces), 'text/markdown');
    assert.equal(preferredType('text/html, text/markdown', produces), 'text/html');
  });

  test('prefers the higher q regardless of order', () => {
    assert.equal(preferredType('text/html;q=0.2, text/markdown;q=0.9', produces), 'text/markdown');
  });

  test('a specific q=0 is not smuggled back in by a wildcard', () => {
    assert.equal(preferredType('text/html;q=0, */*', produces), 'text/markdown');
    assert.equal(preferredType('text/markdown;q=0, */*', produces), 'text/html');
  });

  test('returns null when every representation is rejected', () => {
    assert.equal(preferredType('application/pdf', produces), null);
    assert.equal(preferredType('text/html;q=0, text/markdown;q=0', produces), null);
  });

  test('matches a subtype wildcard', () => {
    assert.equal(preferredType('text/*', ['text/markdown']), 'text/markdown');
    assert.equal(preferredType('image/*', ['text/markdown']), null);
  });
});

describe('Vary', () => {
  test('adds Accept when absent', () => {
    const headers = new Headers();
    appendVaryAccept(headers);
    assert.equal(headers.get('vary'), 'Accept');
  });

  test('appends to an existing Vary without dropping it', () => {
    const headers = new Headers({ Vary: 'Accept-Encoding' });
    appendVaryAccept(headers);
    assert.equal(headers.get('vary'), 'Accept-Encoding, Accept');
  });

  test('does not duplicate Accept', () => {
    const headers = new Headers({ Vary: 'Accept-Encoding, accept' });
    appendVaryAccept(headers);
    assert.equal(headers.get('vary'), 'Accept-Encoding, accept');
  });
});

describe('markdown mapping', () => {
  test('maps the page shapes that have a twin', () => {
    assert.equal(markdownTwin('/reviewers/example-instruction/'), '/raw/example-instruction.md');
    assert.equal(markdownTwin('/reviewers/example-instruction'), '/raw/example-instruction.md');
    assert.equal(markdownTwin('/domains/ai-agents/'), '/raw/bundles/ai-agents.md');
    assert.equal(markdownTwin('/'), '/raw/site.md');
  });

  test('leaves pages without a twin alone', () => {
    assert.equal(markdownTwin('/methodology/'), null);
    assert.equal(markdownTwin('/reviewers/'), null);
    assert.equal(markdownTwin('/domains/ai-agents/extra/'), null);
  });

  test('passes files and assets straight through', () => {
    assert.ok(isPassThrough('/raw/example-instruction.md'));
    assert.ok(isPassThrough('/openapi.json'));
    assert.ok(isPassThrough('/llms.txt'));
    assert.ok(isPassThrough('/assets/css/site.css'));
    assert.ok(!isPassThrough('/reviewers/example-instruction/'));
  });
});

describe('negotiation end to end', () => {
  test('serves markdown for Accept: text/markdown', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/reviewers/example-instruction/', 'text/markdown'), origin);

    assert.equal(response.status, 200);
    assert.equal(response.headers.get('content-type'), 'text/markdown; charset=utf-8');
    assert.equal(response.headers.get('vary'), 'Accept');
    assert.equal(response.headers.get('content-location'), '/raw/example-instruction.md');
    assert.equal(await response.text(), '# Example\n');
  });

  test('serves the domain bundle for a domain page', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/domains/ai-agents/', 'text/markdown'), origin);

    assert.equal(response.headers.get('content-type'), 'text/markdown; charset=utf-8');
    assert.equal(await response.text(), '# AI Agents\n');
  });

  test('serves the site overview for the homepage, not the whole corpus index', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/', 'text/markdown'), origin);

    assert.equal(response.headers.get('content-type'), 'text/markdown; charset=utf-8');
    assert.equal(response.headers.get('content-location'), '/raw/site.md');
    assert.match(await response.text(), /## Developer resources/);
  });

  test('serves HTML to a browser and advertises the markdown twin', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(
      get('/reviewers/example-instruction/', 'text/html,application/xhtml+xml,*/*;q=0.8'),
      origin,
    );

    assert.equal(response.status, 200);
    assert.match(response.headers.get('content-type'), /text\/html/);
    assert.equal(response.headers.get('vary'), 'Accept');
    assert.equal(
      response.headers.get('link'),
      '</raw/example-instruction.md>; rel="alternate"; type="text/markdown"',
    );
  });

  test('keeps an origin Vary and adds Accept to it', async () => {
    const origin = stubOrigin({
      ...SITE,
      '/reviewers/example-instruction/': {
        ...SITE['/reviewers/example-instruction/'],
        headers: { Vary: 'Accept-Encoding' },
      },
    });
    const response = await handle(get('/reviewers/example-instruction/'), origin);
    assert.equal(response.headers.get('vary'), 'Accept-Encoding, Accept');
  });

  test('varies on Accept even where there is no markdown to serve', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/methodology/', 'text/markdown, */*;q=0.1'), origin);

    assert.equal(response.status, 200);
    assert.match(response.headers.get('content-type'), /text\/html/);
    assert.equal(response.headers.get('vary'), 'Accept');
    assert.equal(response.headers.get('link'), null);
    assert.deepEqual(origin.seen, ['/methodology/'], 'no markdown twin to probe');
  });

  test('falls back to HTML when the markdown twin is missing but HTML is welcome', async () => {
    const origin = stubOrigin({ '/reviewers/gone/': SITE['/methodology/'] });
    const response = await handle(get('/reviewers/gone/', 'text/markdown, */*'), origin);

    assert.equal(response.status, 200);
    assert.match(response.headers.get('content-type'), /text\/html/);
    assert.deepEqual(origin.seen, ['/raw/gone.md', '/reviewers/gone/']);
  });

  test('does not fall back to HTML the client did not ask for', async () => {
    const origin = stubOrigin({ '/reviewers/gone/': SITE['/methodology/'] });
    for (const accept of ['text/markdown', 'text/markdown, text/html;q=0']) {
      const response = await handle(get('/reviewers/gone/', accept), origin);
      assert.equal(response.status, 406, accept);
      assert.equal(response.headers.get('vary'), 'Accept');
    }
  });

  test('a page with no markdown 406s a markdown-only client', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/methodology/', 'text/markdown'), origin);
    assert.equal(response.status, 406);
  });

  test('passes machine endpoints through untouched', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/openapi.json', 'text/markdown'), origin);

    assert.equal(response.status, 200);
    assert.equal(response.headers.get('content-type'), 'application/json');
    assert.deepEqual(origin.seen, ['/openapi.json']);
  });
});

describe('error responses', () => {
  test('returns problem details to a JSON client', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/does-not-exist/', 'application/json'), origin);

    assert.equal(response.status, 404);
    assert.equal(response.headers.get('content-type'), 'application/problem+json; charset=utf-8');

    const problem = await response.json();
    assert.equal(problem.type, problemTypeUrl('not_found'));
    assert.equal(problem.status, 404);
    assert.equal(problem.code, 'not_found');
    assert.equal(problem.instance, '/does-not-exist/');
    assert.match(problem.resolution, /raw\/index\.json/);
  });

  test('returns problem details for a missing file too', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/raw/missing.md', 'application/problem+json'), origin);

    assert.equal(response.status, 404);
    assert.equal((await response.json()).code, 'not_found');
  });

  test('leaves the HTML 404 page alone for a browser', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/does-not-exist/', 'text/html,*/*;q=0.8'), origin);

    assert.equal(response.status, 404);
    assert.match(response.headers.get('content-type'), /text\/html/);
  });

  test('406 carries problem details when the client wants JSON', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(
      get('/reviewers/example-instruction/', 'application/json, text/html;q=0, text/markdown;q=0'),
      origin,
    );

    assert.equal(response.status, 406);
    const problem = await response.json();
    assert.equal(problem.code, 'not_acceptable');
    assert.deepEqual(problem.produces, ['text/html', 'text/markdown']);
  });

  test('406 is plain text otherwise, and still varies on Accept', async () => {
    const origin = stubOrigin(SITE);
    const response = await handle(get('/reviewers/example-instruction/', 'application/pdf'), origin);

    assert.equal(response.status, 406);
    assert.match(response.headers.get('content-type'), /text\/plain/);
    assert.equal(response.headers.get('vary'), 'Accept');
  });
});

describe('agreement with the published description', () => {
  test('the worker catalogue matches openapi.json', () => {
    let published;
    try {
      published = JSON.parse(readFileSync(new URL('openapi.json', ROOT), 'utf8'));
    } catch (error) {
      assert.fail(
        `openapi.json is missing — run \`python build_data.py\` first (${error.message})`,
      );
    }

    const schema = published.components.schemas.Problem.properties;
    assert.deepEqual(schema.code.enum.sort(), Object.keys(PROBLEMS).sort());
    assert.deepEqual(
      schema.type.enum.sort(),
      Object.keys(PROBLEMS).map(problemTypeUrl).sort(),
    );

    for (const [code, problem] of Object.entries(PROBLEMS)) {
      const documented = Object.values(published.paths)
        .flatMap((item) => Object.values(item))
        .flatMap((operation) => Object.values(operation.responses))
        .flatMap((response) => Object.values(response.content ?? {}))
        .map((media) => media.example)
        .find((example) => example?.code === code);

      assert.ok(documented, `${code} is not documented in openapi.json`);
      assert.equal(documented.title, problem.title);
      assert.equal(documented.detail, problem.detail);
      assert.equal(documented.resolution, problem.resolution);
      assert.equal(documented.status, problem.status);
    }
  });

  test('the site path fileURL resolves to a checkout root', () => {
    assert.ok(readFileSync(fileURLToPath(new URL('build_data.py', ROOT)), 'utf8').length > 0);
  });
});
