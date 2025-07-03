// Add Repository modal handling
window.CAN_USE_HEADERS = location.hostname.includes('baz.ninja');

const modal = document.getElementById('add-repo-modal');
const openBtn = document.getElementById('add-repo-card');
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
    const res = await fetch(
      `https://awesome.baz.ninja/request?repo_name=${repo}`, {
        method: window.CAN_USE_HEADERS ? 'POST' : 'GET',
        ...(window.CAN_USE_HEADERS && {
          headers: {
            'Content-Type': 'application/json',
            'x-amz-content-sha256':
              'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
          },
          body: '{}'
        })
      }
    );
    if (res.ok) {
      feedbackEl.textContent = 'Repo valid';
      feedbackEl.className = 'modal__feedback valid';
    } else {
      const txt = await res.text();
      throw new Error(txt || res.statusText);
    }
  } catch (err) {
    feedbackEl.textContent = 'Repo not valid';
    feedbackEl.className = 'modal__feedback invalid';
  }
});
