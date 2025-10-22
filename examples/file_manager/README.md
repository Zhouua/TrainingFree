# File Manager Example

This example showcases a `SimpleAgent` that organizes local files. It's a practical demonstration of using an agent for file system tasks, accessible through a `Gradio` web UI.

**Warning**: This agent can modify and delete files. It is configured to work *only* in a safe `/tmp/file_manager_test` directory. If you change the configuration to use a custom path, **back up your data first**.

## How to Run

**1. Prepare Workspace**

First, create a safe workspace with sample files by running:
```bash
python -m examples.file_manager.prepare_messy_files
```

**2. Launch UI**

Next, start the Gradio web interface:
```bash
python -m examples.file_manager.main_web
```

Then, open the web UI and give the agent a task.