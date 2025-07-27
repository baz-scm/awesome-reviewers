document.addEventListener('DOMContentLoaded', async () => {
  const res = await fetch('/assets/data/trends.json');
  const d = await res.json();
  buildSummaryStats(d);
  buildLangChart(d);
  buildCatChart(d);
  buildRepoList(d);
  buildHumanBotProgress(d);
  buildYearSpark(d);
  buildDowBars(d);
  buildReuseBars(d);
  buildSuggestionStat(d);
});

function asciiBarChart(hostId, title, entries) {
  const host = document.getElementById(hostId);
  host.querySelector('.chart-title').textContent = title;
  const pre = host.querySelector('pre');
  const max = Math.max(...entries.map(e => e[1]));
  const width = 20;
  const lines = entries.map(([label,count]) => {
    const barLen = Math.round(count / max * width);
    const bar = '#'.repeat(barLen).padEnd(width, ' ');
    return `${label.padEnd(15)} | ${bar} | ${count}`;
  });
  pre.textContent = lines.join('\n');
}

function buildLangChart(d){
  const entries = Object.entries(d.languages).sort((a,b)=>b[1]-a[1]).slice(0,10);
  asciiBarChart('lang-chart','Language Distribution',entries);
}

function buildCatChart(d){
  const entries = Object.entries(d.categories).sort((a,b)=>b[1]-a[1]).slice(0,10);
  asciiBarChart('cat-chart','Category Distribution',entries);
}

function buildRepoList(d){
  const host = document.getElementById('repo-chart');
  host.querySelector('.chart-title').textContent = 'Top Source Repositories';
  const pre = host.querySelector('pre');
  const top = Object.entries(d.repositories).sort((a,b)=>b[1]-a[1]).slice(0,10);
  const lines = top.map(([repo,count],i)=>`${String(i+1).padStart(2,'.')} ${repo} - ${count}`);
  pre.textContent = lines.join('\n');
}

function buildHumanBotProgress(d){
  const host = document.getElementById('human-bot');
  host.querySelector('.chart-title').textContent = 'Human vs Bot Reviews';
  const pre = host.querySelector('pre');
  const pct = Math.round(d.human_comments / d.total_comments * 100);
  const width = 20;
  const filled = Math.round(pct/100 * width);
  const bar = '#'.repeat(filled).padEnd(width, '-');
  pre.textContent = `[${bar}] ${pct}% human`;
}

function buildYearSpark(d){
  const host = document.getElementById('timeline');
  host.querySelector('.chart-title').textContent = 'Comments per Year';
  const pre = host.querySelector('pre');
  const years = Object.keys(d.comments_year).map(Number).sort();
  const max = Math.max(...years.map(y=>d.comments_year[y]));
  const height = 4;
  const values = years.map(y=>d.comments_year[y]);
  let lines = [];
  for(let h=height; h>=1; h--){
    lines.push(values.map(v => v/max*height>=h ? '█' : ' ').join(''));
  }
  lines.push(years.map(y=>String(y).slice(2)).join(''));
  pre.textContent = lines.join('\n');
}

function buildDowBars(d){
  const host = document.getElementById('dow-chart');
  host.querySelector('.chart-title').textContent = 'Activity by Day';
  const pre = host.querySelector('pre');
  const days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const max=Math.max(...days.map(day=>d.comments_dow[day]||0));
  const height=5;
  let lines=[];
  for(let h=height; h>=1; h--){
    lines.push(days.map(day => (d.comments_dow[day]||0)/max*height>=h ? '█' : ' ').join(''));
  }
  lines.push(days.map(d=>d[0]).join(''));
  pre.textContent=lines.join('\n');
}

function buildReuseBars(d){
  const host=document.getElementById('reuse-chart');
  host.querySelector('.chart-title').textContent='Prompt Reuse';
  const pre=host.querySelector('pre');
  const bins=['1','2-3','4-7','8+'];
  const max=Math.max(...bins.map(b=>d.prompt_occ_bins[b]||0));
  const height=5;
  let lines=[];
  for(let h=height; h>=1; h--){
    lines.push(bins.map(b=> (d.prompt_occ_bins[b]||0)/max*height>=h ? '█':' ').join(' '));
  }
  lines.push(bins.join(' '));
  pre.textContent=lines.join('\n');
}

function buildSuggestionStat(d){
  const host=document.getElementById('suggestion-stat');
  const pct=(d.suggestion_comments/d.total_comments*100).toFixed(1);
  host.querySelector('.statblock').textContent=pct+'%';
}

function buildSummaryStats(d){
  document.getElementById('stat-total-languages').textContent = Object.keys(d.languages).length;
  document.getElementById('stat-category-count').textContent = Object.keys(d.categories).length;
  document.getElementById('stat-top-repos').textContent = Object.entries(d.repositories).sort((a,b)=>b[1]-a[1]).slice(0,8).length;
  document.getElementById('stat-reuse-8plus').textContent = d.prompt_occ_bins['8+']||0;
}
