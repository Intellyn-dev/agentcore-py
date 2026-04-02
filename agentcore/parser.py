from __future__ import annotations

import json
import re
from typing import TypeVar

from pydantic import BaseModel

from agentcore.exceptions import ParseError

T = TypeVar("T", bound=BaseModel)


def parse_structured(response: str, model: type[T]) -> T:
    """Parse an LLM text response into a Pydantic model.

    Extracts JSON from the response (handles markdown code fences),
    then validates against the provided model class.
    """
    text = response.strip()

    json_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if json_match:
        text = json_match.group(1)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"Response is not valid JSON: {exc}") from exc

    try:
        return model(**data)
    except Exception as exc:
        raise ParseError(f"Failed to parse response into {model.__name__}: {exc}") from exc


def extract_json_block(text: str) -> dict:
    """Extract the first JSON object or array from free-form text."""
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ParseError("No JSON object found in response")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ParseError(f"Extracted JSON is malformed: {exc}") from exc
