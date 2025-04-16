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
"""Tests for the clients module of the bedrock-kb-retrieval-mcp-server."""

import boto3
import pytest
from unittest.mock import MagicMock, patch
from awslabs.bedrock_kb_retrieval_mcp_server.knowledgebases.clients import (
    get_bedrock_agent_client,
    get_bedrock_agent_runtime_client,
)


class TestGetBedrockAgentRuntimeClient:
    """Tests for the get_bedrock_agent_runtime_client function."""

    @patch('boto3.client')
    def test_get_bedrock_agent_runtime_client_default(self, mock_boto3_client):
        """Test get_bedrock_agent_runtime_client with default parameters."""
        # Set up the mock
        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        # Call the function
        client = get_bedrock_agent_runtime_client()

        # Check that boto3.client was called with the correct arguments
        mock_boto3_client.assert_called_once_with('bedrock-agent-runtime', region_name='us-west-2')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.client')
    def test_get_bedrock_agent_runtime_client_with_region(self, mock_boto3_client):
        """Test get_bedrock_agent_runtime_client with a specific region."""
        # Set up the mock
        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        # Call the function with a specific region
        client = get_bedrock_agent_runtime_client(region_name='us-east-1')

        # Check that boto3.client was called with the correct arguments
        mock_boto3_client.assert_called_once_with('bedrock-agent-runtime', region_name='us-east-1')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.Session')
    def test_get_bedrock_agent_runtime_client_with_profile(self, mock_boto3_session):
        """Test get_bedrock_agent_runtime_client with a specific profile."""
        # Set up the mock
        mock_session = MagicMock()
        mock_boto3_session.return_value = mock_session
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client

        # Call the function with a specific profile
        client = get_bedrock_agent_runtime_client(profile_name='test-profile')

        # Check that boto3.Session was called with the correct arguments
        mock_boto3_session.assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct arguments
        mock_session.client.assert_called_once_with('bedrock-agent-runtime', region_name='us-west-2')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.Session')
    def test_get_bedrock_agent_runtime_client_with_region_and_profile(self, mock_boto3_session):
        """Test get_bedrock_agent_runtime_client with a specific region and profile."""
        # Set up the mock
        mock_session = MagicMock()
        mock_boto3_session.return_value = mock_session
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client

        # Call the function with a specific region and profile
        client = get_bedrock_agent_runtime_client(region_name='us-east-1', profile_name='test-profile')

        # Check that boto3.Session was called with the correct arguments
        mock_boto3_session.assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct arguments
        mock_session.client.assert_called_once_with('bedrock-agent-runtime', region_name='us-east-1')

        # Check that the function returns the client
        assert client == mock_client


class TestGetBedrockAgentClient:
    """Tests for the get_bedrock_agent_client function."""

    @patch('boto3.client')
    def test_get_bedrock_agent_client_default(self, mock_boto3_client):
        """Test get_bedrock_agent_client with default parameters."""
        # Set up the mock
        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        # Call the function
        client = get_bedrock_agent_client()

        # Check that boto3.client was called with the correct arguments
        mock_boto3_client.assert_called_once_with('bedrock-agent', region_name='us-west-2')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.client')
    def test_get_bedrock_agent_client_with_region(self, mock_boto3_client):
        """Test get_bedrock_agent_client with a specific region."""
        # Set up the mock
        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        # Call the function with a specific region
        client = get_bedrock_agent_client(region_name='us-east-1')

        # Check that boto3.client was called with the correct arguments
        mock_boto3_client.assert_called_once_with('bedrock-agent', region_name='us-east-1')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.Session')
    def test_get_bedrock_agent_client_with_profile(self, mock_boto3_session):
        """Test get_bedrock_agent_client with a specific profile."""
        # Set up the mock
        mock_session = MagicMock()
        mock_boto3_session.return_value = mock_session
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client

        # Call the function with a specific profile
        client = get_bedrock_agent_client(profile_name='test-profile')

        # Check that boto3.Session was called with the correct arguments
        mock_boto3_session.assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct arguments
        mock_session.client.assert_called_once_with('bedrock-agent', region_name='us-west-2')

        # Check that the function returns the client
        assert client == mock_client

    @patch('boto3.Session')
    def test_get_bedrock_agent_client_with_region_and_profile(self, mock_boto3_session):
        """Test get_bedrock_agent_client with a specific region and profile."""
        # Set up the mock
        mock_session = MagicMock()
        mock_boto3_session.return_value = mock_session
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client

        # Call the function with a specific region and profile
        client = get_bedrock_agent_client(region_name='us-east-1', profile_name='test-profile')

        # Check that boto3.Session was called with the correct arguments
        mock_boto3_session.assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct arguments
        mock_session.client.assert_called_once_with('bedrock-agent', region_name='us-east-1')

        # Check that the function returns the client
        assert client == mock_client
