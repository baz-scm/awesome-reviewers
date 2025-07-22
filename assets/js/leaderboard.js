document.addEventListener('DOMContentLoaded', () => {
  const dataEl = document.getElementById('review-data');
  const boardEl = document.getElementById('leaderboard');
  if (!dataEl || !boardEl) return;
  const reviewers = JSON.parse(dataEl.textContent);

  // Optionally re-sort:
  reviewers.sort((a, b) => b.comments - a.comments);

  let table = `<table class="leaderboard-table">
                 <thead>
                   <tr><th>Reviewer</th><th>Comments</th><th>⭐ Stars</th></tr>
                 </thead><tbody>`;
  reviewers.forEach(r => {
    table += `<tr>
                <td><a href="/reviewers/${r.slug}/">${r.title}</a></td>
                <td>${r.comments}</td>
                <td>${r.stars}</td>
              </tr>`;
  });
  table += '</tbody></table>';
  boardEl.innerHTML = table;
});
