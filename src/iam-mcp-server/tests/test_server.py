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

"""Tests for the AWS IAM MCP Server."""

import pytest
from awslabs.iam_mcp_server.aws_client import get_iam_client
from awslabs.iam_mcp_server.context import Context
from awslabs.iam_mcp_server.errors import (
    IamPermissionError,
    IamResourceNotFoundError,
    handle_iam_error,
)
from awslabs.iam_mcp_server.models import UsersListResponse
from botocore.exceptions import ClientError as BotoClientError
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch


def test_get_iam_client():
    """Test IAM client creation."""
    with patch('boto3.client') as mock_client:
        mock_client.return_value = Mock()
        client = get_iam_client()
        assert client is not None
        mock_client.assert_called_once_with('iam')


def test_get_iam_client_with_region():
    """Test IAM client creation with region."""
    with patch('boto3.client') as mock_client:
        mock_client.return_value = Mock()
        client = get_iam_client(region='us-west-2')
        assert client is not None
        mock_client.assert_called_once_with('iam', region_name='us-west-2')


def test_handle_iam_error_access_denied():
    """Test handling of AccessDenied error."""
    error_response = {
        'Error': {
            'Code': 'AccessDenied',
            'Message': 'User is not authorized to perform this action',
        }
    }
    boto_error = BotoClientError(error_response, 'GetUser')

    handled_error = handle_iam_error(boto_error)

    assert isinstance(handled_error, IamPermissionError)
    assert 'Access denied' in str(handled_error)


def test_handle_iam_error_no_such_entity():
    """Test handling of NoSuchEntity error."""
    error_response = {'Error': {'Code': 'NoSuchEntity', 'Message': 'The user does not exist'}}
    boto_error = BotoClientError(error_response, 'GetUser')

    handled_error = handle_iam_error(boto_error)

    assert isinstance(handled_error, IamResourceNotFoundError)
    assert 'Resource not found' in str(handled_error)


def test_context_initialization():
    """Test Context initialization."""
    Context.initialize(readonly=True, region='us-east-1')

    assert Context.is_readonly() is True
    assert Context.get_region() == 'us-east-1'


def test_context_readonly_mode():
    """Test Context readonly mode."""
    Context.initialize(readonly=False)
    assert Context.is_readonly() is False

    Context.initialize(readonly=True)
    assert Context.is_readonly() is True


@pytest.mark.asyncio
async def test_list_users_mock():
    """Test list_users function with mocked IAM client."""
    from awslabs.iam_mcp_server.server import list_users

    mock_response = {
        'Users': [
            {
                'UserName': 'test-user',
                'UserId': 'AIDACKCEVSQ6C2EXAMPLE',
                'Arn': 'arn:aws:iam::123456789012:user/test-user',
                'Path': '/',
                'CreateDate': datetime(2023, 1, 1),
            }
        ],
        'IsTruncated': False,
    }

    mock_ctx = AsyncMock()

    with patch('awslabs.iam_mcp_server.server.get_iam_client') as mock_get_client:
        mock_client = Mock()
        mock_client.list_users.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = await list_users(mock_ctx)

        assert isinstance(result, UsersListResponse)
        assert len(result.users) == 1
        assert result.users[0].user_name == 'test-user'
        assert result.count == 1
        assert result.is_truncated is False


@pytest.mark.asyncio
async def test_create_user_readonly_mode():
    """Test create_user function in readonly mode."""
    from awslabs.iam_mcp_server.errors import IamClientError
    from awslabs.iam_mcp_server.server import create_user

    # Set readonly mode
    Context.initialize(readonly=True)

    mock_ctx = AsyncMock()

    with pytest.raises(IamClientError) as exc_info:
        await create_user(mock_ctx, user_name='test-user')

    assert 'read-only mode' in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_user_success():
    """Test successful user creation."""
    from awslabs.iam_mcp_server.models import CreateUserResponse
    from awslabs.iam_mcp_server.server import create_user

    # Disable readonly mode
    Context.initialize(readonly=False)

    mock_response = {
        'User': {
            'UserName': 'new-user',
            'UserId': 'AIDACKCEVSQ6C2EXAMPLE',
            'Arn': 'arn:aws:iam::123456789012:user/new-user',
            'Path': '/',
            'CreateDate': datetime(2023, 1, 1),
        }
    }

    mock_ctx = AsyncMock()

    with patch('awslabs.iam_mcp_server.server.get_iam_client') as mock_get_client:
        mock_client = Mock()
        mock_client.create_user.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = await create_user(mock_ctx, user_name='new-user')

        assert isinstance(result, CreateUserResponse)
        assert result.user.user_name == 'new-user'
        assert 'Successfully created user: new-user' in result.message
