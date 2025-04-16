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
"""Tests for the models module of the bedrock-kb-retrieval-mcp-server."""

import pytest
from awslabs.bedrock_kb_retrieval_mcp_server.models import (
    DataSource,
    KnowledgeBase,
    KnowledgeBaseMapping,
)
from typing import Dict, List


class TestDataSource:
    """Tests for the DataSource TypedDict."""

    def test_data_source_creation(self):
        """Test that a DataSource can be created with the required fields."""
        data_source: DataSource = {
            'id': 'ds-abc123',
            'name': 'Test Data Source',
        }
        
        assert data_source['id'] == 'ds-abc123'
        assert data_source['name'] == 'Test Data Source'

    def test_data_source_missing_fields(self):
        """Test that a DataSource requires all fields."""
        with pytest.raises(KeyError):
            # Missing 'name' field
            data_source: DataSource = {'id': 'ds-abc123'}  # type: ignore
            _ = data_source['name']

        with pytest.raises(KeyError):
            # Missing 'id' field
            data_source: DataSource = {'name': 'Test Data Source'}  # type: ignore
            _ = data_source['id']


class TestKnowledgeBase:
    """Tests for the KnowledgeBase TypedDict."""

    def test_knowledge_base_creation(self):
        """Test that a KnowledgeBase can be created with the required fields."""
        knowledge_base: KnowledgeBase = {
            'name': 'Test Knowledge Base',
            'data_sources': [
                {'id': 'ds-abc123', 'name': 'Test Data Source 1'},
                {'id': 'ds-def456', 'name': 'Test Data Source 2'},
            ],
        }
        
        assert knowledge_base['name'] == 'Test Knowledge Base'
        assert len(knowledge_base['data_sources']) == 2
        assert knowledge_base['data_sources'][0]['id'] == 'ds-abc123'
        assert knowledge_base['data_sources'][0]['name'] == 'Test Data Source 1'
        assert knowledge_base['data_sources'][1]['id'] == 'ds-def456'
        assert knowledge_base['data_sources'][1]['name'] == 'Test Data Source 2'

    def test_knowledge_base_missing_fields(self):
        """Test that a KnowledgeBase requires all fields."""
        with pytest.raises(KeyError):
            # Missing 'data_sources' field
            knowledge_base: KnowledgeBase = {'name': 'Test Knowledge Base'}  # type: ignore
            _ = knowledge_base['data_sources']

        with pytest.raises(KeyError):
            # Missing 'name' field
            knowledge_base: KnowledgeBase = {
                'data_sources': [{'id': 'ds-abc123', 'name': 'Test Data Source'}]
            }  # type: ignore
            _ = knowledge_base['name']


class TestKnowledgeBaseMapping:
    """Tests for the KnowledgeBaseMapping TypeAlias."""

    def test_knowledge_base_mapping_creation(self):
        """Test that a KnowledgeBaseMapping can be created."""
        mapping: KnowledgeBaseMapping = {
            'kb-12345': {
                'name': 'Test Knowledge Base 1',
                'data_sources': [
                    {'id': 'ds-abc123', 'name': 'Test Data Source 1'},
                    {'id': 'ds-def456', 'name': 'Test Data Source 2'},
                ],
            },
            'kb-67890': {
                'name': 'Test Knowledge Base 2',
                'data_sources': [
                    {'id': 'ds-ghi789', 'name': 'Test Data Source 3'},
                ],
            },
        }
        
        assert len(mapping) == 2
        assert 'kb-12345' in mapping
        assert 'kb-67890' in mapping
        assert mapping['kb-12345']['name'] == 'Test Knowledge Base 1'
        assert len(mapping['kb-12345']['data_sources']) == 2
        assert mapping['kb-67890']['name'] == 'Test Knowledge Base 2'
        assert len(mapping['kb-67890']['data_sources']) == 1

    def test_knowledge_base_mapping_empty(self):
        """Test that a KnowledgeBaseMapping can be empty."""
        mapping: KnowledgeBaseMapping = {}
        assert len(mapping) == 0
