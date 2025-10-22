# Paper Collector Example

This example demonstrates a simple, configuration-driven approach to paper analysis using the `OrchestraAgent`.

It showcases the standard "Plan-and-Execute" workflow:

- **Agent Paradigm**: It directly uses the `OrchestraAgent`, which is defined in the main configuration file `configs/examples/paper_collector.yaml`.

- **Workflow**:
    1.  A **Planner** agent creates a step-by-step plan to analyze a given paper.
    2.  **Worker** agents (`PaperSummarizeAgent` and `SearchAgent`) execute the plan's tasks, such as summarizing the paper and finding related articles.
    3.  A **Reporter** agent synthesizes the results into a final comparison report.

- **Few-Shot Planning**: The file `planner_examples_data.json` provides in-domain examples to the Planner which can improve its ability to create logical and effective plans. You can modify this file to see how the Planner's performance changes.
