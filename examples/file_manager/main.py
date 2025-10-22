import asyncio

from utu.agents import SimpleAgent
from utu.config import ConfigLoader
from utu.utils import AgentsUtils

EXAMPLE_QUERY = (
    "整理一下当前文件夹下面的所有文件，按照 学号-姓名 的格式重命名。"
    "我只接受学生提交的pdf，如果不是pdf文件，归档到一个文件夹里面。"
)


config = ConfigLoader.load_agent_config("examples/file_manager")
worker_agent = SimpleAgent(config=config)


async def main_gradio():
    async with worker_agent as agent:
        res = agent.run_streamed(EXAMPLE_QUERY)
        # async for event in res.stream_events():
        #     print(event)
        await AgentsUtils.print_stream_events(res.stream_events())
        print(f"Final output: {res.final_output}")


if __name__ == "__main__":
    asyncio.run(main_gradio())
