"""Tests for agent tool correctness using DeepEval."""

import os
import pytest
from awslabs.agent_test.agent_test_dataset import AgentEvaluationDataset, AgentTestCase
from awslabs.agent_test.agent_tool_test import AgentToolTest
from deepeval import assert_test
from deepeval.metrics.tool_correctness.tool_correctness import ToolCorrectnessMetric


# Get MCP settings from environment or use defaults
MCP_ARGS = ['mcp-server-time', '--local-timezone=US/Pacific']
AGENT_TEST_DATASET = os.environ.get('AGENT_TEST_DATASET', 'examples/agent_test_cases.yaml')


@pytest.fixture
def agent_test():
    """Create an agent test instance."""
    return AgentToolTest(
        mcp_args=MCP_ARGS,
        mcp_env=None,
        model_id=os.environ.get(
            'AGENT_TEST_MODEL_ID', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
        ),
        region_name=os.environ.get('AGENT_TEST_REGION', 'us-west-2'),
    )


@pytest.fixture
def test_dataset():
    """Load or create a test dataset."""
    # Load from file if it exists
    dataset_path = os.environ.get('AGENT_TEST_DATASET')
    if dataset_path and os.path.exists(dataset_path):
        if dataset_path.endswith('.yaml') or dataset_path.endswith('.yml'):
            return AgentEvaluationDataset.from_yaml(dataset_path)
        elif dataset_path.endswith('.json'):
            return AgentEvaluationDataset.from_json(dataset_path)

    # Otherwise use some default test cases with time MCP server tools
    return AgentEvaluationDataset(
        [
            AgentTestCase(
                input="What's the current time in Tokyo?",
                expected_tools=['get_current_time'],
                description='Testing the get_current_time tool',
            ),
            AgentTestCase(
                input='Convert 3:00 PM Los Angeles time to London time',
                expected_tools=['convert_time'],
                description='Testing time conversion between time zones',
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_case',
    [
        AgentTestCase(
            input="What's the current time in Tokyo?",
            expected_tools=['get_current_time'],
            description='Testing the get_current_time tool',
        ),
        AgentTestCase(
            input='Convert 3:00 PM Los Angeles time to London time',
            expected_tools=['convert_time'],
            description='Testing time conversion between time zones',
        ),
    ],
)
async def test_agent_tool_usage(test_case: AgentTestCase, agent_test: AgentToolTest):
    """Test that the agent uses the expected tools for different queries."""
    async with agent_test:
        # Create DeepEval test case by running the agent
        llm_test_case = await agent_test.create_test_case(
            prompt=test_case.input, expected_tools=test_case.expected_tools
        )

        # Define metrics - we use the tool correctness metric
        tool_metric = ToolCorrectnessMetric()

        # Assert using DeepEval's assertion utility
        assert_test(llm_test_case, [tool_metric])
