document.addEventListener('DOMContentLoaded', () => {
  let contributors = {};
  fetch('/assets/data/contributors.json')
    .then(res => res.json())
    .then(data => {
      contributors = data;
      attachListeners();
      openFromHash();
    });

  window.addEventListener('hashchange', openFromHash);

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

  function openFromHash() {
    const user = location.hash.slice(1);
    if (user && contributors[user]) {
      openContributorDrawer(user, false);
    } else if (!user) {
      closeDrawer();
    }
  }

  function openContributorDrawer(user, updateHash = true) {
    const drawer = document.getElementById('drawer');
    const content = document.getElementById('drawer-content');
    const data = contributors[user];
    if (!data) return;

    if (updateHash) {
      history.replaceState(null, '', `#${user}`);
    }

    const commentCount = Object.values(data.comments).reduce((sum, arr) => sum + arr.length, 0);

    const reposHtml = data.repos.map(r =>
      `<a href='/?repo=${encodeURIComponent(r)}' target='_blank' rel='noopener noreferrer' class='block border rounded-md p-2 hover:bg-gray-50'>⭐ ${r} <span class="ml-1">↗️</span></a>`
    ).join('');

    const entriesHtml = data.entries.map(e =>
      `<a href='/reviewers/${e.slug}/' target='_blank' rel='noopener noreferrer' class='block border rounded-md p-2 hover:bg-gray-50'>${e.title} <span class="ml-1">↗️</span></a>`
    ).join('');

    const commentsHtml = Object.entries(data.comments).map(([slug, list]) => {
      const entry = data.entries.find(e => e.slug === slug);
      const title = entry ? entry.title : slug;
      const items = list.map(text => `<li class='mb-1'>${text}</li>`).join('');
      return `<details class='border rounded-md p-2 mb-2'><summary class='cursor-pointer font-medium'>${title}</summary><ul class='mt-2 ml-4 list-disc'>${items}</ul></details>`;
    }).join('');

    const header = `
      <div class='p-4 border-b'>
        <div class='flex items-center space-x-3'>
          <img src='https://github.com/${user}.png?size=80' class='w-16 h-16 rounded-full' alt='${user} avatar'>
          <div>
            <h2 class='font-bold text-xl'>@${user}</h2>
            ${data.name ? `<div class='text-sm text-gray-700'>${data.name}</div>` : ''}
            ${data.bio ? `<div class='text-sm text-gray-700'>${data.bio}</div>` : ''}
            ${data.company ? `<div class='text-sm text-gray-700'>🏢 ${data.company}</div>` : ''}
            ${data.location ? `<div class='text-sm text-gray-700'>📍 ${data.location}</div>` : ''}
          </div>
        </div>
      </div>`;

    const stats = `
      <div class='flex text-center divide-x divide-gray-200 my-4'>
        <div class='flex-1'>
          <div class='text-lg font-semibold'>${data.repos.length}</div>
          <div class='text-xs text-gray-600'>Repositories</div>
        </div>
        <div class='flex-1'>
          <div class='text-lg font-semibold'>${data.entries.length}</div>
          <div class='text-xs text-gray-600'>Entries</div>
        </div>
        <div class='flex-1'>
          <div class='text-lg font-semibold'>${commentCount}</div>
          <div class='text-xs text-gray-600'>Comments</div>
        </div>
      </div>`;

    const reposSection = `
      <div class='p-4'>
        <h3 class='font-semibold mb-2'>Repositories</h3>
        <div class='space-y-2'>${reposHtml}</div>
      </div>`;

    const entriesSection = `
      <div class='p-4'>
        <h3 class='font-semibold mb-2'>Reviewer Entries</h3>
        <div class='space-y-2'>${entriesHtml}</div>
      </div>`;

    const commentsSection = `
      <div class='p-4'>
        <h3 class='font-semibold mb-2'>Comments</h3>
        <div>${commentsHtml}</div>
      </div>`;

    content.innerHTML = header + stats + reposSection + entriesSection + commentsSection;

    drawer.classList.add('open');
    const panel = drawer.querySelector('.drawer-panel');
    if (panel) panel.scrollTop = 0;
  }
});
