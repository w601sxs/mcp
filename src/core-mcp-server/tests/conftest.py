# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Configuration for pytest."""

import pytest
import sys
from unittest.mock import AsyncMock, MagicMock


# --- Global mocks for MCP servers ---
mock_modules = {
    # FastMCP core
    'fastmcp': MagicMock(),
    'fastmcp.settings': MagicMock(),
    'fastmcp.server': MagicMock(),
    'fastmcp.server.proxy': MagicMock(),
    # MCP servers (mocked so imports don’t fail)
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

# Patch async functions in FastMCP so 'await' works in tests
fastmcp_mock = mock_modules['fastmcp']
fastmcp_instance = fastmcp_mock.FastMCP.return_value
# fastmcp_instance.tool = AsyncMock()
# fastmcp_instance.run = AsyncMock()
fastmcp_instance.start = AsyncMock()

# Inject mocks globally
sys.modules.update(mock_modules)


# --- pytest markers & options ---
def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        '--run-live',
        action='store_true',
        default=False,
        help='Run tests that make live API calls',
    )


def pytest_collection_modifyitems(config, items):
    """Skip live tests unless --run-live is specified."""
    if not config.getoption('--run-live'):
        skip_live = pytest.mark.skip(reason='need --run-live option to run')
        for item in items:
            if 'live' in item.keywords:
                item.add_marker(skip_live)
