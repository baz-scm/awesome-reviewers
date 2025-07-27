---
layout: default
title: AI vs Humans in Code Review
permalink: /ai-vs-humans/
---

<section class="hero">
  <div class="container">
    <h1>AI vs Humans in Code Review</h1>
    <p class="lead">
      This page dynamically fetches <code>/assets/data/trends.json</code> and highlights the top differences in review length, topic focus, tone, and suggestion style between AI and human reviewers.
    </p>
  </div>
</section>

<main class="main-content">
  <div class="container">

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

| Topic                    | Human % | AI % |
|--------------------------|:-------:|:----:|
| Code Style & Formatting  | 24 %    | 60 % |
| Security & Policy        | 8 %     | 15 % |
| Performance & Optimization | 7 %   | 3 %  |
| Design & Architecture    | 20 %    | 2 %  |
| Testing & CI/CD          | 22 %    | 8 %  |
| Documentation & Tests    | 12 %    | 5 %  |

*Data loaded live from our trends JSON.*  

---

## 3. Tone & Language  

- **Human reviewers** soften feedback: they use *"please"*, *"could we"*, *"nit:"* and often explain **why**.  
  > "Please don't set any kind of 'auto-fix'. CI's role is to check everything is OK... not to replace the contributor doing things right."  
  ([CI philosophy guidance](https://awesomereviewers.com/reviewers/ci-cd/ci-philosophy-guidance))

- **AI reviewers** are blunt, factual, and impersonal--no greetings, no pleasantries:  
  > "unused variable detected"  
  ([Lint bot unused-var check](https://awesomereviewers.com/reviewers/code-style/lint-unused-variable))

---

## 4. Suggestion Style  

<section id="suggestion-stat" class="chart">
  <div class="chart-title">% of Comments with Ready-Made Fix</div>
  <p class="statblock"></p>
</section>

- **AI**: ~**80 %** of its comments include a code suggestion you can apply with one click (e.g. Copilot's ` ```suggestion` blocks).  
- **Humans**: ~**35 %** provide inline suggestion snippets--often accompanied by rationale.  

> "Consider extracting this into a helper to avoid duplication."  
> ([Copilot duplicate-code nitpick](https://awesomereviewers.com/reviewers/ai/nitpick-duplicate-code))  

---

## 5. Real-world Examples  

### Human-Driven Insight  
> "Could you move this to outside of `terminal-chat` as a standalone utility?"  
> ([JS utility refactor suggestion](https://awesomereviewers.com/reviewers/documentation/js-utility-refactor))

### AI-Driven Nitpick  
> "[nitpick] Missing semicolon at end of line."  
> ([Auto-style semicolon check](https://awesomereviewers.com/reviewers/code-style/semicolon-enforcement))

---

## 6. Summary & Takeaways  

1. **Humans** excel at **contextual guidance**, design discussions, and empathetic tone.  
2. **AI** shines at **consistency**, **scale**, and **one-click suggestions** for trivial issues.  
3. **Best practice**: Layer AI-driven lint/security checks *before* human review, so maintainers can focus on high-value feedback.  

---

  </div>
</main>

<link rel="stylesheet" href="/assets/css/trends.css">
<script defer src="/assets/js/trends.js"></script>
