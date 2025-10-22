import asyncio
import pathlib
import re

from examples.data_analysis.planner import DAPlannerAgent
from utu.agents import OrchestraAgent
from utu.config import ConfigLoader


async def main():
    # Set up the agent
    config = ConfigLoader.load_agent_config("examples/data_analysis")
    config.planner_config["examples_path"] = pathlib.Path(__file__).parent / "planner_examples_data.json"
    config.reporter_config["template_path"] = pathlib.Path(__file__).parent / "web_reporter_sp.j2"
    runner = OrchestraAgent(config)
    planner = DAPlannerAgent(config)
    runner.set_planner(planner)

    # Run the agent with a sample question
    # data from https://www.kaggle.com/datasets/joannanplkrk/its-raining-cats
    fn = pathlib.Path(__file__).parent / "data" / "cat_breeds_clean.csv"
    assert fn.exists(), f"File {fn} does not exist."
    question = f"请分析位于`{fn}`的猫品种数据，提取有价值的信息。"
    result = await runner.run(question)

    # Extract and print the result
    match = re.search(r"```html(.*?)```", result.final_output, re.DOTALL)
    result = match.group(1).strip() if match else result.final_output
    print(f"Run completed with result: {result}")
    with open(fn.parent / "report.html", "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    asyncio.run(main())
