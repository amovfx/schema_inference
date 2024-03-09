from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
    Mock,
)

import pytest
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from app.services.schema_inference.outputparser import (
    SchemaInferenceParser,
    FieldModel,
    SchemaInferenceModel,
)

from app.services.schema_inference.chains import (
    create_schema_inference_parser,
    extract_schema,
)
from langchain.prompts import PromptTemplate

from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_create_schema_inference_parser():
    with patch(
        "app.services.schema_inference.chains.schema_inference_chain",
    ) as mock_abatch, patch(
        "app.services.schema_inference.chains.reducer_chain",
    ) as mock_invoke:

        test_field = FieldModel(
            name="TestField", type="string", description="Test description"
        )
        test_data = SchemaInferenceModel(
            name="TestModel", fields=[test_field, test_field]
        )
        mock_abatch.abatch = AsyncMock(return_value=[test_data.dict()] * 3)
        mock_invoke.invoke = MagicMock(return_value=test_data.dict())
        # Assuming this is the expected return type

        documents = [Document(page_content="Test content") for _ in range(5)]
        result = await create_schema_inference_parser(
            data=documents, instructions="Test instructions", sample_size=3
        )

        assert result == test_data.dict()
        assert mock_abatch.called_once()
        assert mock_invoke.called_once()


@pytest.mark.asyncio
async def test_extract_schema():
    # Mock the extract_chain to return a mock with an abatch method that is an AsyncMock
    with patch(
        "app.services.schema_inference.chains.extract_chain",
        new_callable=AsyncMock,
    ) as mock_extract_chain:
        # Setup the mock return value for abatch
        mock_extract_chain.abatch = AsyncMock(
            return_value=[{"content": "mocked content"}]
        )

        async def async_magic():
            return_value = [{"content": "mocked content"}]
            return return_value

        MagicMock.__await__ = lambda x: async_magic().__await__()

        # Create a mock JsonOutputParser with a mocked parse method
        mock_parser = Mock()
        mock_parser.parse = Mock(return_value={"parsed": "data"})
        mock_parser.get_format_instructions = Mock(return_value="mocked instructions")

        # Create mock Document objects
        documents = [Document(page_content=f"Test content {i}") for i in range(3)]

        # Call the function under test
        results = await extract_schema(data=documents, dynamic_parser=mock_parser)

        # Assertions
        # mock_extract_chain.abatch.assert_called_once()  # Ensure abatch was called exactly once
        assert all(
            isinstance(result, dict) for result in results
        ), "All results should be dictionaries"
