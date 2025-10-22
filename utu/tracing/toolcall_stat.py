from typing import Any

from agents import Agent, RunContextWrapper, RunHooks, TContext, Tool


# TODO: log toolcall infos into db
class ToolCallStatRunHook(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper[TContext], agent: Agent[TContext]) -> None:
        pass

    async def on_agent_end(self, context: RunContextWrapper[TContext], agent: Agent[TContext], output: Any) -> None:
        pass

    async def on_handoff(
        self, context: RunContextWrapper[TContext], from_agent: Agent[TContext], to_agent: Agent[TContext]
    ) -> None:
        pass

    async def on_tool_start(self, context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool) -> None:
        pass

    async def on_tool_end(
        self, context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool, result: str
    ) -> None:
        pass
