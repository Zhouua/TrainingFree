from utu.agents import SimpleAgent
from utu.config import ConfigLoader
from utu.ui import ExampleConfig
from utu.ui.webui_chatbot import WebUIChatbot

EXAMPLE_QUERY = (
    "整理一下当前文件夹下面的所有文件，按照 学号-姓名 的格式重命名。"
    "我只接受学生提交的pdf，如果不是pdf文件，归档到一个文件夹里面。"
)


config = ConfigLoader.load_agent_config("examples/file_manager")
worker_agent = SimpleAgent(config=config)


def main_gradio():
    env_and_args = ExampleConfig()
    chatbot = WebUIChatbot(worker_agent, example_query=EXAMPLE_QUERY)
    chatbot.launch(port=env_and_args.port, ip=env_and_args.ip, autoload=env_and_args.autoload)


if __name__ == "__main__":
    main_gradio()
