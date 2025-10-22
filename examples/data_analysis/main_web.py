import pathlib

from examples.data_analysis.planner import DAPlannerAgent
from utu.agents import OrchestraAgent
from utu.config import ConfigLoader
from utu.ui import ExampleConfig
from utu.ui.webui_chatbot import WebUIChatbot


def main():
    env_and_args = ExampleConfig()
    # Set up the agent
    config = ConfigLoader.load_agent_config("examples/data_analysis")
    config.planner_config["examples_path"] = pathlib.Path(__file__).parent / "planner_examples_data.json"
    config.reporter_config["template_path"] = pathlib.Path(__file__).parent / "web_reporter_sp.j2"
    runner = OrchestraAgent(config)
    planner = DAPlannerAgent(config)
    # await runner.build()
    runner.set_planner(planner)

    # Run the agent with a sample question
    # data from https://www.kaggle.com/datasets/joannanplkrk/its-raining-cats
    fn = pathlib.Path(__file__).parent / "data" / "cat_breeds_clean.csv"

    question = f"请分析位于`{fn}`的猫品种数据，提取有价值的信息。"
    ui = WebUIChatbot(runner, example_query=question)

    ui.launch(port=env_and_args.port, ip=env_and_args.ip, autoload=env_and_args.autoload)


if __name__ == "__main__":
    main()
