// Add Repository modal handling
// Attempt POST with required header; if it fails, fall back to a GET request

const modal = document.getElementById('add-repo-modal');
const openBtn = document.getElementById('add-repo-button');
const closeBtn = modal ? modal.querySelector('.modal__close') : null;
const backdrop = modal ? modal.querySelector('.modal__backdrop') : null;

if (openBtn && modal) {
  openBtn.addEventListener('click', () => {
    modal.classList.add('modal--open');
    const modalForm = modal.querySelector('[data-add-repo-form]');
    const modalFeedback = modal.querySelector('[data-repo-feedback]');
    if (modalForm) {
      modalForm.reset();
      const urlInput = modalForm.querySelector('input[type="url"]');
      if (urlInput) urlInput.focus();
    }
    if (modalFeedback) {
      modalFeedback.textContent = '';
      modalFeedback.classList.remove('valid', 'invalid');
    }
  });
}

if (modal) {
  [closeBtn, backdrop].forEach(el => {
    if (el) {
      el.addEventListener('click', () => modal.classList.remove('modal--open'));
    }
  });
}

const addRepoForms = document.querySelectorAll('[data-add-repo-form]');

addRepoForms.forEach(form => {
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const feedbackEl = form.querySelector('[data-repo-feedback]');
    const submitBtn = form.querySelector('button[type="submit"]');
    const urlInput = form.querySelector('input[type="url"]');
    if (!submitBtn || !urlInput) return;

    if (feedbackEl) {
      feedbackEl.textContent = '';
      feedbackEl.classList.remove('valid', 'invalid');
    }

    const originalButtonText = submitBtn.textContent;
    const url = urlInput.value.trim();

    // Set loading state
    submitBtn.disabled = true;
    urlInput.disabled = true;
    submitBtn.textContent = 'Adding...';

    const m = url.match(/github\.com\/([^/]+\/[^/]+)(?:\/|$)/);
    if (!m) {
      if (feedbackEl) {
        feedbackEl.textContent = 'Repo not valid';
        feedbackEl.classList.add('invalid');
      }
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
      } catch (err) {
        // no JSON body
      }

      let valid = true;
      if (status === 202) {
        if (feedbackEl) feedbackEl.textContent = '✅ Request accepted – processing soon.';
      } else if (status === 409 && message) {
        if (feedbackEl) feedbackEl.textContent = `⚠️ ${message}`;
      } else if (status === 400 && message) {
        if (feedbackEl) feedbackEl.textContent = `❌ ${message}`;
        valid = false;
      } else {
        if (feedbackEl) feedbackEl.textContent = '⚠️ Request submitted.';
      }
      if (feedbackEl) {
        feedbackEl.classList.remove('valid', 'invalid');
        feedbackEl.classList.add(valid ? 'valid' : 'invalid');
      }
    } catch (err) {
      if (feedbackEl) {
        feedbackEl.textContent = 'Repo not valid';
        feedbackEl.classList.remove('valid', 'invalid');
        feedbackEl.classList.add('invalid');
      }
    } finally {
      submitBtn.disabled = false;
      urlInput.disabled = false;
      submitBtn.textContent = originalButtonText;
    }
  });
});

