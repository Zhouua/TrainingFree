import asyncio
import pathlib

from utu.agents import OrchestraAgent
from utu.config import ConfigLoader
from utu.utils import AgentsUtils


async def main():
    config = ConfigLoader.load_agent_config("examples/svg_generator")
    config.planner_config["examples_path"] = pathlib.Path(__file__).parent / "planner_examples.json"
    config.reporter_config["template_path"] = pathlib.Path(__file__).parent / "reporter_csv.j2"
    runner = OrchestraAgent(config)

    data_dir = pathlib.Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    question = "deepseek-v3.1有哪些亮点更新?"

    res = runner.run_streamed(question)
    await AgentsUtils.print_stream_events(res.stream_events())
    print(f"Final output: {res.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
