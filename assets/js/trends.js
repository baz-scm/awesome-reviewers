document.addEventListener("DOMContentLoaded", async () => {
  const res   = await fetch("/assets/data/trends.json");
  const data  = await res.json();
  buildLangChart(data);
  buildCatChart(data);
  buildRepoChart(data);
  buildHumanBotPie(data);
  buildTimeline(data);
  buildDowChart(data);
  buildReuseHist(data);
  buildSuggestionStat(data);
});

function buildBarChart({hostId, title, entries, widthFn}) {
  const host = document.getElementById(hostId);
  host.querySelector('.chart-title').textContent = title;
  entries.forEach(([label, count]) => {
    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.innerHTML = `
      <span class=bar-label>${label}</span>
      <span class=bar-fill style="width:${widthFn(count)}%"></span>
      <span class=bar-value>${count}</span>`;
    host.appendChild(bar);
  });
}

/* 1 – Language bar chart */
function buildLangChart(d) {
  buildBarChart({
    hostId: 'lang-chart',
    title: 'Language Distribution',
    entries: Object.entries(d.languages).sort((a,b)=>b[1]-a[1]),
    widthFn: c => (c/d.total_comments*100).toFixed(1)
  });
}

/* 2 – Category bar chart */
function buildCatChart(d){
  buildBarChart({
    hostId: 'cat-chart',
    title: 'Category Distribution',
    entries: Object.entries(d.categories).sort((a,b)=>b[1]-a[1]),
    widthFn: c => (c/d.total_comments*100).toFixed(1)
  });
}

/* 3 – Top 10 repos */
function buildRepoChart(d){
  const top = Object.entries(d.repositories).sort((a,b)=>b[1]-a[1]).slice(0,10);
  buildBarChart({
    hostId: 'repo-chart',
    title: 'Top Source Repositories',
    entries: top,
    widthFn: c => (c/top[0][1]*100).toFixed(1)
  });
}

/* 4 – Human vs Bot pie (CSS conic-gradient) */
function buildHumanBotPie(d){
  const humanPct = +(d.human_comments/d.total_comments*100).toFixed(1);
  const host = document.getElementById("human-bot");
  host.querySelector(".chart-title").textContent = "Human\u202fvs\u202fBot Reviews";
  const pie = host.querySelector(".pie");
  pie.style.background =
    `conic-gradient(#4caf50 0 ${humanPct}%, #d32f2f ${humanPct}% 100%)`;
  host.querySelector(".pie-label").textContent =
    `${humanPct}% human`;
}

/* 5 – Timeline (simple <svg>) */
function buildTimeline(d){
  const host = document.getElementById("timeline");
  host.querySelector(".chart-title").textContent = "Comments per Year";
  const years = Object.keys(d.comments_year).map(Number).sort();
  const max   = Math.max(...years.map(y=>d.comments_year[y]));
  const pts   = years.map((y,i)=>{
      const x = i/(years.length-1)*100;
      const yPct = 100 - (d.comments_year[y]/max*100);
      return `${x},${yPct}`;
  }).join(" ");
  host.querySelector("polyline").setAttribute("points", pts);
}

/* 6 – Day-of-week chart */
function buildDowChart(d){
  const order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  const entries = order.map(day => [day, d.comments_dow[day] || 0]);
  buildBarChart({
    hostId: 'dow-chart',
    title: 'Activity by Day',
    entries,
    widthFn: c => (c/d.total_comments*100).toFixed(1)
  });
}

/* 7 – Prompt reuse histogram */
function buildReuseHist(d){
  const bins = ["1","2-3","4-7","8+"];
  const max = Math.max(...bins.map(b => d.prompt_occ_bins[b] || 0));
  const entries = bins.map(b => [b, d.prompt_occ_bins[b] || 0]);
  buildBarChart({
    hostId: 'reuse-chart',
    title: 'Prompt Reuse',
    entries,
    widthFn: c => (c/max*100).toFixed(1)
  });
}

/* 8 – Suggestion stat block */
function buildSuggestionStat(d){
  const host = document.getElementById("suggestion-stat");
  const pct = (d.suggestion_comments/d.total_comments*100).toFixed(1);
  host.querySelector(".statblock").textContent = `${pct}%`;
}
