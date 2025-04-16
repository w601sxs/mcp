# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
# and limitations under the License.
"""Tests for the runtime module of the bedrock-kb-retrieval-mcp-server."""

import json
import pytest
from unittest.mock import MagicMock, patch
from awslabs.bedrock_kb_retrieval_mcp_server.knowledgebases.runtime import query_knowledge_base


class TestQueryKnowledgeBase:
    """Tests for the query_knowledge_base function."""

    @pytest.mark.asyncio
    async def test_query_knowledge_base(self, mock_bedrock_agent_runtime_client, sample_query_response):
        """Test query_knowledge_base with default parameters."""
        # Call the function
        result = await query_knowledge_base(
            query='test query',
            knowledge_base_id='kb-12345',
            kb_agent_client=mock_bedrock_agent_runtime_client,
        )

        # Check that the result is as expected
        # Parse the result string into a list of JSON objects
        result_docs = [json.loads(doc) for doc in result.split('\n\n')]
        
        assert len(result_docs) == 2
        assert result_docs[0]['content']['text'] == 'This is a test document content.'
        assert result_docs[0]['location'] == 's3://test-bucket/test-document.txt'
        assert result_docs[0]['score'] == 0.95
        assert result_docs[1]['content']['text'] == 'This is another test document content.'
        assert result_docs[1]['location'] == 's3://test-bucket/test-document-2.txt'
        assert result_docs[1]['score'] == 0.85

        # Check that the client methods were called correctly
        mock_bedrock_agent_runtime_client.retrieve.assert_called_once()
        call_args = mock_bedrock_agent_runtime_client.retrieve.call_args[1]
        assert call_args['knowledgeBaseId'] == 'kb-12345'
        assert call_args['retrievalQuery']['text'] == 'test query'
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['numberOfResults'] == 20
        assert 'rerankingConfiguration' in call_args['retrievalConfiguration']['vectorSearchConfiguration']

    @pytest.mark.asyncio
    async def test_query_knowledge_base_with_custom_parameters(self, mock_bedrock_agent_runtime_client):
        """Test query_knowledge_base with custom parameters."""
        # Call the function with custom parameters
        result = await query_knowledge_base(
            query='test query',
            knowledge_base_id='kb-12345',
            kb_agent_client=mock_bedrock_agent_runtime_client,
            number_of_results=5,
            reranking=True,
            reranking_model_name='COHERE',
            data_source_ids=['ds-abc123', 'ds-def456'],
        )

        # Check that the client methods were called correctly
        mock_bedrock_agent_runtime_client.retrieve.assert_called_once()
        call_args = mock_bedrock_agent_runtime_client.retrieve.call_args[1]
        assert call_args['knowledgeBaseId'] == 'kb-12345'
        assert call_args['retrievalQuery']['text'] == 'test query'
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['numberOfResults'] == 5
        assert 'rerankingConfiguration' in call_args['retrievalConfiguration']['vectorSearchConfiguration']
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['rerankingConfiguration']['bedrockRerankingConfiguration']['modelConfiguration']['modelArn'].endswith('cohere.rerank-v3-5:0')
        assert 'filter' in call_args['retrievalConfiguration']['vectorSearchConfiguration']
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['filter']['in']['key'] == 'x-amz-bedrock-kb-data-source-id'
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['filter']['in']['value'] == ['ds-abc123', 'ds-def456']

    @pytest.mark.asyncio
    async def test_query_knowledge_base_without_reranking(self, mock_bedrock_agent_runtime_client):
        """Test query_knowledge_base without reranking."""
        # Call the function with reranking disabled
        result = await query_knowledge_base(
            query='test query',
            knowledge_base_id='kb-12345',
            kb_agent_client=mock_bedrock_agent_runtime_client,
            reranking=False,
        )

        # Check that the client methods were called correctly
        mock_bedrock_agent_runtime_client.retrieve.assert_called_once()
        call_args = mock_bedrock_agent_runtime_client.retrieve.call_args[1]
        assert call_args['knowledgeBaseId'] == 'kb-12345'
        assert call_args['retrievalQuery']['text'] == 'test query'
        assert call_args['retrievalConfiguration']['vectorSearchConfiguration']['numberOfResults'] == 20
        assert 'rerankingConfiguration' not in call_args['retrievalConfiguration']['vectorSearchConfiguration']

    @pytest.mark.asyncio
    async def test_query_knowledge_base_with_unsupported_region(self):
        """Test query_knowledge_base with an unsupported region for reranking."""
        # Create a mock client with an unsupported region
        mock_client = MagicMock()
        mock_client.meta = MagicMock()
        mock_client.meta.region_name = 'eu-west-1'  # Unsupported region for reranking

        # Call the function with reranking enabled
        with pytest.raises(ValueError) as excinfo:
            await query_knowledge_base(
                query='test query',
                knowledge_base_id='kb-12345',
                kb_agent_client=mock_client,
                reranking=True,
            )

        # Check that the correct error message is raised
        assert 'Reranking is not supported in region eu-west-1' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_query_knowledge_base_with_image_content(self, mock_bedrock_agent_runtime_client):
        """Test query_knowledge_base with image content in the response."""
        # Call the function
        result = await query_knowledge_base(
            query='test query',
            knowledge_base_id='kb-12345',
            kb_agent_client=mock_bedrock_agent_runtime_client,
        )

        # Parse the result string into a list of JSON objects
        result_docs = [json.loads(doc) for doc in result.split('\n\n')]
        
        # Check that only text documents are included in the result (image is skipped)
        assert len(result_docs) == 2
        for doc in result_docs:
            assert doc['content']['type'] == 'TEXT'
