// Add Repository modal handling
// Attempt POST with required header; if it fails, fall back to a GET request

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

// Mobile header menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const headerEl = document.querySelector('.header');
if (menuToggle && headerEl) {
  menuToggle.addEventListener('click', () => {
    headerEl.classList.toggle('open');
    const open = headerEl.classList.contains('open');
    const hamburgerIcon = menuToggle.querySelector('.hamburger-icon');
    const closeIcon = menuToggle.querySelector('.close-icon');
    if (hamburgerIcon) hamburgerIcon.style.display = open ? 'none' : 'block';
    if (closeIcon) closeIcon.style.display = open ? 'block' : 'none';
  });
}

// Reviewer bundling functionality
const bundleBar = document.getElementById('bundle-bar');
const bundleCountEl = document.getElementById('bundle-count');
let bundleCart = [];

function updateBundleUI() {
  const buttons = document.querySelectorAll('.bundle-button');
  buttons.forEach(btn => {
    const slug = btn.dataset.slug;
    if (bundleCart.includes(slug)) {
      btn.classList.add('added');
      btn.textContent = 'Added';
    } else {
      btn.classList.remove('added');
      btn.textContent = 'Add';
    }
  });

  bundleCountEl.textContent = bundleCart.length;
  bundleBar.style.display = bundleCart.length > 0 ? 'flex' : 'none';
}

function toggleBundle(e, slug) {
  e.stopPropagation();
  const idx = bundleCart.indexOf(slug);
  if (idx >= 0) {
    bundleCart.splice(idx, 1);
  } else {
    bundleCart.push(slug);
  }
  updateBundleUI();
}

function clearBundle() {
  bundleCart = [];
  updateBundleUI();
}

async function downloadBundle() {
  if (bundleCart.length === 0) return;

  const sections = [];
  for (const slug of bundleCart) {
    const res = await fetch(`/_reviewers/${slug}.md`);
    if (!res.ok) continue;
    const text = await res.text();
    const parsed = parseFrontMatter(text);
    sections.push(createSection(parsed.meta, parsed.body));
  }

  const content = '# Bundled Reviewers\n\n' + sections.join('\n');
  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'AGENTS.md';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function parseFrontMatter(text) {
  if (text.startsWith('---')) {
    const end = text.indexOf('---', 3);
    if (end !== -1) {
      const yaml = text.slice(3, end).trim();
      const body = text.slice(end + 3).trim();
      const meta = {};
      yaml.split(/\n/).forEach(line => {
        const sep = line.indexOf(':');
        if (sep !== -1) {
          const key = line.slice(0, sep).trim();
          const val = line.slice(sep + 1).trim();
          meta[key] = val;
        }
      });
      return { meta, body };
    }
  }
  return { meta: {}, body: text };
}

function createSection(meta, body) {
  const title = meta.title || 'Untitled';
  const description = meta.description ? `${meta.description}\n` : '';
  return `## ${title}\n${description}\n${body.trim()}\n`;
}

document.addEventListener('DOMContentLoaded', updateBundleUI);
