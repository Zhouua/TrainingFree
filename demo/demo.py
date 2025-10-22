import agents as ag

from utu.agents import SimpleAgent
from utu.config import ConfigLoader
from utu.ui.gradio_chatbot import GradioChatbot


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


config = ConfigLoader.load_agent_config("base")
config.max_turns = 100


def main():
    simple_agent = SimpleAgent(config=config, name="gradio-demo", tools=[fibonacci])

    chatbot = GradioChatbot(
        simple_agent,
        example_query="斐波那契数列的第10个数是多少？记这个数为x，数列的第x个数是多少？",
    )
    chatbot.launch(port=8848)


if __name__ == "__main__":
    main()
