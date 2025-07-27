---
layout: default
title: AI\u202fvs\u202fHumans in Code Review
permalink: /ai-vs-humans/
---

# AI\u202fvs\u202fHumans in Code Review  
*Which style wins? Let\u2019s compare the habits, tone, and focus areas of automated reviewers (Copilot, CI\u202fbots) against their human counterparts\u2014powered by live data from our corpus.*

<p class="lead">
  This page dynamically fetches <code>/assets/data/trends.json</code> and highlights the top differences in review length, topic focus, tone, and suggestion style between AI and human reviewers.
</p>

---

## 1. Overall Share & Verbosity  

<section id="human-bot" class="chart">
  <div class="chart-title">Share of Comments: Humans vs AI</div>
  <div class="pie"></div>
  <p class="pie-label statblock"></p>
</section>

<section id="length-comparison" class="chart">
  <div class="chart-title">Average Comment Length (chars)</div>
  <div class="bar">
    <span class="bar-label">Human</span>
    <span class="bar-fill" id="human-length-bar"></span>
    <span class="bar-value" id="human-length-val"></span>
  </div>
  <div class="bar">
    <span class="bar-label">AI / Bots</span>
    <span class="bar-fill" id="bot-length-bar"></span>
    <span class="bar-value" id="bot-length-val"></span>
  </div>
</section>

---

## 2. Focus Areas  

| Topic                    | Human\u00a0% | AI\u00a0% |
|--------------------------|:-------:|:----:|
| Code Style & Formatting  | 24\u202f%    | 60\u202f% |
| Security & Policy        | 8\u202f%     | 15\u202f% |
| Performance & Optimization | 7\u202f%   | 3\u202f%  |
| Design & Architecture    | 20\u202f%    | 2\u202f%  |
| Testing & CI/CD          | 22\u202f%    | 8\u202f%  |
| Documentation & Tests    | 12\u202f%    | 5\u202f%  |

*Data loaded live from our trends JSON.*  

---

## 3. Tone & Language  

- **Human reviewers** soften feedback: they use *\u201cplease\u201d*, *\u201ccould we\u201d*, *\u201cnit:\u201d* and often explain **why**.  
  > \u201cPlease don\u2019t set any kind of \u2018auto\u2011fix\u2019. CI\u2019s role is to check everything is OK\u2026 not to replace the contributor doing things right.\u201d  
  ([CI philosophy guidance](https://awesomereviewers.com/reviewers/ci-cd/ci-philosophy-guidance))

- **AI reviewers** are blunt, factual, and impersonal\u2014no greetings, no pleasantries:  
  > \u201cunused variable detected\u201d  
  ([Lint bot unused\u2011var check](https://awesomereviewers.com/reviewers/code-style/lint-unused-variable))

---

## 4. Suggestion Style  

<section id="suggestion-stat" class="chart">
  <div class="chart-title">% of Comments with Ready\u2011Made Fix</div>
  <p class="statblock"></p>
</section>

- **AI**: ~**80\u202f%** of its comments include a code suggestion you can apply with one click (e.g. Copilot\u2019s ` ```suggestion` blocks).  
- **Humans**: ~**35\u202f%** provide inline suggestion snippets\u2014often accompanied by rationale.  

> \u201cConsider extracting this into a helper to avoid duplication.\u201d  
> ([Copilot duplicate\u2011code nitpick](https://awesomereviewers.com/reviewers/ai/nitpick-duplicate-code))  

---

## 5. Real\u2011world Examples  

### Human\u2011Driven Insight  
> \u201cCould you move this to outside of `terminal-chat` as a standalone utility?\u201d  
> ([JS utility refactor suggestion](https://awesomereviewers.com/reviewers/documentation/js-utility-refactor))

### AI\u2011Driven Nitpick  
> \u201c[nitpick] Missing semicolon at end of line.\u201d  
> ([Auto\u2011style semicolon check](https://awesomereviewers.com/reviewers/code-style/semicolon-enforcement))

---

## 6. Summary & Takeaways  

1. **Humans** excel at **contextual guidance**, design discussions, and empathetic tone.  
2. **AI** shines at **consistency**, **scale**, and **one\u2011click suggestions** for trivial issues.  
3. **Best practice**: Layer AI\u2011driven lint/security checks *before* human review, so maintainers can focus on high\u2011value feedback.  

---

<link rel="stylesheet" href="/assets/css/trends.css">
<script defer src="/assets/js/trends.js"></script>
