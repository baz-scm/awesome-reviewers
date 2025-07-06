let votesData = {};
let votesSha = '';

async function loadVotes() {
  try {
    const res = await fetch('/assets/data/votes.json');
    votesData = await res.json();
  } catch (e) {
    console.error('Failed to load votes', e);
  }
  updateVoteCounts();
}

function updateVoteCounts() {
  document.querySelectorAll('.reviewer-card').forEach(card => {
    const slug = card.dataset.slug;
    const counts = votesData[slug] || { up: 0, down: 0 };
    const up = card.querySelector('.up-count');
    const down = card.querySelector('.down-count');
    if (up) up.textContent = counts.up;
    if (down) down.textContent = counts.down;
  });
}

function voteReview(e, slug, delta) {
  e.stopPropagation();
  if (sessionStorage.getItem(`voted_${slug}`)) return;
  const card = document.querySelector(`[data-slug="${slug}"]`);
  if (!card) return;
  const upBtn = card.querySelector('.upvote-btn');
  const downBtn = card.querySelector('.downvote-btn');
  const upSpan = card.querySelector('.up-count');
  const downSpan = card.querySelector('.down-count');
  if (delta === 1 && upSpan) upSpan.textContent = parseInt(upSpan.textContent) + 1;
  if (delta === -1 && downSpan) downSpan.textContent = parseInt(downSpan.textContent) + 1;
  if (upBtn) upBtn.disabled = true;
  if (downBtn) downBtn.disabled = true;
  sessionStorage.setItem(`voted_${slug}`, 'true');
  if (!votesData[slug]) votesData[slug] = { up: 0, down: 0 };
  if (delta === 1) votesData[slug].up++; else votesData[slug].down++;
  saveVote(slug);
}

async function saveVote(slug) {
  const token = window.GITHUB_TOKEN;
  if (!token) return;
  try {
    if (!votesSha) {
      const res = await fetch('https://api.github.com/repos/baz-scm/awesome-reviewers/contents/assets/data/votes.json');
      const data = await res.json();
      votesSha = data.sha;
    }
    const content = btoa(JSON.stringify(votesData, null, 2));
    await fetch('https://api.github.com/repos/baz-scm/awesome-reviewers/contents/assets/data/votes.json', {
      method: 'PUT',
      headers: {
        'Accept': 'application/vnd.github+json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message: `Update votes for ${slug}`,
        content,
        sha: votesSha
      })
    });
  } catch (err) {
    console.error('Failed to save vote', err);
  }
}

document.addEventListener('DOMContentLoaded', loadVotes);
