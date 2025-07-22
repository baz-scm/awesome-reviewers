// Add Repository modal handling
// Attempt POST with required header; if it fails, fall back to a GET request

function renderDiscussionThread(slug, container) {
  fetch(`/reviewers/${slug}.json`)
    .then(r => r.json())
    .then(rawBlocks => {
      const blocks = rawBlocks.map(b => ({
        changes: parseDiff(b.commented_code || ''),
        comments: (b.discussion_comments || []).map(c => ({
          author: {
            username: c.comment_author,
            name: c.comment_author,
            avatar: `https://avatars.githubusercontent.com/${c.comment_author}`,
          },
          content: c.comment_body,
          timestamp: c.comment_created_at,
          isReply: false,
        })),
      }));
      renderDiscussion(container, blocks);
    });
}

function parseDiff(str) {
  return str.split('\n').map(l => {
    if (l.startsWith('+')) return { type: 'added', content: l.slice(1) };
    if (l.startsWith('-')) return { type: 'removed', content: l.slice(1) };
    return { type: 'context', content: l.replace(/^ /, '') };
  });
}

function renderDiscussion(container, blocks) {
  const totalComments = blocks.reduce((sum, b) => sum + b.comments.length, 0);
  const participants = new Set(
    blocks.flatMap(b => b.comments.map(c => c.author.username))
  ).size;
  container.innerHTML = `
    <div class="flex items-center gap-2 mb-4">
      <svg class="h-6 w-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <h2 class="text-2xl font-bold">Discussion Thread</h2>
      <span class="ml-auto text-xs px-2 py-1 rounded bg-muted/20 text-muted-foreground">${totalComments} Comments</span>
    </div>
  `;
  blocks.forEach((block, i) => {
    const blockEl = document.createElement('div');
    blockEl.className = 'rounded-lg border border-muted-foreground/20 overflow-hidden border-l-4 border-l-primary/20';
    let codeHtml = `<div class="bg-slate-50 dark:bg-slate-900/50"><div class="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 border-b text-xs text-muted-foreground flex items-center"><span class="font-mono">Changes #${i + 1}</span></div><div class="font-mono text-sm">`;
    block.changes.forEach(line => {
      const type = line.type;
      const symbol = type === 'added' ? '+' : type === 'removed' ? '-' : '\u00A0';
      const colorCls =
        type === 'added'
          ? 'bg-green-50 dark:bg-green-950/30 border-l-4 border-l-green-500 text-green-600 dark:text-green-400'
          : type === 'removed'
          ? 'bg-red-50 dark:bg-red-950/30 border-l-4 border-l-red-500 text-red-600 dark:text-red-400'
          : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-muted-foreground';
      codeHtml += `<div class="px-3 py-0.5 ${colorCls}"><span class="select-none mr-2 text-xs">${symbol}</span><span class="break-all text-xs">${line.content || '\u00A0'}</span></div>`;
    });
    codeHtml += `</div></div>`;
    blockEl.innerHTML = codeHtml;
    if (block.comments.length) {
      const commentsWrap = document.createElement('div');
      commentsWrap.className = 'p-4 space-y-4';
      block.comments.forEach((c, idx) => {
        if (idx) {
          const sep = document.createElement('hr');
          sep.className = 'my-3 border-t border-muted-foreground/20';
          commentsWrap.appendChild(sep);
        }
        const commentEl = document.createElement('div');
        commentEl.className = `flex gap-3 ${c.isReply ? 'ml-6 pl-3 border-l-2 border-muted' : ''}`;
        commentEl.innerHTML = `
          <img src="${c.author.avatar}" alt="${c.author.name}" class="w-8 h-8 rounded-full border-2 border-background shadow-sm flex-shrink-0"/>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-semibold text-sm">${c.author.name}</h3>
              <span class="text-xs text-muted-foreground">@${c.author.username}</span>
              <div class="flex items-center gap-1 text-xs text-muted-foreground ml-auto">
                <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                ${c.timestamp}
              </div>
            </div>
            <p class="prose prose-sm max-w-none dark:prose-invert text-xs leading-relaxed m-0">${c.content}</p>
          </div>`;
        commentsWrap.appendChild(commentEl);
      });
      blockEl.appendChild(commentsWrap);
    }
    container.appendChild(blockEl);
  });
  const footer = document.createElement('div');
  footer.className = 'bg-slate-50 dark:bg-slate-900/50 rounded-lg p-3 text-xs text-muted-foreground flex items-center justify-between';
  footer.innerHTML = `<div class="flex items-center gap-3"><span class="flex items-center gap-1"><svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>${participants} participants</span><span class="flex items-center gap-1"><svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>${totalComments} total comments</span></div><span>Last updated ${blocks[0]?.comments[0]?.timestamp || ''}</span>`;
  container.appendChild(footer);
}

