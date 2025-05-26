"""Tests for agent_test_harness module.

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import pytest
import unittest.mock
from awslabs.agent_test.agent_test_harness import AgentTestHarness


class TestAgentTestHarness:
    """Test AgentTestHarness class."""

    def test_initialization_default_params(self):
        """Test initialization with default parameters."""
        harness = AgentTestHarness(mcp_args=['arg1', 'arg2'], mcp_env={'VAR1': 'value1'})
        assert harness.mcp_args == ['arg1', 'arg2']
        assert harness.mcp_env == {'VAR1': 'value1'}
        assert harness.model_id == 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
        assert harness.region_name == 'us-west-2'
        assert harness.mcp_command == 'uvx'

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        harness = AgentTestHarness(
            mcp_args=['custom-arg'],
            mcp_env={'CUSTOM_VAR': 'custom_value'},
            model_id='custom-model-id',
            region_name='us-east-1',
            mcp_command='custom-command',
        )
        assert harness.mcp_args == ['custom-arg']
        assert harness.mcp_env == {'CUSTOM_VAR': 'custom_value'}
        assert harness.model_id == 'custom-model-id'
        assert harness.region_name == 'us-east-1'
        assert harness.mcp_command == 'custom-command'

    def test_initialization_none_env(self):
        """Test initialization with None environment."""
        harness = AgentTestHarness(mcp_args=['arg1'], mcp_env=None)
        assert harness.mcp_args == ['arg1']
        assert harness.mcp_env is None

    def test_get_server_parameters(self):
        """Test _get_server_parameters method."""
        harness = AgentTestHarness(
            mcp_args=['server', 'arg'],
            mcp_env={'TEST_VAR': 'test_value'},
            mcp_command='test-command',
        )

        with unittest.mock.patch(
            'awslabs.agent_test.agent_test_harness.StdioServerParameters'
        ) as mock_params:
            result = harness._get_server_parameters()

            mock_params.assert_called_once_with(
                command='test-command', args=['server', 'arg'], env={'TEST_VAR': 'test_value'}
            )
            assert result == mock_params.return_value

    def test_get_mcp_stdio_client(self):
        """Test _get_mcp_stdio_client method."""
        harness = AgentTestHarness(mcp_args=['arg'], mcp_env={'VAR': 'value'})

        with (
            unittest.mock.patch.object(harness, '_get_server_parameters') as mock_get_params,
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.stdio_client'
            ) as mock_stdio_client,
        ):
            mock_params = unittest.mock.Mock()
            mock_get_params.return_value = mock_params

            result = harness._get_mcp_stdio_client()

            mock_get_params.assert_called_once()
            mock_stdio_client.assert_called_once_with(mock_params)
            assert result == mock_stdio_client.return_value

    @pytest.mark.asyncio
    async def test_context_manager_enter_exit(self):
        """Test async context manager entry and exit."""
        harness = AgentTestHarness(mcp_args=['test-arg'], mcp_env={'TEST': 'value'})

        # Mock all the dependencies
        mock_mcp_client = unittest.mock.AsyncMock()
        mock_read_mcp = unittest.mock.Mock()
        mock_write_mcp = unittest.mock.Mock()
        mock_session = unittest.mock.AsyncMock()

        with (
            unittest.mock.patch.object(
                harness, '_get_mcp_stdio_client', return_value=mock_mcp_client
            ),
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.ClientSession', return_value=mock_session
            ),
        ):
            # Setup mock returns
            mock_mcp_client.__aenter__.return_value = (mock_read_mcp, mock_write_mcp)

            # Test context manager entry
            result = await harness.__aenter__()

            # Verify all setup calls
            mock_mcp_client.__aenter__.assert_called_once()
            mock_session.__aenter__.assert_called_once()
            mock_session.initialize.assert_called_once()

            # Verify state
            assert harness._mcp_client == mock_mcp_client
            assert harness._read_mcp == mock_read_mcp
            assert harness._write_mcp == mock_write_mcp
            assert harness._session == mock_session
            assert result == harness

            # Test context manager exit
            exc_type, exc_val, exc_tb = None, None, None
            await harness.__aexit__(exc_type, exc_val, exc_tb)

            # Verify cleanup calls
            mock_session.__aexit__.assert_called_once_with(exc_type, exc_val, exc_tb)
            mock_mcp_client.__aexit__.assert_called_once_with(exc_type, exc_val, exc_tb)

            # Verify state cleanup
            assert harness._session is None
            assert harness._mcp_client is None
            assert harness._agent is None

    @pytest.mark.asyncio
    async def test_context_manager_exit_with_none_session(self):
        """Test context manager exit when session is already None."""
        harness = AgentTestHarness(['arg'], {})

        # Set up partial state
        mock_mcp_client = unittest.mock.AsyncMock()
        harness._mcp_client = mock_mcp_client
        harness._session = None  # Already None

        # Test exit
        await harness.__aexit__(None, None, None)

        # Should still clean up mcp_client
        mock_mcp_client.__aexit__.assert_called_once()
        assert harness._mcp_client is None

    @pytest.mark.asyncio
    async def test_context_manager_exit_with_none_mcp_client(self):
        """Test context manager exit when mcp_client is already None."""
        harness = AgentTestHarness(['arg'], {})

        # Set up partial state
        harness._session = None
        harness._mcp_client = None

        # Test exit - should not raise errors
        await harness.__aexit__(None, None, None)

        # Verify final state
        assert harness._session is None
        assert harness._mcp_client is None
        assert harness._agent is None

    @pytest.mark.asyncio
    async def test_get_agent_without_context_manager(self):
        """Test get_agent raises error when not used as context manager."""
        harness = AgentTestHarness(['arg'], {})

        with pytest.raises(
            RuntimeError, match='AgentTestHarness must be used as a context manager'
        ):
            await harness.get_agent()

    @pytest.mark.asyncio
    async def test_get_agent_creates_agent_once(self):
        """Test get_agent creates agent once and caches it."""
        harness = AgentTestHarness(
            mcp_args=['arg'], mcp_env={}, model_id='test-model', region_name='us-east-1'
        )

        # Mock session and dependencies
        mock_session = unittest.mock.AsyncMock()
        mock_tools = [unittest.mock.Mock(), unittest.mock.Mock()]
        mock_agent = unittest.mock.Mock()

        harness._session = mock_session  # Simulate being in context manager

        with (
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.load_mcp_tools', return_value=mock_tools
            ) as mock_load_tools,
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.create_react_agent', return_value=mock_agent
            ) as mock_create_agent,
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.ChatBedrockConverse'
            ) as mock_chat_bedrock,
        ):
            # First call
            result1 = await harness.get_agent()

            # Verify agent creation
            mock_load_tools.assert_called_once_with(mock_session)
            mock_chat_bedrock.assert_called_once_with(model='test-model', region_name='us-east-1')
            mock_create_agent.assert_called_once_with(
                model=mock_chat_bedrock.return_value, tools=mock_tools
            )
            assert result1 == mock_agent
            assert harness._agent == mock_agent

            # Second call should return cached agent
            result2 = await harness.get_agent()

            # Verify no additional calls were made
            assert mock_load_tools.call_count == 1
            assert mock_chat_bedrock.call_count == 1
            assert mock_create_agent.call_count == 1
            assert result2 == mock_agent

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test full workflow from context manager to agent creation."""
        harness = AgentTestHarness(
            mcp_args=['workflow-test'],
            mcp_env={'WORKFLOW': 'test'},
            model_id='workflow-model',
            region_name='us-west-1',
        )

        # Mock all dependencies
        mock_mcp_client = unittest.mock.AsyncMock()
        mock_read_mcp = unittest.mock.Mock()
        mock_write_mcp = unittest.mock.Mock()
        mock_session = unittest.mock.AsyncMock()
        mock_tools = [unittest.mock.Mock()]
        mock_agent = unittest.mock.Mock()

        with (
            unittest.mock.patch.object(
                harness, '_get_mcp_stdio_client', return_value=mock_mcp_client
            ),
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.ClientSession', return_value=mock_session
            ),
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.load_mcp_tools', return_value=mock_tools
            ),
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.create_react_agent', return_value=mock_agent
            ),
            unittest.mock.patch(
                'awslabs.agent_test.agent_test_harness.ChatBedrockConverse'
            ) as mock_chat_bedrock,
        ):
            # Setup mock returns
            mock_mcp_client.__aenter__.return_value = (mock_read_mcp, mock_write_mcp)

            # Test full workflow
            async with harness as h:
                assert h == harness
                agent = await h.get_agent()
                assert agent == mock_agent

                # Verify model was created with correct parameters
                mock_chat_bedrock.assert_called_once_with(
                    model='workflow-model', region_name='us-west-1'
                )

            # After exiting context, verify cleanup
            assert harness._session is None
            assert harness._mcp_client is None
            assert harness._agent is None
