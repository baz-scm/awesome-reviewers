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
  const url = document.getElementById('repo-url-input').value.trim();
  const m = url.match(/github\.com\/([^/]+\/[^/]+)(?:\/|$)/);
  if (!m) {
    feedbackEl.textContent = 'Repo not valid';
    feedbackEl.className = 'modal__feedback invalid';
    return;
  }
  const repo = encodeURIComponent(m[1]);
  try {
    let res;
    try {
      res = await fetch(
        `https://awesome.baz.ninja/request?repo_name=${repo}`,
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
  }
});
