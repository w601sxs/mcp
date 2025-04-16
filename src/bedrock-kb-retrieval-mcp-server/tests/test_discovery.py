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
"""Tests for the discovery module of the bedrock-kb-retrieval-mcp-server."""

import pytest
from unittest.mock import MagicMock, patch
from awslabs.bedrock_kb_retrieval_mcp_server.knowledgebases.discovery import (
    discover_knowledge_bases,
    KNOWLEDGE_BASE_TAG_INCLUSION_KEY,
)


class TestDiscoverKnowledgeBases:
    """Tests for the discover_knowledge_bases function."""

    @pytest.mark.asyncio
    async def test_discover_knowledge_bases(self, mock_bedrock_agent_client):
        """Test discover_knowledge_bases with a mock client."""
        # Call the function
        result = await discover_knowledge_bases(mock_bedrock_agent_client)

        # Check that the result is as expected
        assert len(result) == 1
        assert 'kb-12345' in result
        assert result['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert len(result['kb-12345']['data_sources']) == 2
        assert result['kb-12345']['data_sources'][0]['id'] == 'ds-abc123'
        assert result['kb-12345']['data_sources'][0]['name'] == 'Test Data Source 1'
        assert result['kb-12345']['data_sources'][1]['id'] == 'ds-def456'
        assert result['kb-12345']['data_sources'][1]['name'] == 'Test Data Source 2'

        # Check that the client methods were called correctly
        mock_bedrock_agent_client.get_paginator.assert_called_with('list_knowledge_bases')
        mock_bedrock_agent_client.get_knowledge_base.assert_called_with(knowledgeBaseId='kb-12345')
        mock_bedrock_agent_client.list_tags_for_resource.assert_called()

    @pytest.mark.asyncio
    async def test_discover_knowledge_bases_empty(self):
        """Test discover_knowledge_bases with no matching knowledge bases."""
        # Create a mock client that returns no knowledge bases with the required tag
        mock_client = MagicMock()
        
        # Mock the get_paginator method
        mock_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        
        # Mock the list_knowledge_bases paginator
        kb_page = {
            'knowledgeBaseSummaries': [
                {
                    'knowledgeBaseId': 'kb-12345',
                    'name': 'Test Knowledge Base 1',
                },
                {
                    'knowledgeBaseId': 'kb-67890',
                    'name': 'Test Knowledge Base 2',
                },
            ]
        }
        mock_paginator.paginate.return_value = [kb_page]
        
        # Mock the get_knowledge_base method
        mock_client.get_knowledge_base.side_effect = lambda knowledgeBaseId: {
            'knowledgeBase': {
                'knowledgeBaseArn': f'arn:aws:bedrock:us-west-2:123456789012:knowledge-base/{knowledgeBaseId}'
            }
        }
        
        # Mock the list_tags_for_resource method to return no matching tags
        mock_client.list_tags_for_resource.return_value = {'tags': {}}

        # Call the function
        result = await discover_knowledge_bases(mock_client)

        # Check that the result is empty
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_discover_knowledge_bases_custom_tag(self):
        """Test discover_knowledge_bases with a custom tag key."""
        # Create a mock client
        mock_client = MagicMock()
        
        # Mock the get_paginator method
        mock_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        
        # Mock the list_knowledge_bases paginator
        kb_page = {
            'knowledgeBaseSummaries': [
                {
                    'knowledgeBaseId': 'kb-12345',
                    'name': 'Test Knowledge Base 1',
                },
            ]
        }
        mock_paginator.paginate.return_value = [kb_page]
        
        # Mock the get_knowledge_base method
        mock_client.get_knowledge_base.side_effect = lambda knowledgeBaseId: {
            'knowledgeBase': {
                'knowledgeBaseArn': f'arn:aws:bedrock:us-west-2:123456789012:knowledge-base/{knowledgeBaseId}'
            }
        }
        
        # Mock the list_tags_for_resource method to return a custom tag
        mock_client.list_tags_for_resource.return_value = {'tags': {'custom-tag': 'true'}}
        
        # Mock the list_data_sources paginator
        mock_ds_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_ds_paginator
        
        ds_page = {
            'dataSourceSummaries': [
                {
                    'dataSourceId': 'ds-abc123',
                    'name': 'Test Data Source 1',
                },
            ]
        }
        mock_ds_paginator.paginate.return_value = [ds_page]

        # Call the function with a custom tag key
        result = await discover_knowledge_bases(mock_client, tag_key='custom-tag')

        # Check that the result is as expected
        assert len(result) == 1
        assert 'kb-12345' in result
        assert result['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert len(result['kb-12345']['data_sources']) == 1
        assert result['kb-12345']['data_sources'][0]['id'] == 'ds-abc123'
        assert result['kb-12345']['data_sources'][0]['name'] == 'Test Data Source 1'

    @pytest.mark.asyncio
    async def test_discover_knowledge_bases_pagination(self):
        """Test discover_knowledge_bases with pagination."""
        # Create a mock client
        mock_client = MagicMock()
        
        # Mock the get_paginator method
        mock_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        
        # Mock the list_knowledge_bases paginator with multiple pages
        kb_page1 = {
            'knowledgeBaseSummaries': [
                {
                    'knowledgeBaseId': 'kb-12345',
                    'name': 'Test Knowledge Base 1',
                },
            ]
        }
        kb_page2 = {
            'knowledgeBaseSummaries': [
                {
                    'knowledgeBaseId': 'kb-67890',
                    'name': 'Test Knowledge Base 2',
                },
            ]
        }
        mock_paginator.paginate.return_value = [kb_page1, kb_page2]
        
        # Mock the get_knowledge_base method
        mock_client.get_knowledge_base.side_effect = lambda knowledgeBaseId: {
            'knowledgeBase': {
                'knowledgeBaseArn': f'arn:aws:bedrock:us-west-2:123456789012:knowledge-base/{knowledgeBaseId}'
            }
        }
        
        # Mock the list_tags_for_resource method
        mock_client.list_tags_for_resource.return_value = {'tags': {KNOWLEDGE_BASE_TAG_INCLUSION_KEY: 'true'}}
        
        # Mock the list_data_sources paginator
        mock_ds_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_ds_paginator
        
        ds_page = {
            'dataSourceSummaries': [
                {
                    'dataSourceId': 'ds-abc123',
                    'name': 'Test Data Source 1',
                },
            ]
        }
        mock_ds_paginator.paginate.return_value = [ds_page]

        # Call the function
        result = await discover_knowledge_bases(mock_client)

        # Check that the result includes both knowledge bases
        assert len(result) == 2
        assert 'kb-12345' in result
        assert 'kb-67890' in result
        assert result['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert result['kb-67890']['name'] == 'Test Knowledge Base 2'
