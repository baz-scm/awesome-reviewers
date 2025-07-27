// Fetch and display latest merged PRs for News section
document.addEventListener('DOMContentLoaded', function () {
  const list = document.getElementById('news-list');
  const stampEl = document.getElementById('news-timestamp');
  if (!list) return;
  fetch('https://api.github.com/repos/baz-scm/awesome-reviewers/pulls?state=closed&per_page=10', {
    headers: { 'Accept': 'application/vnd.github+json' }
  })
    .then(res => res.ok ? res.json() : Promise.reject(res.status))
    .then(prs => {
      const merged = prs.filter(pr => pr.merged_at).slice(0, 5);
      list.innerHTML = '';
      merged.forEach(pr => {
        const li = document.createElement('li');
        const date = new Date(pr.merged_at).toISOString().slice(0, 10);
        li.innerHTML = `<span class="pr-date">${date}</span> <a href="${pr.html_url}" target="_blank" rel="noopener noreferrer">${pr.title}</a>`;
        list.appendChild(li);
      });
      if (stampEl) {
        const now = new Date();
        stampEl.textContent = `Updated ${now.toISOString().replace('T', ' ').slice(0, 16)} UTC`;
      }
    })
    .catch(() => {
      list.innerHTML = '<li>Unable to load news.</li>';
    });
});
