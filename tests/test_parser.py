import pytest
from pydantic import BaseModel
from agentcore.parser import parse_structured, extract_json_block
from agentcore.exceptions import ParseError


class SentimentResult(BaseModel):
    sentiment: str
    score: float


def test_parse_valid_json():
    response = '{"sentiment": "positive", "score": 0.95}'
    result = parse_structured(response, SentimentResult)
    assert result.sentiment == "positive"
    assert result.score == 0.95


def test_parse_with_markdown_fence():
    response = '```json\n{"sentiment": "negative", "score": 0.1}\n```'
    result = parse_structured(response, SentimentResult)
    assert result.sentiment == "negative"


def test_parse_invalid_json_raises():
    with pytest.raises(ParseError):
        parse_structured("not json", SentimentResult)
