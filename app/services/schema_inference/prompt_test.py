import pytest
from app.services.schema_inference.prompt import (
    schema_inference_prompt,
    schema_extraction_prompt,
    schema_inference_reducer_prompt,
    type_map_str,
)
from app.services.schema_inference.outputparser import SchemaInferenceParser


def test_schema_inference_prompt():
    # Ensure the ChatOpenAI constructor is called with the expected arguments
    # Adjust the import path as necessary

    val = schema_inference_prompt.format_prompt(
        data=["test1", "test2"], instructions="Test Instructions"
    )
    assert "test1" in val.text
    assert "test2" in val.text
    assert "Test Instructions" in val.text
    assert type_map_str in val.text


def test_schema_extraction_prompt():
    # Ensure the ChatOpenAI constructor is called with the expected arguments
    # Adjust the import path as necessary

    val = schema_extraction_prompt.format_prompt(
        data=["test1", "test2"], format_instructions="Test Instructions"
    )
    assert "test1" in val.text
    assert "test2" in val.text
    assert "Test Instructions" in val.text


def test_schema_inference_reducer_prompt():
    # Ensure the ChatOpenAI constructor is called with the expected arguments
    # Adjust the import path as necessary

    val = schema_inference_reducer_prompt.format_prompt(data=["test1", "test2"])
    assert "test1" in val.text
    assert "test2" in val.text
    assert SchemaInferenceParser().get_format_instructions() in val.text
