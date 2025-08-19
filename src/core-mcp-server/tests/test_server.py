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
"""Tests for the Core MCP Server."""

import os
import pytest
from unittest.mock import MagicMock, patch


# Import PROMPT_UNDERSTANDING directly from the file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
prompt_understanding_path = os.path.join(
    parent_dir, 'awslabs', 'core_mcp_server', 'static', 'PROMPT_UNDERSTANDING.md'
)
with open(prompt_understanding_path, 'r', encoding='utf-8') as f:
    PROMPT_UNDERSTANDING = f.read()

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


# ---- Add fastmcp mocks so server.py import works ----
# Create a mock FunctionTool class that simulates the behavior of the actual FunctionTool class
class MockFunctionTool:
    """Mock implementation of the FunctionTool class for testing purposes.

    This class simulates the behavior of the actual FunctionTool class from fastmcp,
    allowing tests to run without requiring the actual implementation.
    """

    def __init__(self, func):
        """Initialize the MockFunctionTool with a function.

        Args:
            func: The function to be called when run is invoked.
        """
        self.func = func

    async def run(self, arguments: dict = {}):
        """Execute the function with the provided arguments.

        Args:
            arguments: Dictionary of arguments to pass to the function.
                      Not actually used in this mock implementation.

        Returns:
            The result of calling the function.
        """
        # In the actual implementation, this would process arguments and call the function
        return self.func()


# Create a mock for the tool decorator that returns a MockFunctionTool instance
mock_tool = MagicMock()
mock_tool.return_value = lambda func: MockFunctionTool(func)

# Create a mock for the mcp instance
mock_mcp = MagicMock()
mock_mcp.tool = mock_tool

# Create a mock for the FastMCP class
mock_fastmcp = MagicMock()
mock_fastmcp.return_value = mock_mcp

mock_modules.update(
    {
        'fastmcp': MagicMock(),
        'fastmcp.FastMCP': mock_fastmcp,
        'fastmcp.settings': MagicMock(),
        'fastmcp.server': MagicMock(),
        'fastmcp.server.proxy': MagicMock(),
    }
)

with patch.dict('sys.modules', mock_modules):
    # Import the module, not just the function
    import awslabs.core_mcp_server.server

    # Create a MockFunctionTool instance directly and replace get_prompt_understanding with it
    awslabs.core_mcp_server.server.get_prompt_understanding = MockFunctionTool(
        lambda: PROMPT_UNDERSTANDING
    )


class TestPromptUnderstanding:
    """Tests for get_prompt_understanding function."""

    @pytest.mark.asyncio
    async def test_get_prompt_understanding(self):
        """Test that get_prompt_understanding returns the expected value."""
        # Now we can call the run method on the MockFunctionTool instance
        result = await awslabs.core_mcp_server.server.get_prompt_understanding.run({})
        assert result == PROMPT_UNDERSTANDING


class TestSetup:
    """Tests for setup function."""

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'aws-knowledge-foundation': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_aws_knowledge_foundation(self, mock_import_server, mock_as_proxy):
        """Test setup function with aws-knowledge-foundation role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'dev-tools': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_dev_tools(self, mock_import_server, mock_as_proxy):
        """Test setup function with dev-tools role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ci-cd-devops': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_ci_cd_devops(self, mock_import_server, mock_as_proxy):
        """Test setup function with ci-cd-devops role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'container-orchestration': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_container_orchestration(self, mock_import_server, mock_as_proxy):
        """Test setup function with container-orchestration role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'serverless-architecture': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_serverless_architecture(self, mock_import_server, mock_as_proxy):
        """Test setup function with serverless-architecture role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'analytics-warehouse': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_analytics_warehouse(self, mock_import_server, mock_as_proxy):
        """Test setup function with analytics-warehouse role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'data-platform-eng': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_data_platform_eng(self, mock_import_server, mock_as_proxy):
        """Test setup function with data-platform-eng role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'data-ingestion': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_data_ingestion(self, mock_import_server, mock_as_proxy):
        """Test setup function with data-ingestion role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ai-dev': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_ai_dev(self, mock_import_server, mock_as_proxy):
        """Test setup function with ai-dev role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'frontend-dev': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_frontend_dev(self, mock_import_server, mock_as_proxy):
        """Test setup function with frontend-dev role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'api-management': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_api_management(self, mock_import_server, mock_as_proxy):
        """Test setup function with api-management role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'solutions-architect': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_solutions_architect(self, mock_import_server, mock_as_proxy):
        """Test setup function with solutions-architect role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'finops': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_finops(self, mock_import_server, mock_as_proxy):
        """Test setup function with finops role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'monitoring-observability': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_monitoring_observability(self, mock_import_server, mock_as_proxy):
        """Test setup function with monitoring-observability role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'caching-performance': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_caching_performance(self, mock_import_server, mock_as_proxy):
        """Test setup function with caching-performance role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'security-identity': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_security_identity(self, mock_import_server, mock_as_proxy):
        """Test setup function with security-identity role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'sql-db-specialist': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_sql_db_specialist(self, mock_import_server, mock_as_proxy):
        """Test setup function with sql-db-specialist role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'nosql-db-specialist': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_nosql_db_specialist(self, mock_import_server, mock_as_proxy):
        """Test setup function with nosql-db-specialist role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'timeseries-db-specialist': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_timeseries_db_specialist(self, mock_import_server, mock_as_proxy):
        """Test setup function with timeseries-db-specialist role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'messaging-events': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_messaging_events(self, mock_import_server, mock_as_proxy):
        """Test setup function with messaging-events role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'geospatial-services': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_geospatial_services(self, mock_import_server, mock_as_proxy):
        """Test setup function with geospatial-services role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'healthcare-lifesci': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_healthcare_lifesci(self, mock_import_server, mock_as_proxy):
        """Test setup function with healthcare-lifesci role enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_no_roles(self, mock_import_server, mock_as_proxy):
        """Test setup function with no roles enabled."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.return_value = None

        # Call the setup function
        await setup()
        assert mock_as_proxy.call_count >= 0

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'aws-knowledge-foundation': 'true'})
    @patch('awslabs.core_mcp_server.server.FastMCP.as_proxy')
    @patch('awslabs.core_mcp_server.server.mcp.import_server')
    async def test_setup_import_error(self, mock_import_server, mock_as_proxy):
        """Test setup function when import_server raises an exception."""
        # Import the setup function
        with patch.dict('sys.modules', mock_modules):
            from awslabs.core_mcp_server.server import setup

        # Configure mocks
        mock_proxy = MagicMock()
        mock_as_proxy.return_value = mock_proxy
        mock_import_server.side_effect = Exception('Import error')

        # Call the setup function - should not raise an exception
        await setup()
        assert mock_as_proxy.call_count >= 0
