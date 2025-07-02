---
title: Optimize model token usage
description: 'Implement token-efficient patterns when working with AI models to optimize
  costs and performance. Key practices include:


  1. Batch identical prompts into single API calls where supported'
repository: langchain-ai/langchainjs
label: AI
language: Typescript
comments_count: 5
repository_stars: 15004
---

Implement token-efficient patterns when working with AI models to optimize costs and performance. Key practices include:

1. Batch identical prompts into single API calls where supported
2. Leverage provider-specific features for token efficiency
3. Use appropriate token counting methods for accurate estimation

Example of efficient batching with OpenAI:

```typescript
// Inefficient: Multiple separate calls
const results = await Promise.all(
  inputs.map(input => model.generate(input))
);

// Efficient: Single batched call
const results = await model.generate(
  [promptValue], 
  { n: inputs.length }  // OpenAI charges input tokens only once
);

// For accurate token counting:
const tokenCount = await model.getNumTokensFromMessages(messages);
```

This approach can significantly reduce costs, especially for use cases with high input token counts relative to output. Different providers may offer varying batching capabilities - consult their documentation for optimal usage patterns.


[
  {
    "discussion_id": "1561463582",
    "pr_number": 5016,
    "pr_file": "libs/langchain-openai/src/chat_models.ts",
    "created_at": "2024-04-11T18:23:48+00:00",
    "commented_code": "return this._identifyingParams();\n  }\n\n  async batch(\n    inputs: BaseLanguageModelInput[],\n    options?: CallOptions\n  ): Promise<BaseMessageChunk[]> {\n    const promptValues = inputs.map((i) =>\n      BaseChatModel._convertInputToPromptValue(i)\n    );\n\n    const promptValueStrings = promptValues.map((p) => p.toString());\n    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n      const result = await this.generatePrompt(\n        [promptValues[0]],\n        { ...options, n: inputs.length } as CallOptions,",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1561463582",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-11T18:23:48+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "We should probably upper bound this - I can handle it!",
        "pr_file_module": null
      },
      {
        "comment_id": "1561507605",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-11T18:56:12+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Does this have the same output as just sending `n` requests? Or will it pick the top `n` candidates?",
        "pr_file_module": null
      },
      {
        "comment_id": "1561586595",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-11T20:07:29+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Hey so chatted with the Python folks - this would change the tracing behavior for folks, and they have some concerns about overall behavior changing since it's a black box on OpenAI's end.\r\n\r\nCould we table it for now? Sorry for the thrash - you can always wrap a `.generate()` call in a lambda.",
        "pr_file_module": null
      },
      {
        "comment_id": "1562397961",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-12T11:01:59+00:00",
        "comment_author": "davidfant",
        "comment_body": "> Does this have the same output as just sending `n` requests? Or will it pick the top `n` candidates?\r\n\r\nYes, this makes OpenAI create `n` independent results for the same prompt. `best_of` would return top candidates based on log probs\r\nhttps://platform.openai.com/docs/api-reference/chat/create\r\n\r\n> Hey so chatted with the Python folks - this would change the tracing behavior for folks, and they have some concerns about overall behavior changing since it's a black box on OpenAI's end.\r\n> \r\n> Could we table it for now? Sorry for the thrash - you can always wrap a `.generate()` call in a lambda.\r\n\r\nOk. FWIW here are my 2c:\r\n* I don't really get the point with \"concerns about overall behavior\". The samples are generated independently, with the benefit of only paying for input tokens once.\r\n* Pricing-wise the difference is huge, esp for use cases with lots of input and limited output. For us, we have lots of input tokens and not so many output tokens (relatively speaking), so not using `n` would be not great\r\n* IMO the tracing behavior is changed for the better, at least in terms of how this is visualized in LS\r\n* The goal with adding this to ChatOpenAI.batch (rather than hackily accomplishing the same thing with generate) is to avoid having lots of different logic for how to do requests depending on what model provider is used. Basically I've abstracted out model in my runnables so that they're given `model: BaseChatModel`, which lets me easily configure what model to use from one place.\r\n\r\nIf this still isn't a change that doesn't make sense on your end, I'll just apply a patch locally for now.",
        "pr_file_module": null
      },
      {
        "comment_id": "1562496158",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-12T12:40:30+00:00",
        "comment_author": "functorism",
        "comment_body": "OpenAI supporting `n` completions is a very high value feature, because of the fact that input tokens are priced only once. If you make `n` separate requests you eat the input token costs `n` times. This is an amazing aspect of the OpenAI pricing model, which many other providers don't support (for example Anthropic). I believe making it easy for users to benefit from this, even if they don't know about it is a great value add LangChain can provide.\r\n\r\nOpenAI supports the `best_of` option, which has interplay with `n`.\r\n\r\n> Generates best_of completions server-side and returns the \"best\" (the one with the highest log probability per token). Results cannot be streamed.\r\n\r\nUsers can also do this themselves now that chat completions return `logprobs`. It's a common pattern in my workflows to increase temperature for higher generation variance and utilizing the `logprobs` or simply doing self-consistency voting (https://arxiv.org/abs/2203.11171). The OpenAI pricing model has great synergy with these techniques, since you only pay extra for your generations.\r\n\r\nI would almost argue that this feature of the API enables quality improving techniques where they would otherwise be cost prohibitive, and think leaning in and making these as easy to use as possible is of immense value.",
        "pr_file_module": null
      },
      {
        "comment_id": "1562941800",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5016,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "1561463582",
        "commented_code": "@@ -627,6 +629,29 @@ export class ChatOpenAI<\n     return this._identifyingParams();\n   }\n \n+  async batch(\n+    inputs: BaseLanguageModelInput[],\n+    options?: CallOptions\n+  ): Promise<BaseMessageChunk[]> {\n+    const promptValues = inputs.map((i) =>\n+      BaseChatModel._convertInputToPromptValue(i)\n+    );\n+\n+    const promptValueStrings = promptValues.map((p) => p.toString());\n+    if (promptValueStrings.every((p) => p === promptValueStrings[0])) {\n+      const result = await this.generatePrompt(\n+        [promptValues[0]],\n+        { ...options, n: inputs.length } as CallOptions,",
        "comment_created_at": "2024-04-12T17:41:42+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "I'll figure it out on our end and get this merged. Thanks for weighing in!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1912116237",
    "pr_number": 7505,
    "pr_file": "examples/src/tools/google_calendar.ts",
    "created_at": "2025-01-11T17:42:40+00:00",
    "commented_code": "import { initializeAgentExecutorWithOptions } from \"langchain/agents\";\nimport { OpenAI } from \"@langchain/openai\";\nimport { AgentExecutor, createOpenAIToolsAgent } from \"langchain/agents\";\nimport { pull } from \"langchain/hub\";\nimport { OpenAI, ChatOpenAI } from \"@langchain/openai\";\nimport { Calculator } from \"@langchain/community/tools/calculator\";\nimport {\n  GoogleCalendarCreateTool,\n  GoogleCalendarViewTool,\n} from \"@langchain/community/tools/google_calendar\";\nimport { ChatPromptTemplate } from \"@langchain/core/prompts\";\n\nexport async function run() {\n  const model = new OpenAI({",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1912116237",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7505,
        "pr_file": "examples/src/tools/google_calendar.ts",
        "discussion_id": "1912116237",
        "commented_code": "@@ -1,10 +1,12 @@\n-import { initializeAgentExecutorWithOptions } from \"langchain/agents\";\n-import { OpenAI } from \"@langchain/openai\";\n+import { AgentExecutor, createOpenAIToolsAgent } from \"langchain/agents\";\n+import { pull } from \"langchain/hub\";\n+import { OpenAI, ChatOpenAI } from \"@langchain/openai\";\n import { Calculator } from \"@langchain/community/tools/calculator\";\n import {\n   GoogleCalendarCreateTool,\n   GoogleCalendarViewTool,\n } from \"@langchain/community/tools/google_calendar\";\n+import { ChatPromptTemplate } from \"@langchain/core/prompts\";\n \n export async function run() {\n   const model = new OpenAI({",
        "comment_created_at": "2025-01-11T17:42:40+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Let's use `ChatOpenAI` with `model: \"gpt-4o-mini\"` for everything, `OpenAI` completions models are deprecated",
        "pr_file_module": null
      },
      {
        "comment_id": "1912356961",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7505,
        "pr_file": "examples/src/tools/google_calendar.ts",
        "discussion_id": "1912116237",
        "commented_code": "@@ -1,10 +1,12 @@\n-import { initializeAgentExecutorWithOptions } from \"langchain/agents\";\n-import { OpenAI } from \"@langchain/openai\";\n+import { AgentExecutor, createOpenAIToolsAgent } from \"langchain/agents\";\n+import { pull } from \"langchain/hub\";\n+import { OpenAI, ChatOpenAI } from \"@langchain/openai\";\n import { Calculator } from \"@langchain/community/tools/calculator\";\n import {\n   GoogleCalendarCreateTool,\n   GoogleCalendarViewTool,\n } from \"@langchain/community/tools/google_calendar\";\n+import { ChatPromptTemplate } from \"@langchain/core/prompts\";\n \n export async function run() {\n   const model = new OpenAI({",
        "comment_created_at": "2025-01-12T03:35:50+00:00",
        "comment_author": "ucev",
        "comment_body": "done. Cuz `ChatOpenAI` inherits `BaseChatModel`, not `BaseLLM`, I also update google_calendar type definitions.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1744568491",
    "pr_number": 6674,
    "pr_file": "examples/src/llms/arcjet.ts",
    "created_at": "2024-09-04T22:08:47+00:00",
    "commented_code": "import {\n  ArcjetRedact\n} from \"@langchain/community/llms/arcjet\";\nimport { OpenAI } from \"@langchain/openai\";\n\n// Create an instance of another LLM for Arcjet to wrap\nconst openai = new OpenAI({",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1744568491",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6674,
        "pr_file": "examples/src/llms/arcjet.ts",
        "discussion_id": "1744568491",
        "commented_code": "@@ -0,0 +1,42 @@\n+import {\n+  ArcjetRedact\n+} from \"@langchain/community/llms/arcjet\";\n+import { OpenAI } from \"@langchain/openai\";\n+\n+// Create an instance of another LLM for Arcjet to wrap\n+const openai = new OpenAI({",
        "comment_created_at": "2024-09-04T22:08:47+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "We probably will want this to work with chat models - most state of the art models are chat models rather than LLMs.",
        "pr_file_module": null
      },
      {
        "comment_id": "1745775580",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6674,
        "pr_file": "examples/src/llms/arcjet.ts",
        "discussion_id": "1744568491",
        "commented_code": "@@ -0,0 +1,42 @@\n+import {\n+  ArcjetRedact\n+} from \"@langchain/community/llms/arcjet\";\n+import { OpenAI } from \"@langchain/openai\";\n+\n+// Create an instance of another LLM for Arcjet to wrap\n+const openai = new OpenAI({",
        "comment_created_at": "2024-09-05T15:36:08+00:00",
        "comment_author": "e-moran",
        "comment_body": "We are planning on adding a second integration for chat models, I'm planning on adding that in a second PR though since it is a separate piece of work but I'm happy to add it to this PR if you think that would be better.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1375277963",
    "pr_number": 2891,
    "pr_file": "langchain/src/chat_models/openai.ts",
    "created_at": "2023-10-28T16:20:15+00:00",
    "commented_code": "}\n  }\n\n  async getNumTokensFromMessages(messages: BaseMessage[]): Promise<{\n    totalCount: number;\n    countPerMessage: number[];\n  }> {\n  /**\n   * Estimate the number of tokens a prompt will use.\n   * Modified from: https://github.com/hmarr/openai-chat-tokens/blob/main/src/index.ts\n   */\n  private async getNumTokensFromPrompt(\n    messages: BaseMessage[],\n    functions?: OpenAIFnDef[],\n    function_call?: \"none\" | \"auto\" | OpenAIFnCallOption\n  ): Promise<number> {\n    // It appears that if functions are present, the first system message is padded with a trailing newline. This\n    // was inferred by trying lots of combinations of messages and functions and seeing what the token counts were.\n    // let paddedSystem = false;\n    const openaiMessages = messages.map((m) => messageToOpenAIMessage(m));\n\n    let tokens = (await this.getNumTokensFromMessages(messages)).totalCount;\n\n    // If there are functions, add the function definitions as they count towards token usage\n    if (functions && function_call !== \"auto\") {\n      const promptDefinitions = formatFunctionDefinitions(\n        functions as unknown as FunctionDef[]\n      );\n      tokens += await this.getNumTokens(promptDefinitions);\n      tokens += 9; // Add nine per completion\n    }\n\n    // If there's a system message _and_ functions are present, subtract four tokens. I assume this is because\n    // functions typically add a system message, but reuse the first one if it's already there. This offsets\n    // the extra 9 tokens added by the function definitions.\n    if (functions && openaiMessages.find((m) => m.role === \"system\")) {\n      tokens -= 4;\n    }\n\n    // If function_call is 'none', add one token.\n    // If it's a FunctionCall object, add 4 + the number of tokens in the function name.\n    // If it's undefined or 'auto', don't add anything.\n    if (function_call === \"none\") {\n      tokens += 1;\n    } else if (typeof function_call === \"object\") {\n      tokens += (await this.getNumTokens(function_call.name)) + 4;\n    }\n\n    return tokens;\n  }\n\n  /**\n   * Estimate the number of tokens an array of generations have used.\n   */\n  private async getNumTokensFromGenerations(generations: ChatGeneration[]) {\n    const generationUsages = await Promise.all(\n      generations.map(async (generation) => {\n        const openAIMessage = messageToOpenAIMessage(generation.message);\n        if (openAIMessage.function_call) {\n          return (await this.getNumTokensFromMessages([generation.message]))\n            .countPerMessage[0];\n        } else {\n          return await this.getNumTokens(generation.message.content);\n        }\n      })\n    );\n\n    return generationUsages.reduce((a, b) => a + b, 0);\n  }\n\n  async getNumTokensFromMessages(messages: BaseMessage[]) {\n    let totalCount = 0;\n    let tokensPerMessage = 0;\n    let tokensPerName = 0;\n\n    // From: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb\n    if (getModelNameForTiktoken(this.modelName) === \"gpt-3.5-turbo\") {\n    if (this.modelName === \"gpt-3.5-turbo-0301\") {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1375277963",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 2891,
        "pr_file": "langchain/src/chat_models/openai.ts",
        "discussion_id": "1375277963",
        "commented_code": "@@ -523,19 +563,79 @@ export class ChatOpenAI<\n     }\n   }\n \n-  async getNumTokensFromMessages(messages: BaseMessage[]): Promise<{\n-    totalCount: number;\n-    countPerMessage: number[];\n-  }> {\n+  /**\n+   * Estimate the number of tokens a prompt will use.\n+   * Modified from: https://github.com/hmarr/openai-chat-tokens/blob/main/src/index.ts\n+   */\n+  private async getNumTokensFromPrompt(\n+    messages: BaseMessage[],\n+    functions?: OpenAIFnDef[],\n+    function_call?: \"none\" | \"auto\" | OpenAIFnCallOption\n+  ): Promise<number> {\n+    // It appears that if functions are present, the first system message is padded with a trailing newline. This\n+    // was inferred by trying lots of combinations of messages and functions and seeing what the token counts were.\n+    // let paddedSystem = false;\n+    const openaiMessages = messages.map((m) => messageToOpenAIMessage(m));\n+\n+    let tokens = (await this.getNumTokensFromMessages(messages)).totalCount;\n+\n+    // If there are functions, add the function definitions as they count towards token usage\n+    if (functions && function_call !== \"auto\") {\n+      const promptDefinitions = formatFunctionDefinitions(\n+        functions as unknown as FunctionDef[]\n+      );\n+      tokens += await this.getNumTokens(promptDefinitions);\n+      tokens += 9; // Add nine per completion\n+    }\n+\n+    // If there's a system message _and_ functions are present, subtract four tokens. I assume this is because\n+    // functions typically add a system message, but reuse the first one if it's already there. This offsets\n+    // the extra 9 tokens added by the function definitions.\n+    if (functions && openaiMessages.find((m) => m.role === \"system\")) {\n+      tokens -= 4;\n+    }\n+\n+    // If function_call is 'none', add one token.\n+    // If it's a FunctionCall object, add 4 + the number of tokens in the function name.\n+    // If it's undefined or 'auto', don't add anything.\n+    if (function_call === \"none\") {\n+      tokens += 1;\n+    } else if (typeof function_call === \"object\") {\n+      tokens += (await this.getNumTokens(function_call.name)) + 4;\n+    }\n+\n+    return tokens;\n+  }\n+\n+  /**\n+   * Estimate the number of tokens an array of generations have used.\n+   */\n+  private async getNumTokensFromGenerations(generations: ChatGeneration[]) {\n+    const generationUsages = await Promise.all(\n+      generations.map(async (generation) => {\n+        const openAIMessage = messageToOpenAIMessage(generation.message);\n+        if (openAIMessage.function_call) {\n+          return (await this.getNumTokensFromMessages([generation.message]))\n+            .countPerMessage[0];\n+        } else {\n+          return await this.getNumTokens(generation.message.content);\n+        }\n+      })\n+    );\n+\n+    return generationUsages.reduce((a, b) => a + b, 0);\n+  }\n+\n+  async getNumTokensFromMessages(messages: BaseMessage[]) {\n     let totalCount = 0;\n     let tokensPerMessage = 0;\n     let tokensPerName = 0;\n \n     // From: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb\n-    if (getModelNameForTiktoken(this.modelName) === \"gpt-3.5-turbo\") {\n+    if (this.modelName === \"gpt-3.5-turbo-0301\") {",
        "comment_created_at": "2023-10-28T16:20:15+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Do you have a source for this change? ",
        "pr_file_module": null
      },
      {
        "comment_id": "1375331056",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 2891,
        "pr_file": "langchain/src/chat_models/openai.ts",
        "discussion_id": "1375277963",
        "commented_code": "@@ -523,19 +563,79 @@ export class ChatOpenAI<\n     }\n   }\n \n-  async getNumTokensFromMessages(messages: BaseMessage[]): Promise<{\n-    totalCount: number;\n-    countPerMessage: number[];\n-  }> {\n+  /**\n+   * Estimate the number of tokens a prompt will use.\n+   * Modified from: https://github.com/hmarr/openai-chat-tokens/blob/main/src/index.ts\n+   */\n+  private async getNumTokensFromPrompt(\n+    messages: BaseMessage[],\n+    functions?: OpenAIFnDef[],\n+    function_call?: \"none\" | \"auto\" | OpenAIFnCallOption\n+  ): Promise<number> {\n+    // It appears that if functions are present, the first system message is padded with a trailing newline. This\n+    // was inferred by trying lots of combinations of messages and functions and seeing what the token counts were.\n+    // let paddedSystem = false;\n+    const openaiMessages = messages.map((m) => messageToOpenAIMessage(m));\n+\n+    let tokens = (await this.getNumTokensFromMessages(messages)).totalCount;\n+\n+    // If there are functions, add the function definitions as they count towards token usage\n+    if (functions && function_call !== \"auto\") {\n+      const promptDefinitions = formatFunctionDefinitions(\n+        functions as unknown as FunctionDef[]\n+      );\n+      tokens += await this.getNumTokens(promptDefinitions);\n+      tokens += 9; // Add nine per completion\n+    }\n+\n+    // If there's a system message _and_ functions are present, subtract four tokens. I assume this is because\n+    // functions typically add a system message, but reuse the first one if it's already there. This offsets\n+    // the extra 9 tokens added by the function definitions.\n+    if (functions && openaiMessages.find((m) => m.role === \"system\")) {\n+      tokens -= 4;\n+    }\n+\n+    // If function_call is 'none', add one token.\n+    // If it's a FunctionCall object, add 4 + the number of tokens in the function name.\n+    // If it's undefined or 'auto', don't add anything.\n+    if (function_call === \"none\") {\n+      tokens += 1;\n+    } else if (typeof function_call === \"object\") {\n+      tokens += (await this.getNumTokens(function_call.name)) + 4;\n+    }\n+\n+    return tokens;\n+  }\n+\n+  /**\n+   * Estimate the number of tokens an array of generations have used.\n+   */\n+  private async getNumTokensFromGenerations(generations: ChatGeneration[]) {\n+    const generationUsages = await Promise.all(\n+      generations.map(async (generation) => {\n+        const openAIMessage = messageToOpenAIMessage(generation.message);\n+        if (openAIMessage.function_call) {\n+          return (await this.getNumTokensFromMessages([generation.message]))\n+            .countPerMessage[0];\n+        } else {\n+          return await this.getNumTokens(generation.message.content);\n+        }\n+      })\n+    );\n+\n+    return generationUsages.reduce((a, b) => a + b, 0);\n+  }\n+\n+  async getNumTokensFromMessages(messages: BaseMessage[]) {\n     let totalCount = 0;\n     let tokensPerMessage = 0;\n     let tokensPerName = 0;\n \n     // From: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb\n-    if (getModelNameForTiktoken(this.modelName) === \"gpt-3.5-turbo\") {\n+    if (this.modelName === \"gpt-3.5-turbo-0301\") {",
        "comment_created_at": "2023-10-28T22:53:13+00:00",
        "comment_author": "wlyh514",
        "comment_body": "From section 6 of [the linked jupyter notebook](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb), in the function definition of `num_tokens_from_messages` it states that `token_per_message = 4` and `token_per_name = -1` only applies for the 'gpt-3.5-turbo-0301' model, and not other gpt-3.5 models. Testing this function on `gpt-3.5-turbo` and `gpt-3.5-turbo-0301` also yield correct results with this change. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1204888837",
    "pr_number": 659,
    "pr_file": "examples/src/retrievers/pinecone_hybrid.ts",
    "created_at": "2023-05-25T00:55:49+00:00",
    "commented_code": "import { PineconeClient } from \"@pinecone-database/pinecone\";\nimport { BertTokenizer } from \"bert-tokenizer\";\n\nimport { OpenAIEmbeddings } from \"langchain/embeddings\";\nimport { PineconeHybridSearchRetriever } from \"langchain/retrievers\";\n\nexport const run = async () => {\n  const client = new PineconeClient();\n\n  await client.init({\n    environment: process.env.PINECONE_ENVIRONMENT!,\n    apiKey: process.env.PINECONE_API_KEY!,\n  });\n\n  const embeddings = new OpenAIEmbeddings();\n  const pineconeIndex = client.Index(process.env.PINECONE_INDEX!);\n\n  const tokenizer = new BertTokenizer(undefined, true, 512);",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1204888837",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 659,
        "pr_file": "examples/src/retrievers/pinecone_hybrid.ts",
        "discussion_id": "1204888837",
        "commented_code": "@@ -0,0 +1,30 @@\n+import { PineconeClient } from \"@pinecone-database/pinecone\";\n+import { BertTokenizer } from \"bert-tokenizer\";\n+\n+import { OpenAIEmbeddings } from \"langchain/embeddings\";\n+import { PineconeHybridSearchRetriever } from \"langchain/retrievers\";\n+\n+export const run = async () => {\n+  const client = new PineconeClient();\n+\n+  await client.init({\n+    environment: process.env.PINECONE_ENVIRONMENT!,\n+    apiKey: process.env.PINECONE_API_KEY!,\n+  });\n+\n+  const embeddings = new OpenAIEmbeddings();\n+  const pineconeIndex = client.Index(process.env.PINECONE_INDEX!);\n+\n+  const tokenizer = new BertTokenizer(undefined, true, 512);",
        "comment_created_at": "2023-05-25T00:55:49+00:00",
        "comment_author": "dqbd",
        "comment_body": "Consider using `js-tiktoken` instead, which should already be a required dependency. ",
        "pr_file_module": null
      }
    ]
  }
]
