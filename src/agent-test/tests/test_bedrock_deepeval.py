"""Tests for bedrock_deepeval module.

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import pytest
import unittest.mock
from awslabs.agent_test.bedrock_deepeval import BedrockDeepEvalEmbeddingModel, BedrockDeepEvalLLM
from pydantic import BaseModel


class SampleModel(BaseModel):
    """Sample model for structured output testing."""

    message: str
    score: float


class TestBedrockDeepEvalEmbeddingModel:
    """Test BedrockDeepEvalEmbeddingModel class."""

    def test_initialization_default_params(self):
        """Test initialization with default parameters."""
        model = BedrockDeepEvalEmbeddingModel()
        assert model.model_id == 'amazon.titan-embed-text-v2:0'
        assert model.region_name == 'us-west-2'

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        model = BedrockDeepEvalEmbeddingModel(model_id='custom-model-id', region_name='us-east-1')
        assert model.model_id == 'custom-model-id'
        assert model.region_name == 'us-east-1'

    def test_get_model_name(self):
        """Test get_model_name method."""
        model = BedrockDeepEvalEmbeddingModel(model_id='test-model')
        assert model.get_model_name() == 'test-model'

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.BedrockEmbeddings')
    def test_load_model(self, mock_bedrock_embeddings):
        """Test load_model method."""
        model = BedrockDeepEvalEmbeddingModel(model_id='test-model-id', region_name='us-east-1')

        result = model.load_model()

        mock_bedrock_embeddings.assert_called_once_with(
            model_id='test-model-id',
            region_name='us-east-1',
            normalize=True,
        )
        assert result == mock_bedrock_embeddings.return_value

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.BedrockEmbeddings')
    def test_embed_text(self, mock_bedrock_embeddings):
        """Test embed_text method."""
        mock_embedding_model = mock_bedrock_embeddings.return_value
        mock_embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]

        model = BedrockDeepEvalEmbeddingModel()
        result = model.embed_text('test text')

        assert result == [0.1, 0.2, 0.3]
        mock_embedding_model.embed_query.assert_called_once_with('test text')

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.BedrockEmbeddings')
    def test_embed_texts(self, mock_bedrock_embeddings):
        """Test embed_texts method."""
        mock_embedding_model = mock_bedrock_embeddings.return_value
        mock_embedding_model.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]

        model = BedrockDeepEvalEmbeddingModel()
        result = model.embed_texts(['text1', 'text2'])

        assert result == [[0.1, 0.2], [0.3, 0.4]]
        mock_embedding_model.embed_documents.assert_called_once_with(['text1', 'text2'])

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.BedrockEmbeddings')
    @pytest.mark.asyncio
    async def test_a_embed_text(self, mock_bedrock_embeddings):
        """Test a_embed_text async method."""
        mock_embedding_model = mock_bedrock_embeddings.return_value
        # Return a coroutine for async call
        import asyncio

        async_return = asyncio.Future()
        async_return.set_result([0.1, 0.2, 0.3])
        mock_embedding_model.aembed_query.return_value = async_return

        model = BedrockDeepEvalEmbeddingModel()
        result = await model.a_embed_text('test text')

        assert result == [0.1, 0.2, 0.3]
        mock_embedding_model.aembed_query.assert_called_once_with('test text')

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.BedrockEmbeddings')
    @pytest.mark.asyncio
    async def test_a_embed_texts(self, mock_bedrock_embeddings):
        """Test a_embed_texts async method."""
        mock_embedding_model = mock_bedrock_embeddings.return_value
        # Return a coroutine for async call
        import asyncio

        async_return = asyncio.Future()
        async_return.set_result([[0.1, 0.2], [0.3, 0.4]])
        mock_embedding_model.aembed_documents.return_value = async_return

        model = BedrockDeepEvalEmbeddingModel()
        result = await model.a_embed_texts(['text1', 'text2'])

        assert result == [[0.1, 0.2], [0.3, 0.4]]
        mock_embedding_model.aembed_documents.assert_called_once_with(['text1', 'text2'])


class TestBedrockDeepEvalLLM:
    """Test BedrockDeepEvalLLM class."""

    def test_initialization_required_params(self):
        """Test initialization with required parameters."""
        model = BedrockDeepEvalLLM(model_id='test-model', region_name='us-west-2')
        assert model.model_id == 'test-model'
        assert model.region_name == 'us-west-2'
        assert model.temperature == 0.0
        assert model.max_tokens == 1000
        assert model.top_p == 0.9999

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        model = BedrockDeepEvalLLM(
            model_id='custom-model',
            region_name='us-east-1',
            temperature=0.5,
            max_tokens=2000,
            top_p=0.8,
        )
        assert model.model_id == 'custom-model'
        assert model.region_name == 'us-east-1'
        assert model.temperature == 0.5
        assert model.max_tokens == 2000
        assert model.top_p == 0.8

    def test_get_model_name(self):
        """Test get_model_name method."""
        model = BedrockDeepEvalLLM(model_id='test-model-name', region_name='us-west-2')
        assert model.get_model_name() == 'test-model-name'

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.ChatBedrockConverse')
    def test_load_model(self, mock_chat_bedrock):
        """Test load_model method."""
        model = BedrockDeepEvalLLM(
            model_id='test-model',
            region_name='us-east-1',
            temperature=0.3,
            max_tokens=1500,
            top_p=0.95,
        )

        result = model.load_model()

        # Verify that the model was created with correct parameters during initialization
        mock_chat_bedrock.assert_called_with(
            model='test-model',
            region_name='us-east-1',
            temperature=0.3,
            max_tokens=1500,
            top_p=0.95,
        )
        assert result == model.model

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.ChatBedrockConverse')
    def test_generate(self, mock_chat_bedrock):
        """Test generate method."""
        # Setup mock
        mock_model_instance = mock_chat_bedrock.return_value
        mock_response = unittest.mock.Mock()
        mock_response.content = 'test response content'
        mock_model_instance.invoke.return_value = mock_response

        model = BedrockDeepEvalLLM(model_id='test-model', region_name='us-west-2')

        result = model.generate('test prompt')

        # Verify calls
        mock_model_instance.invoke.assert_called_once_with(
            [{'role': 'user', 'content': 'test prompt'}]
        )

        # Verify result
        assert result == 'test response content'

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.ChatBedrockConverse')
    def test_generate_exception(self, mock_chat_bedrock):
        """Test generate method with exception."""
        # Setup mock to raise exception
        mock_model_instance = mock_chat_bedrock.return_value
        test_exception = Exception('Test error')
        mock_model_instance.invoke.side_effect = test_exception

        model = BedrockDeepEvalLLM(model_id='test-model', region_name='us-west-2')

        with pytest.raises(Exception) as exc_info:
            model.generate('test prompt')

        assert exc_info.value == test_exception

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.ChatBedrockConverse')
    @pytest.mark.asyncio
    async def test_a_generate(self, mock_chat_bedrock):
        """Test a_generate async method."""
        # Setup mock
        mock_model_instance = mock_chat_bedrock.return_value
        # Return a coroutine for async call
        import asyncio

        async_return = asyncio.Future()
        mock_response = unittest.mock.Mock()
        mock_response.content = 'async test response content'
        async_return.set_result(mock_response)
        mock_model_instance.ainvoke.return_value = async_return

        model = BedrockDeepEvalLLM(model_id='test-model', region_name='us-west-2')

        result = await model.a_generate('async test prompt')

        # Verify calls
        mock_model_instance.ainvoke.assert_called_once_with(
            [{'role': 'user', 'content': 'async test prompt'}]
        )

        # Verify result
        assert result == 'async test response content'

    @unittest.mock.patch('awslabs.agent_test.bedrock_deepeval.ChatBedrockConverse')
    @pytest.mark.asyncio
    async def test_a_generate_exception(self, mock_chat_bedrock):
        """Test a_generate async method with exception."""
        # Setup mock to raise exception
        mock_model_instance = mock_chat_bedrock.return_value
        test_exception = Exception('Async test error')
        mock_model_instance.ainvoke.side_effect = test_exception

        model = BedrockDeepEvalLLM(model_id='test-model', region_name='us-west-2')

        with pytest.raises(Exception) as exc_info:
            await model.a_generate('async test prompt')

        assert exc_info.value == test_exception
