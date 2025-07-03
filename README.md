<div align="center">
   <img align="center" width="128px" src="https://avatars.githubusercontent.com/u/140384842?s=200&v=4" />
   <h1 align="center"><b>Awesome Reviewers ✨ </b></h1>
   <p align="center">
      Ready-to-use system prompts for Agentic Code Review.
      <br />
      <a href="https://awesomereviewers.com"><strong>AwesomeReviewers.com »</strong></a>
      <br />
   </p>
</div>

<div align="center">
   <img align="center" width="600px" src="assets/images/ar-web.png" />
</div>


**Awesome Reviewers** is an open-source registry of ready-to-use **system prompts** for agentic code review. Each “reviewer” prompt is distilled from thousands of real code review comments in leading open source repositories. These prompts capture best practices and coding standards that developers can easily apply during pull request reviews. Simply **copy and paste** a prompt into your AI coding agents (e.g. VS Code, Cursor, Claude, or any AI agent) to instantly get code review suggestions aligned with proven standards

## Features

* **Hundreds of Curated Prompts:** Contains **hundreds of specialized review prompts** (over 470 and counting) covering many languages and frameworks. Each prompt is distilled from actual pull request comments, ensuring **practical, actionable advice** grounded in real code review scenarios. Prompts span categories like *Code Style*, *Documentation*, *Testing*, *Security*, *Performance*, *API Design*, *Naming Conventions*, and more – addressing the areas developers care about most.

* **Real Open-Source Insights:** Every reviewer includes context from the open-source repository it came from, including a link to the source repo and stats like how many times that feedback appeared and the repo’s popularity. This transparency helps you trust the guidance – it’s based on patterns that occurred in high-quality projects (e.g. a prompt might note **9** prior comments advocating a rule in a project with **16k⭐** on GitHub). In short, these AI prompts encapsulate community-agreed best practices.

* **Easy Integration in Developer Workflows:** Using an Awesome Reviewer prompt is as simple as copy-pasting its text into your AI tool of choice. You can prepend the prompt as a **system** or **agent** instruction in chat-based coding assistants (like VS Code’s AI extensions, ChatGPT, Cursor IDE, or Claude) to guide the AI’s code review. The prompts are written to be **IDE-ready** – no extra formatting needed. Just pick a prompt that matches your review focus (for example, “Never commit secrets” for a security review, or “Optimize memory access” for a performance review) and let your AI reviewer follow those guidelines.

* **Searchable Library with Filters:** The entire prompt library is available on the [Awesome Reviewers site](https://awesomereviewers.com) with a fast UI for browsing. You can **search** by keywords or **filter** prompts by category, repository source, or programming language. This makes it easy to find, say, all JavaScript-related testing prompts or all prompts about documentation in Python projects. Each prompt card on the site shows its title, origin repo, comment count, star count, a short description, and tags for category/language for quick scanning.

* **One-Click Deployment with Baz:** For an even smoother experience, you can run these reviewer agents automatically on your pull requests using **[Baz](https://baz.co)**. The site includes a **“🚀 Deploy to baz”** button that lets you spin up the selected reviewer as an AI code review bot in a single click. Baz is a platform for agentic code reviews, and with this integration it can apply the Awesome Reviewers prompts to your PRs without any manual copy-paste. In other words, you get automated code review comments on your GitHub PRs based on the same proven guidelines (with no configuration needed beyond the click). *This is a nod to how Awesome Reviewers works hand-in-hand with Baz to supercharge developer workflows.*

## Getting Started

Using **Awesome Reviewers** is straightforward:

1. **Browse the Library:** Visit [awesomereviewers.com](https://awesomereviewers.com) to view the list of available reviewer prompts. You can search or filter to find a prompt that fits your needs (e.g. *“SQL Injection Check”* under Security, or *“Documentation consistency standards”* under Documentation).

2. **Copy a Prompt:** Click on a reviewer to view the full prompt text and guidelines. Copy the prompt text provided. Each prompt typically consists of a set of guidelines or rules that an AI should follow when reviewing code (written in clear, checklist-style instructions).

3. **Use in Your AI Tool:** Paste the copied prompt into your AI code reviewer as a **system message** or initial instruction. For example:

   * **VS Code**: If using an AI extension (like GitHub Copilot Chat or ChatGPT VS Code extension), paste the prompt at the start of the conversation or as the system role content if supported.
   * **Cursor** (or other IDEs with AI chat): Provide the prompt in the tool’s AI chat before asking it to review your code/PR.
   * **ChatGPT/Claude**: Start a new chat, paste the prompt, then follow it with your code or description of the PR for review.

   The AI will then analyze your code changes according to the guidelines in the prompt, giving focused feedback (e.g. pointing out secret tokens in code if you used the *Never commit secrets* prompt, or checking for clarity and formatting if using a documentation prompt).

4. **Review AI Feedback:** The suggestions from the AI should reflect the best practices from the prompt. You can iteratively refine your code with these suggestions. Feel free to combine multiple prompts or use different ones for different aspects of the review.

5. **(Optional) Deploy with Baz:** If you use the [Baz platform](https://baz.co) for CI, you can deploy a reviewer directly. Clicking **“Deploy to baz”** on a prompt will connect it with your Baz account, so that Baz’s AI will automatically apply that reviewer to your future pull requests. This is ideal for teams wanting to enforce certain standards on every PR – the reviewer agent will leave comments on your GitHub PR just like a human reviewer, but powered by the prompt’s rules.

No installation or CLI is required to use Awesome Reviewers – the content is readily accessible. If you prefer not to use the website UI, you can also find all prompt files in the GitHub repo’s `_reviewers/` directory for direct viewing or copying.

## Acknowledgments

This project is maintained by the team at [**Baz**](https://baz.co) as part of our mission to make **Agentic code reviews** accessible to every developer. The initial set of prompts was generated by analyzing countless code review comments across many repositories – thanks to those open source communities for their feedback which formed the basis of these guidelines. We hope Awesome Reviewers helps you ship higher-quality code faster with a little help from AI. Happy coding and reviewing! 🚀

## Disclaimer
Baz projects are community-contributed and while we strive to maintain high quality, we cannot guarantee the accuracy, completeness, or security of all library documentation. Prompts listed in this repo are inspired by their respective code owners, not by Baz. If you encounter any suspicious, inappropriate, or potentially harmful content, please open an issue in thie repo. We take all reports seriously and will review flagged content promptly to maintain the integrity and safety of our platform. By using Awesome Reviewers, you acknowledge that you do so at your own discretion and risk.
