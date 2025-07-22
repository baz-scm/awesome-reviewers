document.addEventListener('DOMContentLoaded', () => {
  let contributors = {};
  fetch('/assets/data/contributors.json')
    .then(res => res.json())
    .then(data => {
      contributors = data;
      attachListeners();
      const user = location.hash.slice(1);
      if (user && contributors[user]) {
        openContributorDrawer(user);
      }
    });

  function attachListeners() {
    document.querySelectorAll('.contributor-card').forEach(card => {
      card.addEventListener('click', () => {
        const user = card.dataset.contributor;
        if (user) {
          openContributorDrawer(user);
        }
      });
    });
  }

  function openContributorDrawer(user) {
    const drawer = document.getElementById('drawer');
    const content = document.getElementById('drawer-content');
    const data = contributors[user];
    if (!data) return;

    history.replaceState(null, '', `#${user}`);

    const repos = data.repos.map(r => `<li><a href='/?repo=${encodeURIComponent(r)}' target='_blank' rel='noopener noreferrer'>${r}</a></li>`).join('');
    const entries = data.entries.map(e => `<li><a href='/reviewers/${e.slug}/' target='_blank' rel='noopener noreferrer'>${e.title}</a></li>`).join('');
    const comments = Object.entries(data.comments).map(([slug, list]) => {
      const entry = data.entries.find(e => e.slug === slug);
      const title = entry ? entry.title : slug;
      const items = list.map(text => `<li>${text}</li>`).join('');
      return `<details><summary>${title}</summary><ul>${items}</ul></details>`;
    }).join('');

    content.innerHTML = `
      <h2 class='mb-2 font-semibold'>@${user}</h2>
      <details open>
        <summary class='font-medium cursor-pointer'>Repositories</summary>
        <ul class='ml-4 list-disc'>${repos}</ul>
      </details>
      <details open>
        <summary class='font-medium cursor-pointer'>Reviewer Entries</summary>
        <ul class='ml-4 list-disc'>${entries}</ul>
      </details>
      <details>
        <summary class='font-medium cursor-pointer'>Comments</summary>
        <div class='ml-4 space-y-2'>${comments}</div>
      </details>`;

    drawer.classList.add('open');
  }
});
