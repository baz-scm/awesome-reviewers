document.addEventListener('DOMContentLoaded', () => {
    fetch('/assets/data/trends.json')
        .then(r => r.json())
        .then(renderTrends)
        .catch(err => console.error('Failed to load trends data', err));
});

function renderTrends(d) {
    // Pie chart
    const human = Number(d.human_share) || 0;
    const bot = Number(d.bot_share) || 0;
    const total = human + bot || 1;
    const humanPct = Math.round((human / total) * 100);
    const pie = document.querySelector('#human-bot .pie');
    const label = document.querySelector('#human-bot .pie-label');
    if (pie) {
        pie.style.background = `conic-gradient(var(--human-color) 0 0, var(--ai-color) 0 100%)`;
        requestAnimationFrame(() => {
            pie.style.background = `conic-gradient(var(--human-color) 0 ${humanPct}%, var(--ai-color) ${humanPct}% 100%)`;
        });
        pie.title = `${humanPct}% human comments, ${100 - humanPct}% AI`;
        pie.setAttribute('aria-label', pie.title);
    }
    if (label) {
        label.textContent = `${humanPct}% Human \u2022 ${100 - humanPct}% AI`;
    }

    // Length bars
    const humanLen = Number(d.average_human_length) || 0;
    const botLen = Number(d.average_bot_length) || 0;
    const maxLen = Math.max(humanLen, botLen, 1);
    const humanBar = document.getElementById('human-length-bar');
    const botBar = document.getElementById('bot-length-bar');
    const humanVal = document.getElementById('human-length-val');
    const botVal = document.getElementById('bot-length-val');
    if (humanBar) {
        humanBar.style.width = '0';
        humanBar.title = `${humanLen} chars avg (human)`;
        requestAnimationFrame(() => {
            humanBar.style.width = `${(humanLen / maxLen) * 100}%`;
        });
    }
    if (botBar) {
        botBar.style.width = '0';
        botBar.title = `${botLen} chars avg (AI)`;
        requestAnimationFrame(() => {
            botBar.style.width = `${(botLen / maxLen) * 100}%`;
        });
    }
    if (humanVal) humanVal.textContent = humanLen.toLocaleString();
    if (botVal) botVal.textContent = botLen.toLocaleString();

    // Suggestion stat
    const statEl = document.querySelector('#suggestion-stat .statblock');
    const humanRate = Math.round((Number(d.human_suggestion_rate) || 0) * 100);
    const botRate = Math.round((Number(d.bot_suggestion_rate) || 0) * 100);
    if (statEl) {
        statEl.textContent = `Human: ${humanRate}% \u2022 AI: ${botRate}%`;
        statEl.title = `${humanRate}% of human comments vs ${botRate}% of AI comments contain suggestions`;
    }
}
