/* Awesome Reviewers — expand-in-place, copy, filter, search. No dependencies. */
(function () {
  'use strict';

  var RAW = '/raw/';
  var cache = new Map();

  /* -------------------------------------------------------------- dates -- */

  function relative(iso) {
    var then = Date.parse(iso + 'T00:00:00Z');
    if (isNaN(then)) return '';
    var days = Math.floor((Date.now() - then) / 86400000);
    if (days <= 0) return 'today';
    if (days === 1) return 'yesterday';
    if (days < 30) return days + 'd ago';
    var months = Math.round(days / 30.44);
    if (months < 24) return months + 'mo ago';
    return Math.round(days / 365.25) + 'y ago';
  }

  function stampDates(root) {
    (root || document).querySelectorAll('time[data-date]').forEach(function (el) {
      var iso = el.dataset.date;
      if (!iso || el.dataset.stamped) return;
      el.dateTime = iso;
      el.title = iso;
      el.textContent = relative(iso);
      el.dataset.stamped = '1';
    });
  }

  /* ---------------------------------------------------------------- raw -- */

  /* Raw files open with an HTML-comment metadata header; the page shows the
     instruction itself, and copying it should not carry the header along. */
  function stripHeader(text) {
    return text.replace(/^<!--[\s\S]*?-->\s*/, '');
  }

  function fetchRaw(slug) {
    if (!cache.has(slug)) {
      cache.set(slug, fetch(RAW + slug + '.md')
        .then(function (res) {
          if (!res.ok) throw new Error(res.status);
          return res.text();
        })
        .then(stripHeader)
        .catch(function () {
          cache.delete(slug);
          throw new Error('unavailable');
        }));
    }
    return cache.get(slug);
  }

  function flash(button, label) {
    var original = button.dataset.label || button.textContent;
    button.dataset.label = original;
    button.textContent = label;
    button.dataset.copied = 'true';
    setTimeout(function () {
      button.textContent = original;
      delete button.dataset.copied;
    }, 1600);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    var area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    try { document.execCommand('copy'); } finally { document.body.removeChild(area); }
    return Promise.resolve();
  }

  /* ------------------------------------------------------------ actions -- */

  function toggleRow(button) {
    var row = button.closest('[data-slug]');
    var body = row.querySelector('[data-body]');
    var open = button.getAttribute('aria-expanded') === 'true';

    button.setAttribute('aria-expanded', open ? 'false' : 'true');
    if (open) {
      body.hidden = true;
      return;
    }

    body.hidden = false;
    if (body.dataset.loaded) return;
    body.innerHTML = '<pre class="raw raw--loading">loading…</pre>';
    fetchRaw(row.dataset.slug).then(function (text) {
      var pre = document.createElement('pre');
      pre.className = 'raw';
      pre.textContent = text;
      body.innerHTML = '';
      body.appendChild(pre);
      body.dataset.loaded = '1';
    }).catch(function () {
      body.innerHTML = '<pre class="raw raw--loading">Could not load this instruction. ' +
        'Try <a href="' + RAW + row.dataset.slug + '.md">the raw file</a>.</pre>';
    });
  }

  document.addEventListener('click', function (event) {
    var toggle = event.target.closest('[data-toggle]');
    if (toggle) {
      toggleRow(toggle);
      return;
    }

    var copy = event.target.closest('[data-copy]');
    if (copy) {
      var slug = copy.dataset.copy || copy.closest('[data-slug]').dataset.slug;
      fetchRaw(slug)
        .then(function (text) { return copyText(text); })
        .then(function () { flash(copy, 'copied'); })
        .catch(function () { flash(copy, 'failed'); });
      return;
    }

    var share = event.target.closest('[data-share]');
    if (share) {
      copyText(location.origin + share.dataset.share).then(function () {
        flash(share, 'link copied');
      });
    }
  });

  /* ------------------------------------------------------------ filters -- */

  function initFilters(scope) {
    var rows = Array.prototype.slice.call(scope.querySelectorAll('.row'));
    if (!rows.length) return;

    var text = scope.querySelector('[data-filter-text]');
    var selects = Array.prototype.slice.call(scope.querySelectorAll('[data-filter-key]'));
    var sort = scope.querySelector('[data-sort]');
    var count = scope.querySelector('[data-count]');
    var list = rows[0].parentNode;

    /* Built from the rendered row on first use: keeps the markup small. */
    function haystackOf(row) {
      if (!row._hay) {
        row._hay = (row.querySelector('.row__toggle').textContent + ' ' +
          row.dataset.repository + ' ' + row.dataset.topic + ' ' +
          row.dataset.language).toLowerCase();
      }
      return row._hay;
    }

    function apply() {
      var needle = (text && text.value || '').toLowerCase().trim();
      var terms = needle ? needle.split(/\s+/) : [];
      var visible = 0;

      rows.forEach(function (row) {
        var haystack = terms.length ? haystackOf(row) : '';
        var ok = terms.every(function (term) { return haystack.indexOf(term) !== -1; });
        if (ok) {
          ok = selects.every(function (select) {
            return !select.value || row.dataset[select.dataset.filterKey] === select.value;
          });
        }
        row.classList.toggle('row--hidden', !ok);
        if (ok) visible++;
      });

      if (count) count.textContent = visible + ' of ' + rows.length;
    }

    function titleOf(row) {
      return row.querySelector('.row__title').textContent;
    }

    function reorder() {
      var key = sort.value;
      var sorted = rows.slice().sort(function (a, b) {
        if (key === 'title') return titleOf(a).localeCompare(titleOf(b));
        if (key === 'comments') return Number(b.dataset.comments) - Number(a.dataset.comments);
        return b.dataset.updated.localeCompare(a.dataset.updated);
      });
      var fragment = document.createDocumentFragment();
      sorted.forEach(function (row) { fragment.appendChild(row); });
      list.appendChild(fragment);
    }

    /* Deep links such as /domains/llm-infra/?repository=ollama/ollama */
    var params = new URLSearchParams(location.search);
    if (text && params.get('q')) text.value = params.get('q');
    selects.forEach(function (select) {
      var wanted = params.get(select.dataset.filterKey);
      if (!wanted) return;
      var match = Array.prototype.find.call(select.options, function (option) {
        return option.value === wanted;
      });
      if (match) select.value = wanted;
    });

    if (text) text.addEventListener('input', apply);
    selects.forEach(function (select) { select.addEventListener('change', apply); });
    if (sort) sort.addEventListener('change', reorder);
    apply();
  }

  /* ------------------------------------------------------------ threads -- */

  function renderDiff(diff) {
    return '<pre class="diff">' + diff.split('\n').map(function (line) {
      var kind = line.charAt(0) === '+' ? ' diff__line--add'
        : line.charAt(0) === '-' ? ' diff__line--del' : '';
      return '<div class="diff__line' + kind + '">' + escapeHtml(line || ' ') + '</div>';
    }).join('') + '</pre>';
  }

  function renderComment(comment) {
    var author = escapeHtml(comment.comment_author || 'unknown');
    return '<div class="comment">' +
      '<img src="https://github.com/' + author + '.png?size=44" alt="" loading="lazy" width="22" height="22">' +
      '<div><div class="comment__who">' + author + ' · ' +
      escapeHtml((comment.comment_created_at || '').slice(0, 10)) + '</div>' +
      '<div class="comment__body">' + escapeHtml(comment.comment_body || '') + '</div></div></div>';
  }

  function renderThread(thread) {
    var file = thread.pr_file
      ? escapeHtml(thread.pr_file) + (thread.pr_number ? ' · PR #' + escapeHtml(thread.pr_number) : '')
      : 'discussion';
    return '<div class="thread"><div class="thread__file">' + file + '</div>' +
      (thread.commented_code ? renderDiff(thread.commented_code) : '') +
      (thread.discussion_comments || []).map(renderComment).join('') +
      '</div>';
  }

  function initThreads() {
    var host = document.querySelector('[data-threads]');
    if (!host) return;
    var body = host.querySelector('[data-threads-body]');
    var count = host.querySelector('[data-threads-count]');

    host.addEventListener('toggle', function () {
      if (!host.open || body.dataset.loaded) return;
      body.dataset.loaded = '1';
      body.innerHTML = '<p class="hint">loading…</p>';
      fetch('/' + host.dataset.threads + '.json')
        .then(function (res) { return res.json(); })
        .then(function (threads) {
          body.innerHTML = threads.map(renderThread).join('');
          var comments = threads.reduce(function (total, thread) {
            return total + (thread.discussion_comments || []).length;
          }, 0);
          if (count) count.textContent = '· ' + threads.length + ' threads, ' + comments + ' comments';
        })
        .catch(function () {
          body.innerHTML = '<p class="hint">Source discussions unavailable.</p>';
        });
    }, { once: false });
  }

  /* ------------------------------------------------------------- search -- */

  function rowMarkup(entry) {
    var slug = entry.slug;
    return '<li class="row" data-slug="' + slug + '">' +
      '<div class="row__head"><div>' +
      '<button class="row__toggle" data-toggle aria-expanded="false">' +
      '<span class="row__title">' + escapeHtml(entry.title) + '</span>' +
      '<span class="row__desc">' + escapeHtml(entry.description) + '</span></button>' +
      '<div class="row__meta">' +
      '<a href="https://github.com/' + escapeHtml(entry.repository) + '" rel="noopener">' +
      escapeHtml(entry.repository) + '</a>' +
      '<span class="chip">' + escapeHtml(entry.topic) + '</span>' +
      '<span class="chip">' + escapeHtml(entry.language) + '</span>' +
      '<a href="/domains/' + entry.domain + '/">' + entry.domain + '</a>' +
      '<time data-date="' + entry.updated + '"></time>' +
      '</div></div>' +
      '<div class="row__actions">' +
      '<button class="btn" data-copy="' + slug + '">copy</button>' +
      '<a class="btn" href="/reviewers/' + slug + '/">open</a>' +
      '</div></div>' +
      '<div class="row__body" data-body hidden></div></li>';
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function initSearch() {
    var input = document.querySelector('[data-search-input]');
    if (!input) return;
    var results = document.querySelector('[data-search-results]');
    var status = document.querySelector('[data-search-status]');
    var fallback = document.querySelector('[data-search-fallback]');
    var index = null;
    var loading = null;
    var LIMIT = 60;

    function load() {
      if (!loading) {
        status.textContent = 'loading index…';
        loading = fetch('/assets/data/search.json')
          .then(function (res) { return res.json(); })
          .then(function (data) {
            index = data.entries.map(function (row) {
              return {
                slug: row[0],
                title: row[1],
                domain: data.domains[row[2]],
                topic: data.topics[row[3]],
                language: data.languages[row[4]],
                repository: data.repositories[row[5]],
                updated: row[6],
                comments: row[7],
                description: row[8],
                haystack: (row[1] + ' ' + row[8] + ' ' + data.repositories[row[5]] + ' ' +
                  data.topics[row[3]] + ' ' + data.languages[row[4]] + ' ' +
                  data.domains[row[2]] + ' ' + row[0]).toLowerCase()
              };
            });
          })
          .catch(function () { status.textContent = 'search index unavailable'; });
      }
      return loading;
    }

    function run() {
      var query = input.value.toLowerCase().trim();
      if (!query) {
        results.innerHTML = '';
        status.textContent = '';
        if (fallback) fallback.hidden = false;
        return;
      }
      if (fallback) fallback.hidden = true;
      if (!index) {
        load().then(function () { if (index) run(); });
        return;
      }

      var terms = query.split(/\s+/);
      var scored = [];
      index.forEach(function (entry) {
        var matched = 0;
        for (var i = 0; i < terms.length; i++) {
          if (entry.haystack.indexOf(terms[i]) !== -1) matched++;
        }
        if (matched) scored.push({ entry: entry, matched: matched });
      });

      /* Prefer entries matching every term; if a phrase matches nothing, fall
         back to partial matches ranked by how much of it they cover. */
      var exact = scored.filter(function (hit) { return hit.matched === terms.length; });
      var partial = exact.length === 0;
      var hits = (partial ? scored : exact).sort(function (a, b) {
        return b.matched - a.matched || b.entry.updated.localeCompare(a.entry.updated);
      }).map(function (hit) { return hit.entry; });

      results.innerHTML = hits.slice(0, LIMIT).map(rowMarkup).join('');
      stampDates(results);
      status.textContent = hits.length
        ? (partial ? 'no exact match · ' + hits.length + ' related' :
            hits.length + ' match' + (hits.length === 1 ? '' : 'es')) +
          (hits.length > LIMIT ? ' · showing top ' + LIMIT : '')
        : 'no matches';
    }

    input.addEventListener('focus', load, { once: true });
    input.addEventListener('input', run);
    if (input.value) run();
  }

  /* ---------------------------------------------------------- add a repo -- */

  function initRepoForm() {
    var form = document.querySelector('[data-repo-form]');
    if (!form) return;
    var feedback = form.parentNode.querySelector('[data-repo-feedback]');
    var input = form.querySelector('input');
    var button = form.querySelector('button');

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var match = input.value.trim().match(/github\.com\/([^/\s]+\/[^/\s]+?)(?:\.git|\/|$)/);
      if (!match) {
        feedback.textContent = 'Enter a full GitHub repository URL.';
        return;
      }

      button.disabled = true;
      feedback.textContent = 'Submitting…';
      fetch('https://awesome.baz.co/request?repo_name=' + encodeURIComponent(match[1]))
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (body) {
            feedback.textContent = body.message ||
              (res.status === 202 ? 'Request accepted — the repository is queued.' : 'Request submitted.');
          });
        })
        .catch(function () { feedback.textContent = 'Request failed. Try again later.'; })
        .finally(function () { button.disabled = false; });
    });
  }

  /* ---------------------------------------------------------------- init -- */

  function ready() {
    stampDates(document);
    document.querySelectorAll('[data-filters]').forEach(initFilters);
    initSearch();
    initThreads();
    initRepoForm();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
  } else {
    ready();
  }
}());
