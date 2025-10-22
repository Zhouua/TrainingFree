"""Example usage of MCP with SSE transport

- config: configs/agents/examples/mcp/sse_example.yaml

Usage:
    # run server
    python examples/mcp/sse_example/server.py
    # run the agent
    python examples/mcp/sse_example/main.py
"""

import asyncio

from utu.agents import SimpleAgent


async def main():
    queries = ("Add these numbers: 7 and 22.", "What's the weather in Shanghai?", "What's the secret word?")

    async with SimpleAgent(config="examples/mcp/sse_example.yaml") as agent:
        for query in queries:
            await agent.chat_streamed(query)


if __name__ == "__main__":
    asyncio.run(main())
