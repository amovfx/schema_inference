import pytest

from app.services.schema_inference.outputparser import (
    SchemaInferenceParser,
    FieldModel,
    SchemaInferenceModel,
)


def test_field_model():
    field = FieldModel(name="test", type="str", description="test description")
    assert field.name == "test"
    assert field.type == "str"
    assert field.description == "test description"


def test_schema_inference_model():
    field = FieldModel(name="test", type="str", description="test description")
    schema = SchemaInferenceModel(name="test", fields=[field])
    assert schema.name == "test"
    assert schema.fields == [field]


def test_schema_inference_parser():
    field1 = FieldModel(name="name", type="str", description="Name of a person")
    field2 = FieldModel(name="age", type="int", description="Age of a person")
    schema = SchemaInferenceModel(name="test", fields=[field1, field2])

    parser = SchemaInferenceParser.create_infered_json_parser(schema.dict())
    formated_instructions = parser.get_format_instructions()
    assert "name" in formated_instructions
    assert "str" in formated_instructions
    assert "Name of a person" in formated_instructions

    assert "age" in formated_instructions
    assert "int" in formated_instructions
    assert "Age of a person" in formated_instructions
