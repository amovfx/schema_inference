import json

from langchain.prompts import PromptTemplate
from app.services.schema_inference.outputparser import SchemaInferenceParser, type_map

type_map_str = (
    json.dumps({k: k for k in type_map.keys()})
    .replace('": "', '": ')
    .replace('", ', ", ")
    .replace('"}', "}")
)

schema_inference_template = """From the give text:
{data}

Determine the data that would be most useful to extract from the page.
return a pydantic model of the data it should be in the format to feed into this code.

follow this type map, this is what the coverter uses:

type_map = {type_map_str}


{instructions}

Format Instructions:
{format_instructions}

Give no natural language explanation, just the json format instructions. That can be easily parsed by machine.


"""
schema_inference_prompt = PromptTemplate(
    input_variables=["data", "instructions"],
    template=schema_inference_template,
    partial_variables={
        "format_instructions": SchemaInferenceParser().get_format_instructions(),
        "type_map_str": type_map_str,
    },
)


schema_extraction_template = """
Scrape the relevant infromation from the page.
{data}

Give no natural language explanation, just the json format instructions. That can be easily parsed by machine.
If a value for the field is not present, return None.

Format Instructions:
{format_instructions}
"""

schema_extraction_prompt = PromptTemplate(
    input_variables=["data", "format_instructions"],
    template=schema_extraction_template,
)

schema_inference_reducer_template = """


This is a list of schemas that may or may not be different from each other.
{data}

Reduce them into a single schema that can represent all of them.

Format Instructions:
{format_instructions}

Give no natural language explanation, just the json format instructions. That can be easily parsed by machine.


"""
schema_inference_reducer_prompt = PromptTemplate(
    input_variables=["data"],
    template=schema_inference_reducer_template,
    partial_variables={
        "format_instructions": SchemaInferenceParser().get_format_instructions()
    },
)
