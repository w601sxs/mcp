# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the response type classes in server.py."""

import pytest
from typing import get_type_hints
from unittest.mock import MagicMock, patch


# ----------------------
# Mock external modules
# ----------------------
mock_modules = {
    'awslabs.amazon_keyspaces_mcp_server': MagicMock(),
    'awslabs.amazon_keyspaces_mcp_server.server': MagicMock(),
    'awslabs.amazon_mq_mcp_server': MagicMock(),
    'awslabs.amazon_mq_mcp_server.server': MagicMock(),
    'awslabs.amazon_neptune_mcp_server.server': MagicMock(),
    'awslabs.amazon_qbusiness_anonymous_mcp_server.server': MagicMock(),
    'awslabs.amazon_rekognition_mcp_server.server': MagicMock(),
    'awslabs.amazon_sns_sqs_mcp_server.server': MagicMock(),
    'awslabs.aurora_dsql_mcp_server.server': MagicMock(),
    'awslabs.aws_api_mcp_server.server': MagicMock(),
    'awslabs.aws_bedrock_data_automation_mcp_server.server': MagicMock(),
    'awslabs.aws_dataprocessing_mcp_server.server': MagicMock(),
    'awslabs.aws_diagram_mcp_server.server': MagicMock(),
    'awslabs.aws_documentation_mcp_server.server_aws': MagicMock(),
    'awslabs.aws_healthomics_mcp_server.server': MagicMock(),
    'awslabs.aws_location_server.server': MagicMock(),
    'awslabs.aws_pricing_mcp_server.server': MagicMock(),
    'awslabs.aws_serverless_mcp_server.server': MagicMock(),
    'awslabs.aws_support_mcp_server.server': MagicMock(),
    'awslabs.bedrock_kb_retrieval_mcp_server.server': MagicMock(),
    'awslabs.cdk_mcp_server.core.server': MagicMock(),
    'awslabs.cfn_mcp_server.server': MagicMock(),
    'awslabs.cloudwatch_appsignals_mcp_server.server': MagicMock(),
    'awslabs.cloudwatch_mcp_server.server': MagicMock(),
    'awslabs.code_doc_gen_mcp_server.server': MagicMock(),
    'awslabs.cost_explorer_mcp_server.server': MagicMock(),
    'awslabs.documentdb_mcp_server.server': MagicMock(),
    'awslabs.dynamodb_mcp_server.server': MagicMock(),
    'awslabs.ecs_mcp_server.main': MagicMock(),
    'awslabs.eks_mcp_server.server': MagicMock(),
    'awslabs.elasticache_mcp_server.main': MagicMock(),
    'awslabs.finch_mcp_server.server': MagicMock(),
    'awslabs.frontend_mcp_server.server': MagicMock(),
    'awslabs.git_repo_research_mcp_server.server': MagicMock(),
    'awslabs.iam_mcp_server.server': MagicMock(),
    'awslabs.lambda_tool_mcp_server.server': MagicMock(),
    'awslabs.memcached_mcp_server.main': MagicMock(),
    'awslabs.mysql_mcp_server.server': MagicMock(),
    'awslabs.nova_canvas_mcp_server.server': MagicMock(),
    'awslabs.postgres_mcp_server.server': MagicMock(),
    'awslabs.prometheus_mcp_server.server': MagicMock(),
    'awslabs.redshift_mcp_server.server': MagicMock(),
    'awslabs.s3_tables_mcp_server.server': MagicMock(),
    'awslabs.stepfunctions_tool_mcp_server.server': MagicMock(),
    'awslabs.syntheticdata_mcp_server.server': MagicMock(),
    'awslabs.timestream_for_influxdb_mcp_server.server': MagicMock(),
}

# Mock out fastmcp to avoid ValidationError in ExperimentalSettings
mock_fastmcp = MagicMock()
mock_fastmcp.FastMCP = MagicMock()
mock_fastmcp.Settings = MagicMock()

mock_fastmcp_server = MagicMock()
mock_fastmcp_server.proxy = MagicMock()
mock_fastmcp_server.proxy.ProxyClient = MagicMock()

mock_modules.update(
    {
        'fastmcp': mock_fastmcp,
        'fastmcp.settings': MagicMock(),
        'fastmcp.server': mock_fastmcp_server,
        'fastmcp.server.proxy': MagicMock(),
    }
)
with patch.dict('sys.modules', mock_modules):
    from awslabs.core_mcp_server.server import ContentItem, McpResponse


class TestContentItem:
    """Tests for the ContentItem TypedDict."""

    def test_content_item_structure(self):
        """Test that ContentItem has the expected structure."""
        # Get the type hints for ContentItem
        type_hints = get_type_hints(ContentItem)

        # Check that the expected fields are present
        assert 'type' in type_hints
        assert 'text' in type_hints

        # Check that the field types are correct
        assert type_hints['type'] is str
        assert type_hints['text'] is str

    def test_content_item_creation(self):
        """Test creating a ContentItem."""
        # Create a ContentItem
        content_item: ContentItem = {'type': 'text', 'text': 'Test content'}

        # Check that the fields are set correctly
        assert content_item['type'] == 'text'
        assert content_item['text'] == 'Test content'

    def test_content_item_missing_field(self):
        """Test that a ContentItem requires all fields."""
        # This is a runtime check since TypedDict is a runtime construct
        with pytest.raises(KeyError):
            # Missing 'text' field
            content_item: ContentItem = {'type': 'text'}  # type: ignore
            # Access the missing field to trigger the error
            content_item['text']


class TestMcpResponse:
    """Tests for the McpResponse TypedDict."""

    def test_mcp_response_structure(self):
        """Test that McpResponse has the expected structure."""
        # Get the type hints for McpResponse
        type_hints = get_type_hints(McpResponse)

        # Check that the expected fields are present
        assert 'content' in type_hints
        assert 'isError' in type_hints

        # Check that the field types are correct
        # The type might be list[ContentItem] or typing.List[ContentItem] depending on Python version
        assert str(type_hints['content']).endswith(
            'List[awslabs.core_mcp_server.server.ContentItem]'
        )
        assert type_hints['isError'] is bool

    def test_mcp_response_creation(self):
        """Test creating an McpResponse."""
        # Create an McpResponse
        response: McpResponse = {
            'content': [{'type': 'text', 'text': 'Test content'}],
            'isError': False,
        }

        # Check that the fields are set correctly
        assert len(response['content']) == 1
        assert response['content'][0]['type'] == 'text'
        assert response['content'][0]['text'] == 'Test content'
        assert response['isError'] is False

    def test_mcp_response_without_is_error(self):
        """Test creating an McpResponse without isError."""
        # Create an McpResponse without isError
        response: McpResponse = {'content': [{'type': 'text', 'text': 'Test content'}]}

        # Check that the fields are set correctly
        assert len(response['content']) == 1
        assert response['content'][0]['type'] == 'text'
        assert response['content'][0]['text'] == 'Test content'

        # Check that isError is not present
        assert 'isError' not in response

    def test_mcp_response_missing_content(self):
        """Test that an McpResponse can be created without content."""
        # Since McpResponse is defined with total=False, all keys are optional
        response: McpResponse = {'isError': False}

        # Check that isError is set correctly
        assert response.get('isError') is False

        # Check that content is not present
        assert 'content' not in response
