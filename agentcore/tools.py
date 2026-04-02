from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Callable, Any

from agentcore.exceptions import ToolError


@dataclass
class ToolMetadata:
    name: str
    description: str
    version: str = "1.0"
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class Tool:
    metadata: ToolMetadata
    fn: Callable

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def description(self) -> str:
        return self.metadata.description


_registry: dict[str, Tool] = {}


def register_tool(fn: Callable, metadata: ToolMetadata) -> None:
    """Register a callable as an agent tool.

    Args:
        fn: The callable to register as a tool.
        metadata: Tool metadata including name, description, and optional tags.
    """
    if not callable(fn):
        raise TypeError(f"Expected callable, got {type(fn)}")
    _registry[metadata.name] = Tool(metadata=metadata, fn=fn)


def get_tool(name: str) -> Tool:
    if name not in _registry:
        raise ToolError(f"Tool '{name}' not registered")
    return _registry[name]


def list_tools() -> list[str]:
    return list(_registry.keys())


async def execute_tool(name: str, **kwargs: Any) -> Any:
    tool = get_tool(name)
    try:
        if inspect.iscoroutinefunction(tool.fn):
            return await tool.fn(**kwargs)
        return tool.fn(**kwargs)
    except Exception as exc:
        raise ToolError(f"Tool '{name}' failed: {exc}") from exc
