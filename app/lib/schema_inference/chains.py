import asyncio
import random
from typing import List, Optional


from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser

from app.services.schema_inference.model import llm
from app.services.schema_inference.outputparser import SchemaInferenceParser
from app.services.schema_inference.prompt import (
    schema_extraction_prompt,
    schema_inference_prompt,
    schema_inference_reducer_prompt,
)

llm_chain = llm | SchemaInferenceParser()
schema_inference_chain = schema_inference_prompt | llm_chain
reducer_chain = schema_inference_reducer_prompt | llm_chain
extract_chain = schema_extraction_prompt | llm


async def create_schema_inference_parser(
    data: List[Document], instructions: Optional[str] = "", sample_size: int = 5
) -> JsonOutputParser:
    """Takes a list of documents and learns a schema from them. Returns a JsonOutputParser."""

    sample_size = min(sample_size, len(data))
    sample_urls = random.sample(data, sample_size)

    prompts = [
        {"data": sample.page_content, "instructions": instructions}
        for sample in sample_urls
    ]
    # Todo: add heriarchal reducer
    results = await schema_inference_chain.abatch(prompts)
    meta_model_dict = reducer_chain.invoke({"data": results})
    return meta_model_dict


# remove url loading to general text data
async def extract_schema(data: List[Document], dynamic_parser: JsonOutputParser):
    """Takes a list of text and a meta model. Returns a list of parsed data."""

    async def make_prompt_input(s):
        return {
            "data": s,
            "format_instructions": dynamic_parser.get_format_instructions(),
        }

    prompts = await asyncio.gather(*[make_prompt_input(s.page_content) for s in data])
    chain = extract_chain | (lambda x: dynamic_parser.parse(x.content))
    scrape_chain_results = await chain.abatch(prompts)

    return scrape_chain_results
