"""Tests for agent_tool_test module.

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import pytest
import unittest.mock
from awslabs.agent_test.agent_tool_test import AgentToolTest
from deepeval.test_case.llm_test_case import LLMTestCase
from langchain_core.messages import AIMessage, ToolMessage


class TestAgentToolTest:
    """Test AgentToolTest class."""

    def test_initialization_default_params(self):
        """Test initialization with default parameters."""
        tool_test = AgentToolTest(mcp_args=['arg1', 'arg2'], mcp_env={'VAR1': 'value1'})
        assert tool_test.mcp_args == ['arg1', 'arg2']
        assert tool_test.mcp_env == {'VAR1': 'value1'}
        assert tool_test.model_id == 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
        assert tool_test.region_name == 'us-west-2'
        assert tool_test._harness is None

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        tool_test = AgentToolTest(
            mcp_args=['custom-arg'],
            mcp_env={'CUSTOM_VAR': 'custom_value'},
            model_id='custom-model-id',
            region_name='us-east-1',
        )
        assert tool_test.mcp_args == ['custom-arg']
        assert tool_test.mcp_env == {'CUSTOM_VAR': 'custom_value'}
        assert tool_test.model_id == 'custom-model-id'
        assert tool_test.region_name == 'us-east-1'

    @pytest.mark.asyncio
    async def test_context_manager_enter_exit(self):
        """Test async context manager entry and exit."""
        tool_test = AgentToolTest(['arg'], {'VAR': 'value'})

        # Mock harness
        mock_harness = unittest.mock.AsyncMock()

        with unittest.mock.patch(
            'awslabs.agent_test.agent_tool_test.AgentTestHarness', return_value=mock_harness
        ):
            # Test context manager entry
            result = await tool_test.__aenter__()

            # Verify harness setup
            mock_harness.__aenter__.assert_called_once()
            assert tool_test._harness == mock_harness
            assert result == tool_test

            # Test context manager exit
            exc_type, exc_val, exc_tb = None, None, None
            await tool_test.__aexit__(exc_type, exc_val, exc_tb)

            # Verify cleanup
            mock_harness.__aexit__.assert_called_once_with(exc_type, exc_val, exc_tb)
            assert tool_test._harness is None

    @pytest.mark.asyncio
    async def test_context_manager_exit_with_none_harness(self):
        """Test context manager exit when harness is already None."""
        tool_test = AgentToolTest(['arg'], {})
        tool_test._harness = None

        # Should not raise errors
        await tool_test.__aexit__(None, None, None)
        assert tool_test._harness is None

    @pytest.mark.asyncio
    async def test_create_test_case_with_ai_message_tool_calls(self):
        """Test create_test_case with AIMessage containing tool calls."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Create mock AIMessage with tool calls
        ai_message = AIMessage(
            content="I'll use the weather tool",
            tool_calls=[
                {'id': 'call_1', 'name': 'get_weather', 'args': {'location': 'Seattle'}},
                {'id': 'call_2', 'name': 'get_forecast', 'args': {'days': 3}},
            ],
        )

        # Mock agent response
        mock_agent.ainvoke.return_value = {
            'messages': [
                {'role': 'user', 'content': 'What is the weather?'},
                ai_message,
                AIMessage(content='The weather is sunny'),
            ]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(
            prompt='What is the weather?', expected_tools=['get_weather', 'get_forecast']
        )

        # Verify the test case
        assert isinstance(result, LLMTestCase)
        assert result.input == 'What is the weather?'
        assert result.actual_output == 'The weather is sunny'
        assert len(result.tools_called or []) == 2
        assert (result.tools_called or [])[0].name == 'get_weather'
        assert (result.tools_called or [])[1].name == 'get_forecast'
        assert len(result.expected_tools or []) == 2
        assert (result.expected_tools or [])[0].name == 'get_weather'
        assert (result.expected_tools or [])[1].name == 'get_forecast'

    @pytest.mark.asyncio
    async def test_create_test_case_with_dict_tool_calls(self):
        """Test create_test_case with dictionary format tool calls."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Mock agent response with dict format messages
        mock_agent.ainvoke.return_value = {
            'messages': [
                {'role': 'user', 'content': 'Get time'},
                {
                    'role': 'assistant',
                    'content': 'I will get the time',
                    'tool_calls': [
                        {'id': 'time_call_1', 'name': 'get_time', 'args': {}},
                        {'id': 'time_call_2', 'name': 'get_timezone', 'args': {'location': 'UTC'}},
                    ],
                },
                {'role': 'assistant', 'content': 'Current time is 12:00 PM'},
            ]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(
            prompt='Get time', expected_tools=['get_time'], actual_output='Custom output'
        )

        # Verify the test case
        assert isinstance(result, LLMTestCase)
        assert result.input == 'Get time'
        assert result.actual_output == 'Custom output'  # Should use provided output
        assert len(result.tools_called or []) == 2
        assert (result.tools_called or [])[0].name == 'get_time'
        assert (result.tools_called or [])[1].name == 'get_timezone'

    @pytest.mark.asyncio
    async def test_create_test_case_with_duplicate_tool_calls(self):
        """Test create_test_case handles duplicate tool call IDs."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Create messages with duplicate tool call IDs
        ai_message1 = AIMessage(
            content='First call',
            tool_calls=[{'id': 'dup_call', 'name': 'get_weather', 'args': {}}],
        )
        ai_message2 = AIMessage(
            content='Second call',
            tool_calls=[
                {'id': 'dup_call', 'name': 'get_forecast', 'args': {}}
            ],  # Same ID, different tool
        )

        mock_agent.ainvoke.return_value = {
            'messages': [ai_message1, ai_message2, AIMessage(content='Done')]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(
            prompt='Weather query', expected_tools=['get_weather']
        )

        # Should only have one tool call (deduplicated by ID)
        assert len(result.tools_called or []) == 1
        assert (result.tools_called or [])[0].name == 'get_forecast'  # Last one wins

    @pytest.mark.asyncio
    async def test_create_test_case_with_no_tool_calls(self):
        """Test create_test_case with no tool calls in response."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Mock agent response with no tool calls
        mock_agent.ainvoke.return_value = {
            'messages': [
                {'role': 'user', 'content': 'Hello'},
                AIMessage(content='Hello! How can I help?'),
            ]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(prompt='Hello', expected_tools=['some_tool'])

        # Verify the test case
        assert len(result.tools_called or []) == 0
        assert len(result.expected_tools or []) == 1
        assert (result.expected_tools or [])[0].name == 'some_tool'

    @pytest.mark.asyncio
    async def test_create_test_case_with_empty_messages(self):
        """Test create_test_case with empty messages list."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Mock agent response with empty messages
        mock_agent.ainvoke.return_value = {'messages': []}

        # Test create_test_case
        result = await tool_test.create_test_case(prompt='Empty test', expected_tools=['tool1'])

        # Verify the test case
        assert result.input == 'Empty test'
        assert result.actual_output == ''
        assert len(result.tools_called or []) == 0

    @pytest.mark.asyncio
    async def test_create_test_case_without_context_manager(self):
        """Test create_test_case raises error when not used as context manager."""
        tool_test = AgentToolTest(['arg'], {})

        with pytest.raises(RuntimeError, match='AgentToolTest must be used as a context manager'):
            await tool_test.create_test_case('test', ['tool'])

    @pytest.mark.asyncio
    async def test_create_test_case_with_message_content_extraction(self):
        """Test create_test_case extracts content from different message types."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Mock agent response with various message types
        mock_agent.ainvoke.return_value = {
            'messages': [
                AIMessage(content='Response with content attribute'),
                {'role': 'assistant', 'content': 'Dict message with content'},
                unittest.mock.Mock(spec=[]),  # Mock without content attribute
            ]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(
            prompt='Test content extraction', expected_tools=[]
        )

        # Should use the last message's content (empty string for mock without content)
        assert result.actual_output == ''

    def test_run_test_synchronous_wrapper(self):
        """Test run_test synchronous wrapper."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock components
        mock_test_case = unittest.mock.Mock()
        mock_metric = unittest.mock.Mock()
        mock_metric.score = 0.85
        mock_metric.reason = 'Test passed'

        # Mock asyncio.run to avoid getting stuck
        with (
            unittest.mock.patch(
                'awslabs.agent_test.agent_tool_test.asyncio.run'
            ) as mock_asyncio_run,
            unittest.mock.patch(
                'awslabs.agent_test.agent_tool_test.ToolCorrectnessMetric',
                return_value=mock_metric,
            ),
        ):
            # Mock asyncio.run to return the expected result
            mock_asyncio_run.return_value = {
                'score': 0.85,
                'reason': 'Test passed',
                'test_case': mock_test_case,
            }

            # Test run_test
            result = tool_test.run_test('test prompt', ['test_tool'])

            # Verify result
            assert result['score'] == 0.85
            assert result['reason'] == 'Test passed'
            assert result['test_case'] == mock_test_case

            # Verify asyncio.run was called
            mock_asyncio_run.assert_called_once()

    def test_run_test_with_kwargs(self):
        """Test run_test with additional kwargs."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock the components
        mock_test_case = unittest.mock.Mock()
        mock_metric = unittest.mock.Mock()
        mock_metric.score = 0.95
        mock_metric.reason = 'Perfect score'

        # Mock asyncio.run to avoid getting stuck
        with (
            unittest.mock.patch(
                'awslabs.agent_test.agent_tool_test.asyncio.run'
            ) as mock_asyncio_run,
            unittest.mock.patch(
                'awslabs.agent_test.agent_tool_test.ToolCorrectnessMetric',
                return_value=mock_metric,
            ),
        ):
            # Mock asyncio.run to return the expected result
            mock_asyncio_run.return_value = {
                'score': 0.95,
                'reason': 'Perfect score',
                'test_case': mock_test_case,
            }

            # Test run_test with kwargs
            result = tool_test.run_test(
                'test prompt', ['test_tool'], actual_output='custom output'
            )

            # Verify result
            assert result['score'] == 0.95
            assert result['reason'] == 'Perfect score'
            assert result['test_case'] == mock_test_case

            # Verify asyncio.run was called
            mock_asyncio_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_test_case_with_tool_message_ignored(self):
        """Test create_test_case ignores ToolMessage instances."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Create response with AIMessage tool calls and ToolMessage responses
        ai_message = AIMessage(
            content='Using tool', tool_calls=[{'id': 'call_1', 'name': 'get_data', 'args': {}}]
        )
        tool_message = ToolMessage(content='Tool response', tool_call_id='call_1')

        mock_agent.ainvoke.return_value = {
            'messages': [
                ai_message,
                tool_message,  # This should be ignored
                AIMessage(content='Final response'),
            ]
        }

        # Test create_test_case
        result = await tool_test.create_test_case(
            prompt='Test with tool message', expected_tools=['get_data']
        )

        # Should only count the AIMessage tool call, not the ToolMessage
        assert len(result.tools_called or []) == 1
        assert (result.tools_called or [])[0].name == 'get_data'

    @pytest.mark.asyncio
    async def test_create_test_case_logs_response_messages(self):
        """Test create_test_case logs response messages."""
        tool_test = AgentToolTest(['arg'], {})

        # Mock harness and agent
        mock_harness = unittest.mock.AsyncMock()
        mock_agent = unittest.mock.AsyncMock()
        tool_test._harness = mock_harness
        mock_harness.get_agent.return_value = mock_agent

        # Mock messages with pretty_print method
        mock_message = unittest.mock.Mock(spec=AIMessage)

        mock_agent.ainvoke.return_value = {
            'messages': [mock_message, AIMessage(content='Response')]
        }

        # Test create_test_case
        await tool_test.create_test_case(prompt='Test logging', expected_tools=[])

        # Verify pretty_print was called on the mock message
        mock_message.pretty_print.assert_called_once()
