"""
@ii-agent/src/ii_agent/tools/memory/
"""

from typing import Literal

from ..config import ToolkitConfig
from ..utils import get_logger
from .base import AsyncBaseToolkit, register_tool

logger = get_logger(__name__)


class SimpleMemoryToolkit(AsyncBaseToolkit):
    """String-based memory tool for storing and modifying persistent text.

    This tool maintains a single in-memory string that can be read,
    replaced, or selectively edited using string replacement. It provides safety
    warnings when overwriting content or when edit operations would affect
    multiple occurrences.
    """

    def __init__(self, config: ToolkitConfig = None) -> None:
        super().__init__(config)
        self.full_memory = ""

    def _read_memory(self) -> str:
        """Read the current memory contents."""
        return self.full_memory

    def _write_memory(self, content: str) -> str:
        """Replace the entire memory with new content."""
        if self.full_memory:
            previous = self.full_memory
            self.full_memory = content
            return (
                f"Warning: Overwriting existing content. Previous content was:\n{previous}\n\n"
                "Memory has been updated successfully."
            )
        self.full_memory = content
        return "Memory updated successfully."

    def _edit_memory(self, old_string: str, new_string: str) -> str:
        """Replace occurrences of old string with new string."""
        if old_string not in self.full_memory:
            return f"Error: '{old_string}' not found in memory."

        old_memory = self.full_memory
        count = old_memory.count(old_string)

        if count > 1:
            return (
                f"Warning: Found {count} occurrences of '{old_string}'. "
                "Please confirm which occurrence to replace or use more specific context."
            )

        self.full_memory = self.full_memory.replace(old_string, new_string)
        return "Edited memory: 1 occurrence replaced."

    @register_tool
    async def simple_memory(
        self, action: Literal["read", "write", "edit"], content: str = "", old_string: str = "", new_string: str = ""
    ) -> str:
        """Tool for managing persistent text memory with read, write and edit operations.

        MEMORY STORAGE GUIDANCE:
        Store information that needs to persist across agent interactions, including:
        - User context: Requirements, goals, preferences, and clarifications
        - Task state: Completed tasks, pending items, current progress
        - Code context: File paths, function signatures, data structures, dependencies
        - Research findings: Key facts, sources, URLs, and reference materials
        - Configuration: Settings, parameters, and environment details
        - Cross-session continuity: Information needed for future interactions

        OPERATIONS:
        - Read: Retrieves full memory contents as a string
        - Write: Replaces entire memory (warns when overwriting existing data)
        - Edit: Performs targeted string replacement (warns on multiple matches)

        Use structured formats (JSON, YAML, or clear sections) for complex data.
        Prioritize information that would be expensive to regenerate or re-research.

        Args:
            action (Literal["read", "write", "edit"]: The action to perform on the memory.
            content (str, optional): The content to write to the memory. Defaults to "".
            old_string (str, optional): The string to replace in the memory. Defaults to "".
            new_string (str, optional): The string to replace the old string with in the memory. Defaults to "".
        """
        if action == "read":
            result = self._read_memory()
        elif action == "write":
            result = self._write_memory(content)
        elif action == "edit":
            result = self._edit_memory(old_string, new_string)
        else:
            result = f"Error: Unknown action '{action}'. Valid actions are read, write, edit."
        return result


class CompactifyMemoryToolkit(AsyncBaseToolkit):
    """Memory compactification tool that works with any context manager type.

    Applies the context manager's truncation strategy to compress the conversation history.
    This tool adapts to different context management approaches (summarization, simple truncation, etc.).
    """

    async def compactify_memory(
        self,
    ) -> str:
        """Compactifies the conversation memory using the configured context management strategy.
        Use this tool when the conversation is long and you need to free up context space.
        Helps maintain conversation continuity while staying within token limits.
        """
        raise NotImplementedError
        return "Memory compactified."
