---
title: Tool Loop Output Contract
description: When implementing tool-using LLM agent nodes (e.g., LangGraph/LangChain
  multi-agent flows), standardize a “tool loop → finalize only when tools are done”
  contract.
repository: TauricResearch/TradingAgents
label: AI
language: Python
comments_count: 3
repository_stars: 71953
---

When implementing tool-using LLM agent nodes (e.g., LangGraph/LangChain multi-agent flows), standardize a “tool loop → finalize only when tools are done” contract.

**What to do**
1. Build a node that:
   - Creates a `tools` list.
   - Builds a `ChatPromptTemplate` with a strong `system_message` that includes a coordination stop signal (e.g., `FINAL PREDICTION: **YES/NO**`) and any required output formatting instructions (e.g., “append a Markdown table”).
   - Injects required context with `partial(...)` (at minimum: `tool_names`, `current_date`/trade date, `market_id`, `market_question`).
2. Bind tools and execute:
   - `chain = prompt | llm.bind_tools(tools)`
   - `result = chain.invoke(state["messages"])`
3. **Finalize output only on the non-tool invocation**:
   - Populate `report` only when `len(result.tool_calls) == 0` (because the graph will re-invoke the node after tools complete).

**Example pattern**
```python
def agent_node(state, llm):
    current_date = state["trade_date"]
    market_id = state["market_id"]
    market_question = state["market_question"]

    tools = [get_news, search_markets]

    system_message = (
        "You are a <Role> for prediction markets..."
        " If you or any other assistant has the FINAL PREDICTION: **YES/NO**"
        " prefix your response with FINAL PREDICTION: **YES/NO** so the team knows to stop."
        " Make sure to append a Markdown table at the end of the report."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "... {tool_names}...\n{system_message}"
                   " For your reference, the current date is {current_date}."
                   " Market ID: {market_id}. Question: {market_question}"),
        MessagesPlaceholder(variable_name="messages"),
    ])

    prompt = prompt.partial(
        system_message=system_message,
        tool_names=", ".join([t.name for t in tools]),
        current_date=current_date,
        market_id=market_id,
        market_question=market_question,
    )

    chain = prompt | llm.bind_tools(tools)
    result = chain.invoke(state["messages"])

    report = ""
    if len(result.tool_calls) == 0:  # finalize only when tools are complete
        report = result.content

    return report
```

**Secondary process rule**: Keep changes focused—don’t remove or refactor upstream/shared code in the same PR as an unrelated feature; move housekeeping to a separate PR.