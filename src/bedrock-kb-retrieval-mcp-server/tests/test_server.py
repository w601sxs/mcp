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
"""Tests for the server module of the bedrock-kb-retrieval-mcp-server."""

import json
import pytest
from unittest.mock import MagicMock, patch
from awslabs.bedrock_kb_retrieval_mcp_server.server import (
    knowledgebases_resource,
    query_knowledge_bases_tool,
)


class TestKnowledgebasesResource:
    """Tests for the knowledgebases_resource function."""

    @pytest.mark.asyncio
    @patch('awslabs.bedrock_kb_retrieval_mcp_server.server.discover_knowledge_bases')
    async def test_knowledgebases_resource(self, mock_discover_knowledge_bases, sample_knowledge_base_mapping):
        """Test the knowledgebases_resource function."""
        # Set up the mock
        mock_discover_knowledge_bases.return_value = sample_knowledge_base_mapping

        # Call the function
        result = await knowledgebases_resource()

        # Check that the result is as expected
        result_dict = json.loads(result)
        assert 'kb-12345' in result_dict
        assert result_dict['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert len(result_dict['kb-12345']['data_sources']) == 2
        assert result_dict['kb-12345']['data_sources'][0]['id'] == 'ds-abc123'
        assert result_dict['kb-12345']['data_sources'][0]['name'] == 'Test Data Source 1'
        assert result_dict['kb-12345']['data_sources'][1]['id'] == 'ds-def456'
        assert result_dict['kb-12345']['data_sources'][1]['name'] == 'Test Data Source 2'

        # Check that discover_knowledge_bases was called with the correct arguments
        mock_discover_knowledge_bases.assert_called_once()


class TestQueryKnowledgeBasesTool:
    """Tests for the query_knowledge_bases_tool function."""

    @pytest.mark.asyncio
    @patch('awslabs.bedrock_kb_retrieval_mcp_server.server.query_knowledge_base')
    async def test_query_knowledge_bases_tool(self, mock_query_knowledge_base, sample_query_response):
        """Test the query_knowledge_bases_tool function with default parameters."""
        # Set up the mock
        mock_query_knowledge_base.return_value = sample_query_response

        # Call the function
        result = await query_knowledge_bases_tool(
            query='test query',
            knowledge_base_id='kb-12345',
        )

        # Check that the result is as expected
        assert result == sample_query_response

        # Check that query_knowledge_base was called with the correct arguments
        mock_query_knowledge_base.assert_called_once()
        call_args = mock_query_knowledge_base.call_args[1]
        assert call_args['query'] == 'test query'
        assert call_args['knowledge_base_id'] == 'kb-12345'
        assert call_args['number_of_results'] == 10
        assert call_args['reranking'] is True
        assert call_args['reranking_model_name'] == 'AMAZON'
        assert call_args['data_source_ids'] is None

    @pytest.mark.asyncio
    @patch('awslabs.bedrock_kb_retrieval_mcp_server.server.query_knowledge_base')
    async def test_query_knowledge_bases_tool_with_custom_parameters(self, mock_query_knowledge_base, sample_query_response):
        """Test the query_knowledge_bases_tool function with custom parameters."""
        # Set up the mock
        mock_query_knowledge_base.return_value = sample_query_response

        # Call the function with custom parameters
        result = await query_knowledge_bases_tool(
            query='test query',
            knowledge_base_id='kb-12345',
            number_of_results=5,
            reranking=False,
            reranking_model_name='COHERE',
            data_source_ids=['ds-abc123', 'ds-def456'],
        )

        # Check that the result is as expected
        assert result == sample_query_response

        # Check that query_knowledge_base was called with the correct arguments
        mock_query_knowledge_base.assert_called_once()
        call_args = mock_query_knowledge_base.call_args[1]
        assert call_args['query'] == 'test query'
        assert call_args['knowledge_base_id'] == 'kb-12345'
        assert call_args['number_of_results'] == 5
        assert call_args['reranking'] is False
        assert call_args['reranking_model_name'] == 'COHERE'
        assert call_args['data_source_ids'] == ['ds-abc123', 'ds-def456']


class TestServerIntegration:
    """Integration tests for the server module."""

    def test_server_function_registration(self):
        """Test that the server functions are registered correctly."""
        # Check that the functions have the correct docstrings
        assert (
            knowledgebases_resource.__doc__ is not None
            and 'List all available Amazon Bedrock Knowledge Bases and their data sources'
            in knowledgebases_resource.__doc__
        )
        assert (
            query_knowledge_bases_tool.__doc__ is not None
            and 'Query an Amazon Bedrock Knowledge Base using natural language'
            in query_knowledge_bases_tool.__doc__
        )

    @pytest.mark.asyncio
    @patch('awslabs.bedrock_kb_retrieval_mcp_server.server.discover_knowledge_bases')
    @patch('awslabs.bedrock_kb_retrieval_mcp_server.server.query_knowledge_base')
    async def test_server_workflow(
        self, mock_query_knowledge_base, mock_discover_knowledge_bases, sample_knowledge_base_mapping, sample_query_response
    ):
        """Test the complete server workflow."""
        # Set up the mocks
        mock_discover_knowledge_bases.return_value = sample_knowledge_base_mapping
        mock_query_knowledge_base.return_value = sample_query_response

        # Step 1: Get the knowledge bases
        kb_result = await knowledgebases_resource()
        kb_dict = json.loads(kb_result)

        # Step 2: Query a knowledge base
        query_result = await query_knowledge_bases_tool(
            query='test query',
            knowledge_base_id=list(kb_dict.keys())[0],
        )

        # Check that the results are as expected
        assert 'kb-12345' in kb_dict
        assert kb_dict['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert query_result == sample_query_response

        # Check that the functions were called with the correct arguments
        mock_discover_knowledge_bases.assert_called_once()
        mock_query_knowledge_base.assert_called_once()
        call_args = mock_query_knowledge_base.call_args[1]
        assert call_args['query'] == 'test query'
        assert call_args['knowledge_base_id'] == 'kb-12345'
