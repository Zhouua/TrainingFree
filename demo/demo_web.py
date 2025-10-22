import agents as ag

from utu.agents import SimpleAgent
from utu.config import ConfigLoader
from utu.ui.webui_chatbot import WebUIChatbot


@ag.function_tool
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


config = ConfigLoader.load_agent_config("examples/base")
config.max_turns = 100


def main():
    simple_agent = SimpleAgent(config=config, name="demo", tools=[fibonacci])

    chatbot = WebUIChatbot(
        simple_agent,
        example_query="斐波那契数列的第10个数是多少？记这个数为x，数列的第x个数是多少？",
    )
    chatbot.launch(port=config.frontend_port, ip=config.frontend_ip)


if __name__ == "__main__":
    main()
