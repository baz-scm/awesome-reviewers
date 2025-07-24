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

/* 1 – Language bar chart */
function buildLangChart(d) {
  const host = document.getElementById("lang-chart");
  host.querySelector(".chart-title").textContent = "Language Distribution";
  Object.entries(d.languages)
    .sort((a,b)=>b[1]-a[1])
    .forEach(([lang,count])=>{
      const bar = document.createElement("div"); bar.className="bar";
      bar.innerHTML =
        `<span class=bar-label>${lang}</span>
         <span class=bar-fill style="width:${(count/d.total_comments*100).toFixed(1)}%"></span>
         <span class=bar-value>${count}</span>`;
      host.appendChild(bar);
    });
}

/* 2 – Category bar chart */
function buildCatChart(d){
  const host = document.getElementById("cat-chart");
  host.querySelector(".chart-title").textContent = "Category Distribution";
  Object.entries(d.categories)
    .sort((a,b)=>b[1]-a[1])
    .forEach(([cat,count])=>{
      const bar = document.createElement("div"); bar.className="bar";
      bar.innerHTML =
        `<span class=bar-label>${cat}</span>
         <span class=bar-fill style="width:${(count/d.total_comments*100).toFixed(1)}%"></span>
         <span class=bar-value>${count}</span>`;
      host.appendChild(bar);
    });
}

/* 3 – Top 10 repos */
function buildRepoChart(d){
  const top = Object.entries(d.repositories).sort((a,b)=>b[1]-a[1]).slice(0,10);
  const host = document.getElementById("repo-chart");
  host.querySelector(".chart-title").textContent = "Top Source Repositories";
  top.forEach(([r,c])=>{
    const bar = document.createElement("div"); bar.className="bar";
    bar.innerHTML =
      `<span class=bar-label>${r}</span>
       <span class=bar-fill style="width:${(c/top[0][1]*100).toFixed(1)}%"></span>
       <span class=bar-value>${c}</span>`;
    host.appendChild(bar);
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
  const host = document.getElementById("dow-chart");
  host.querySelector(".chart-title").textContent = "Activity by Day";
  const order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  order.forEach(day => {
    const count = d.comments_dow[day] || 0;
    const bar = document.createElement("div"); bar.className="bar";
    bar.innerHTML =
      `<span class=bar-label>${day}</span>
       <span class=bar-fill style="width:${(count/d.total_comments*100).toFixed(1)}%"></span>
       <span class=bar-value>${count}</span>`;
    host.appendChild(bar);
  });
}

/* 7 – Prompt reuse histogram */
function buildReuseHist(d){
  const bins = ["1","2-3","4-7","8+"];
  const host = document.getElementById("reuse-chart");
  host.querySelector(".chart-title").textContent = "Prompt Reuse";
  const max = Math.max(...bins.map(b => d.prompt_occ_bins[b] || 0));
  bins.forEach(bin => {
    const c = d.prompt_occ_bins[bin] || 0;
    const bar = document.createElement("div"); bar.className="bar";
    bar.innerHTML =
      `<span class=bar-label>${bin}</span>
       <span class=bar-fill style="width:${(c/max*100).toFixed(1)}%"></span>
       <span class=bar-value>${c}</span>`;
    host.appendChild(bar);
  });
}

/* 8 – Suggestion stat block */
function buildSuggestionStat(d){
  const host = document.getElementById("suggestion-stat");
  const pct = (d.suggestion_comments/d.total_comments*100).toFixed(1);
  host.querySelector(".statblock").textContent = `${pct}%`;
}
