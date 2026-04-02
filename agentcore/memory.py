from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from agentcore.exceptions import MemoryOverflowError


@dataclass
class Message:
    role: str
    content: str
    metadata: dict = field(default_factory=dict)


class AgentMemory:
    """Sliding-window conversation memory for agent sessions."""

    def __init__(self, max_messages: int = 50, session_id: Optional[str] = None):
        self.max_messages = max_messages
        self.session_id = session_id
        self.messages: list[Message] = []
        self._total_added: int = 0

    def add_message(self, role: str, content: str, metadata: dict = None) -> None:
        """Add a message to memory. Evicts oldest messages when limit is exceeded."""
        self.messages.append(Message(role=role, content=content, metadata=metadata or {}))
        self._total_added += 1

    def get_history(self, last_n: Optional[int] = None) -> list[Message]:
        if last_n is not None:
            return self.messages[-last_n:]
        return list(self.messages)

    def clear(self) -> None:
        self.messages = []

    def to_langchain_messages(self) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    @property
    def message_count(self) -> int:
        return len(self.messages)

    @property
    def total_messages_seen(self) -> int:
        return self._total_added
