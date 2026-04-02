# agentcore-py

Shared AI agent primitives for the Intellyn platform.

## Installation

```bash
pip install git+https://github.com/Intellyn-dev/agentcore-py.git
```

## Version 2.0 Breaking Changes

- `register_tool()` signature changed from `(name, description, fn)` to `(fn, metadata: ToolMetadata)`
- Use `ToolMetadata(name=..., description=...)` when registering tools

## Usage

```python
from agentcore import register_tool, ToolMetadata, AgentMemory, parse_structured

# Register a tool
def search_products(query: str) -> list:
    ...

register_tool(search_products, ToolMetadata(name="search_products", description="Search product catalog"))

# Use memory
memory = AgentMemory(max_messages=50)
memory.add_message("user", "Find me red shoes")
```
