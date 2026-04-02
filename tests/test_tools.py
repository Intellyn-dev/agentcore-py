import pytest
from agentcore.tools import register_tool, get_tool, list_tools, ToolMetadata
from agentcore.exceptions import ToolError


def test_register_and_retrieve():
    def my_fn(x): return x * 2
    meta = ToolMetadata(name="double", description="Doubles a number")
    register_tool(my_fn, meta)
    tool = get_tool("double")
    assert tool.name == "double"
    assert tool.fn(3) == 6


def test_get_missing_tool_raises():
    with pytest.raises(ToolError):
        get_tool("nonexistent_tool_xyz")


def test_list_tools_contains_registered():
    def noop(): pass
    meta = ToolMetadata(name="noop_test", description="No-op")
    register_tool(noop, meta)
    assert "noop_test" in list_tools()
