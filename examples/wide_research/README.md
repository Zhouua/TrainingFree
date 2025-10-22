# Wide Research Example

This example implements the ["Wide Research"](https://manus.im/blog/introducing-wide-research) proposed by Manus. It demonstrates a powerful pattern where a single, primary agent uses a custom tool to delegate and parallelize work.

This approach presents a simpler architecture compared to the `research` example, as the main control flow remains with one agent.

## How it Works

The architecture consists of a primary agent that is given a special, powerful tool:

1.  **`PlannerAgent`**: A single `SimpleAgent` acts as the main entry point. It analyzes the user's research query. Based on its instructions, it can either perform simple searches itself or, if it identifies a task that can be broken down into many similar sub-tasks, it will call its special tool.

2.  **`wide_research` Tool**: This is a custom `function_tool` provided to the `PlannerAgent`. Its purpose is to execute a batch of homogeneous sub-tasks in parallel. When called by the planner, this tool dynamically creates numerous short-lived `SearcherAgent` instances.

3.  **`SearcherAgent`**: These are simple, ephemeral agents created on-the-fly by the `wide_research` tool. Each one is responsible for executing a single sub-task (e.g., looking up one specific item) and returning the result. The `asyncio` library is used to run all these agents concurrently.

## Key Concepts

- **Tool-based Parallelism**: This example encapsulates complex parallel logic within a single tool. The main agent doesn't manage multiple agents; it simply calls a tool, which handles the concurrent execution internally. This simplifies the primary agent's logic.
- **Dynamic Agent Creation**: The `SearcherAgent`s are not persistent. They are created, used, and discarded on-demand by the `wide_research` tool, showcasing a flexible pattern for handling bursty, parallel workloads.
