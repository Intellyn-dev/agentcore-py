"""Agentcore: Shared AI agent primitives for the Intellyn platform.

Version 2.0 — Breaking changes from 1.x:
  - register_tool() now takes (fn, metadata: ToolMetadata) instead of (name, description, fn)
  - AgentMemory.max_messages is now enforced with automatic eviction
  - parse_structured() now uses model.model_validate() for Pydantic v2 compatibility
"""

from agentcore.tools import register_tool, get_tool, list_tools, execute_tool, Tool, ToolMetadata
from agentcore.memory import AgentMemory, Message
from agentcore.parser import parse_structured, extract_json_block
from agentcore.retry import with_retry
from agentcore.exceptions import ToolError, ParseError, MemoryOverflowError, RateLimitError

__version__ = "2.0.0"

__all__ = [
    "register_tool",
    "get_tool",
    "list_tools",
    "execute_tool",
    "Tool",
    "ToolMetadata",
    "AgentMemory",
    "Message",
    "parse_structured",
    "extract_json_block",
    "with_retry",
    "ToolError",
    "ParseError",
    "MemoryOverflowError",
    "RateLimitError",
]
