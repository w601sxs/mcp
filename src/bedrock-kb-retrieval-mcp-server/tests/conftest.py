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
"""Test fixtures for the bedrock-kb-retrieval-mcp-server tests."""

import json
import pytest
from typing import Dict, Generator, List
from unittest.mock import MagicMock


@pytest.fixture
def mock_bedrock_agent_client() -> MagicMock:
    """Create a mock Bedrock agent client for testing."""
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
    
    # Mock the list_tags_for_resource method
    mock_client.list_tags_for_resource.side_effect = lambda resourceArn: {
        'tags': {'mcp-multirag-kb': 'true'} if 'kb-12345' in resourceArn else {}
    }
    
    # Mock the list_data_sources paginator
    mock_ds_paginator = MagicMock()
    mock_client.get_paginator.return_value = mock_ds_paginator
    
    ds_page = {
        'dataSourceSummaries': [
            {
                'dataSourceId': 'ds-abc123',
                'name': 'Test Data Source 1',
            },
            {
                'dataSourceId': 'ds-def456',
                'name': 'Test Data Source 2',
            },
        ]
    }
    mock_ds_paginator.paginate.return_value = [ds_page]
    
    return mock_client


@pytest.fixture
def mock_bedrock_agent_runtime_client() -> MagicMock:
    """Create a mock Bedrock agent runtime client for testing."""
    mock_client = MagicMock()
    
    # Mock the meta attribute with region_name
    mock_client.meta = MagicMock()
    mock_client.meta.region_name = 'us-west-2'
    
    # Mock the retrieve method
    mock_client.retrieve.return_value = {
        'retrievalResults': [
            {
                'content': {
                    'text': 'This is a test document content.',
                    'type': 'TEXT',
                },
                'location': 's3://test-bucket/test-document.txt',
                'score': 0.95,
            },
            {
                'content': {
                    'text': 'This is another test document content.',
                    'type': 'TEXT',
                },
                'location': 's3://test-bucket/test-document-2.txt',
                'score': 0.85,
            },
            {
                'content': {
                    'type': 'IMAGE',
                    'image': 'base64-encoded-image-data',
                },
                'location': 's3://test-bucket/test-image.jpg',
                'score': 0.75,
            },
        ]
    }
    
    return mock_client


@pytest.fixture
def sample_knowledge_base_mapping() -> Dict:
    """Return a sample knowledge base mapping for testing."""
    return {
        'kb-12345': {
            'name': 'Test Knowledge Base 1',
            'data_sources': [
                {'id': 'ds-abc123', 'name': 'Test Data Source 1'},
                {'id': 'ds-def456', 'name': 'Test Data Source 2'},
            ]
        }
    }


@pytest.fixture
def sample_query_response() -> str:
    """Return a sample query response for testing."""
    documents = [
        {
            'content': {
                'text': 'This is a test document content.',
                'type': 'TEXT',
            },
            'location': 's3://test-bucket/test-document.txt',
            'score': 0.95,
        },
        {
            'content': {
                'text': 'This is another test document content.',
                'type': 'TEXT',
            },
            'location': 's3://test-bucket/test-document-2.txt',
            'score': 0.85,
        },
    ]
    
    return '\n\n'.join([json.dumps(document) for document in documents])
