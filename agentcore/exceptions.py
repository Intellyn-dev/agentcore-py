class ToolError(Exception):
    """Raised when a registered tool fails during execution."""
    pass


class ParseError(Exception):
    """Raised when structured output parsing fails."""
    pass


class MemoryOverflowError(Exception):
    """Raised when agent memory exceeds configured limits."""
    pass


class RateLimitError(Exception):
    """Raised when an upstream LLM or API rate limit is hit."""
    pass
