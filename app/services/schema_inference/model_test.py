import pytest
from app.services.schema_inference.model import (
    llm,
)  # Adjust the import path as necessary


# Use pytest fixtures to set environment variables and mock objects
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")


def test_llm_instantiation():
    # Ensure the ChatOpenAI constructor is called with the expected arguments

    test_instance = llm.with_config(
        configurable={"temperature": 2, "model": "gpt-3.5-turbo"}
    )
    assert test_instance.config["configurable"]["model"] == "gpt-3.5-turbo"
    assert test_instance.config["configurable"]["temperature"] == 2
