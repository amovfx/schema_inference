import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

load_dotenv(".env")

# TODO: Add the model name and temperature to environment variables, have a mode for testing.
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4-0125-preview",
    temperature=0.0,
).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    ),
    model_name=ConfigurableField(
        id="llm_model_name",
        name="LLM Model Name",
        description="The name of the LLM model",
    ),
)
