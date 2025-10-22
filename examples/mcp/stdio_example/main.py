"""Example usage of MCP with stdio transport

- config: configs/agents/examples/mcp/stdio_example.yaml
- env: MCP_MEMORY_FILE_PATH

Usage:
    python examples/mcp/stdio_example/main.py
"""

import asyncio

from utu.agents import SimpleAgent

# from https://en.wikipedia.org/wiki/Anthropic
DOC = """Anthropic PBC is an American artificial intelligence (AI) startup company founded in 2021.
 Anthropic has developed a family of large language models (LLMs) named Claude as a competitor to OpenAI's ChatGPT
 and Google's Gemini.[5] According to the company, it researches and develops AI to "study their safety properties
 at the technological frontier" and use this research to deploy safe models for the public.[6][7]

Anthropic was founded by former members of OpenAI, including siblings Daniela Amodei and Dario Amodei.[8]
 In September 2023, Amazon announced an investment of up to $4 billion, followed by a $2 billion commitment
 from Google in the following month.[9][10][11]"""
queries = [
    "What's the current time?",
    f"Add memory: {DOC}",
    "Who are the founders of Anthropic?",
]


async def main():
    async with SimpleAgent(
        config="examples/mcp/stdio_example",
        name="mcp_stdio_example",
    ) as agent:
        for query in queries:
            await agent.chat_streamed(query)


if __name__ == "__main__":
    asyncio.run(main())