const modal = document.getElementById('add-repo-modal');
const openBtn = document.getElementById('add-repo-button');
const closeBtn = modal.querySelector('.modal__close');
const backdrop = modal.querySelector('.modal__backdrop');
const form = document.getElementById('add-repo-form');
const feedbackEl = document.getElementById('repo-add-feedback');

// Open modal
openBtn && openBtn.addEventListener('click', () => {
  modal.classList.add('modal--open');
  feedbackEl.textContent = '';
  form.reset();
});

// Close modal
[closeBtn, backdrop].forEach(el =>
  el.addEventListener('click', () => modal.classList.remove('modal--open'))
);

// Submit handler
form && form.addEventListener('submit', async e => {
  e.preventDefault();
  feedbackEl.textContent = '';
  
  const submitBtn = form.querySelector('button[type="submit"]');
  const urlInput = document.getElementById('repo-url-input');
  const originalButtonText = submitBtn.textContent;
  
  // Set loading state
  submitBtn.disabled = true;
  urlInput.disabled = true;
  submitBtn.textContent = 'Adding...';
  feedbackEl.textContent = '';
  feedbackEl.className = 'modal__feedback';
  
  const url = urlInput.value.trim();
  const m = url.match(/github\.com\/([^/]+\/[^/]+)(?:\/|$)/);
  if (!m) {
    feedbackEl.textContent = 'Repo not valid';
    feedbackEl.className = 'modal__feedback invalid';
    // Reset loading state
    submitBtn.disabled = false;
    urlInput.disabled = false;
    submitBtn.textContent = originalButtonText;
    return;
  }
  
  const repo = encodeURIComponent(m[1]);
  try {
    let res;
    try {
      res = await fetch(
        `https://awesome.baz.co/request?repo_name=${repo}`,
        {
          method: 'POST',
          headers: {
            'x-amz-content-sha256':
              'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
          }
        }
      );
      if (!res.ok && res.status !== 409) throw new Error(res.statusText);
    } catch (postErr) {
      res = await fetch(
        `https://awesome.baz.co/request?repo_name=${repo}`
      );
      if (!res.ok && res.status !== 409) throw new Error(res.statusText);
    }

    const status = res.status;
    let message = '';
    try {
      const data = await res.json();
      message = data.message || '';
    } catch (e) {
      // no JSON body
    }

    let valid = true;
    if (status === 202) {
      feedbackEl.textContent = '✅ Request accepted – processing soon.';
    } else if (status === 409 && message) {
      feedbackEl.textContent = `⚠️ ${message}`;
    } else if (status === 400 && message) {
      feedbackEl.textContent = `❌ ${message}`;
      valid = false;
    } else {
      feedbackEl.textContent = '⚠️ Request submitted.';
    }
    feedbackEl.className = valid ? 'modal__feedback valid' : 'modal__feedback invalid';
  } catch (err) {
    feedbackEl.textContent = 'Repo not valid';
    feedbackEl.className = 'modal__feedback invalid';
  } finally {
    // Reset loading state
    submitBtn.disabled = false;
    urlInput.disabled = false;
    submitBtn.textContent = originalButtonText;
  }
});

