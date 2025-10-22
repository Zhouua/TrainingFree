# Deep Research Example

This example implements a "Plan-and-Execute" workflow by orchestrating three specialized `SimpleAgent` instances. It's inspired by the [research_bot example](https://github.com/openai/openai-agents-python/tree/main/examples/research_bot) from the `openai-agents` library and showcases a lightweight approach to multi-agent collaboration.

## Workflow

The process is a simple and powerful pipeline:

1.  **Plan**: The `PlannerAgent` receives the user's query and generates a `WebSearchPlan` (a list of search terms). It uses a Pydantic model for reliable, structured output.

2.  **Search**: The `SearchAgent` takes the plan and executes all web searches **in parallel** using `asyncio` and the `SearchToolkit`. It returns a concise summary for each result.

3.  **Write**: The `WriterAgent` synthesizes all search summaries into a final, detailed report, also defined with a Pydantic `ReportData` model.

This example highlights how to chain agents, pass structured data between them, and use parallelism for efficiency, providing a lightweight alternative to the formal `OrchestraAgent`.

