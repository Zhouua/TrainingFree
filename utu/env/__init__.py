from ..config import AgentConfig
from ..utils import DIR_ROOT
from .base_env import BaseEnv, Env
from .browser_env import BrowserEnv
from .shell_local_env import ShellLocalEnv


async def get_env(config: AgentConfig, trace_id: str) -> Env:
    if (not config.env) or (not config.env.name):
        return BaseEnv()
    match config.env.name:
        case "base":
            return BaseEnv()
        case "shell_local":
            workspace = DIR_ROOT / "workspace" / trace_id
            workspace.mkdir(parents=True, exist_ok=True)
            print(f"> Workspace: {workspace}")
            return ShellLocalEnv(workspace)
        case "browser_docker":
            return BrowserEnv(trace_id)
        case _:
            raise ValueError(f"Unknown env name: {config.env.name}")
