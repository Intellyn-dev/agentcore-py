import json
from typing import Optional

import pytest
from pydantic import BaseModel

from agentcore.parser import parse_structured


class ModelWithOptionalField(BaseModel):
    name: str
    score: int
    summary: Optional[str] = None


class ModelWithAllOptional(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    count: Optional[int] = None


def test_parse_structured_optional_field_missing_does_not_raise():
    """Verify that parse_structured does not raise a KeyError when an optional
    field defined in the model schema is absent from the LLM response JSON.
    The fix replaces manual field iteration with model(**data), allowing Pydantic
    to handle missing optional fields using their default values."""
    response = json.dumps({"name": "AgentCore", "score": 42})
    result = parse_structured(response, ModelWithOptionalField)
    assert result.name == "AgentCore"
    assert result.score == 42
    assert result.summary is None


def test_parse_structured_optional_field_present_is_used():
    """Verify that when an optional field is present in the response, its value
    is correctly populated in the returned model instance."""
    response = json.dumps({"name": "AgentCore", "score": 42, "summary": "A great agent"})
    result = parse_structured(response, ModelWithOptionalField)
    assert result.name == "AgentCore"
    assert result.score == 42
    assert result.summary == "A great agent"


def test_parse_structured_all_optional_fields_missing():
    """Verify that a model where all fields are optional can be parsed from an
    empty JSON object without raising any exception."""
    response = json.dumps({})
    result = parse_structured(response, ModelWithAllOptional)
    assert result.title is None
    assert result.description is None
    assert result.count is None


def test_parse_structured_all_optional_fields_partially_provided():
    """Verify that a subset of optional fields can be provided and the rest
    default to None without raising a KeyError."""
    response = json.dumps({"title": "Hello"})
    result = parse_structured(response, ModelWithAllOptional)
    assert result.title == "Hello"
    assert result.description is None
    assert result.count is None


def test_parse_structured_optional_field_missing_in_markdown_fenced_response():
    """Verify that the fix works correctly when the JSON is wrapped in a
    markdown code fence and an optional field is absent from the payload."""
    response = "```json\n{\"name\": \"Fenced\", \"score\": 7}\n```"
    result = parse_structured(response, ModelWithOptionalField)
    assert result.name == "Fenced"
    assert result.score == 7
    assert result.summary is None