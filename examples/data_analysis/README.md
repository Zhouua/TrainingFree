# Data Analysis Example

This example showcases an advanced `OrchestraAgent` for data analysis, featuring significant customizations to the standard workflow for a more sophisticated result.

## Key Features:

- **Custom Planner (`DAPlannerAgent`):** The planner is extended to first **proactively inspect the data file's schema**. 
- **Custom HTML Reporter:** The reporter uses a custom template (`web_reporter_sp.j2`) to generate a rich, interactive HTML report.

## How to Run

1.  **Run with Python**
    ```bash
    python -m examples.data_analysis.main
    ```

2.  **Run with Web UI**
    ```bash
    python -m examples.data_analysis.main_web
    ```
