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

"""AgentCore MCP Server - Identity Management Module.

Contains API key credential provider creation, management, and runtime utilities.

MCP TOOLS IMPLEMENTED:
• create_credential_provider - Create API key credential providers
• list_credential_providers - List all credential providers
• get_credential_provider - Get specific credential provider details
• update_credential_provider - Update existing credential providers
• delete_credential_provider - Delete credential providers

"""

import time
from .utils import SDK_AVAILABLE
from mcp.server.fastmcp import FastMCP
from pydantic import Field


# ============================================================================
# IDENTITY MANAGEMENT TOOLS
# ============================================================================


def register_identity_tools(mcp: FastMCP):
    """Register identity and credential provider management tools."""

    @mcp.tool()
    async def manage_credentials(
        action: str = Field(
            default='list',
            description='Credential action',
            enum=['create', 'list', 'delete', 'get', 'update'],
        ),
        provider_name: str = Field(default='', description='Name of the credential provider'),
        api_key: str = Field(default='', description='API key value (for create/update)'),
        description: str = Field(default='', description='Description of the credential provider'),
        region: str = Field(default='us-east-1', description='AWS region'),
    ) -> str:
        """Security: IDENTITY & CREDENTIAL MANAGEMENT.

        Manage API key credential providers for use in agents at runtime.
        These providers allow agents to securely access API keys without hardcoding them.

        Actions:
        - create: Create a new API key credential provider
        - list: List all credential providers
        - delete: Delete a credential provider
        - get: Get details of a specific provider
        - update: Update an existing provider
        """
        if not SDK_AVAILABLE:
            return """X AgentCore SDK Not Available

To use credential provider functionality:
1. Install: `uv add bedrock-agentcore bedrock-agentcore-starter-toolkit`
2. Configure AWS credentials: `aws configure`
3. Retry credential operations

Alternative: Use AWS Console for credential management"""

        try:
            from bedrock_agentcore.services.identity import IdentityClient

            # Initialize Identity Client
            identity_client = IdentityClient(region=region)

            # Action: create - Create new API key credential provider
            if action == 'create':
                if not provider_name:
                    return """X Error: provider_name is required for create action

Example:
```python
manage_credentials(
    action="create",
    provider_name="openai-api-key", # pragma: allowlist secret
    api_key="sk-...", # pragma: allowlist secret
    description="OpenAI API key for GPT models" # pragma: allowlist secret
)
```"""

                if not api_key:
                    return """X Error: api_key is required for create action

Example:
```python
manage_credentials(
    action="create",
    provider_name="my-api-provider", # pragma: allowlist secret
    api_key="your-actual-api-key-here" # pragma: allowlist secret
)
```"""

                try:
                    # Create the credential provider
                    provider_config = {'name': provider_name, 'apiKey': api_key}

                    if description:
                        provider_config['description'] = description

                    result = identity_client.create_api_key_credential_provider(provider_config)

                    return f"""# OK Credential Provider Created Successfully

## Provider Details:
- Name: `{provider_name}`
- Type: API Key Credential Provider
- Region: `{region}`
- Created: {time.strftime('%Y-%m-%d %H:%M:%S')}
{f'- Description: {description}' if description else ''}

## Usage in Agent Code:
```python
from bedrock_agentcore.identity.auth import requires_api_key

@requires_api_key(provider_name="{provider_name}")
async def my_function(*, api_key: str):
    # The API key is automatically injected
    print(f"Using API key: {{api_key[:8]}}...")
    # Use the API key for authentication
    headers = {{"Authorization": f"Bearer {{api_key}}"}}
    # Make your API calls...
```

## Next Steps:
1. List providers: `manage_credentials(action="list")`
2. Use in agents: Import and use the `@requires_api_key` decorator
3. Update if needed: `manage_credentials(action="update", provider_name="{provider_name}")`

Secure: Security: API key is securely stored and encrypted by AWS AgentCore Identity service."""

                except Exception as create_error:
                    return f"""X Failed to Create Credential Provider

Provider Name: `{provider_name}`
Error: {str(create_error)}

Possible Causes:
- Provider name already exists
- Invalid API key format
- Insufficient AWS permissions
- Network connectivity issues

Troubleshooting:
1. Check if provider exists: `manage_credentials(action="list")`
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Ensure unique provider name
4. Check API key format"""

            # Action: list - List all credential providers
            elif action == 'list':
                try:
                    # Get all credential providers
                    providers = identity_client.list_credential_providers()

                    if not providers or len(providers) == 0:
                        return f"""# Security: No Credential Providers Found

Region: {region}

## Getting Started:
Create your first credential provider:
```python
manage_credentials(
    action="create",
    provider_name="my-api-key", # pragma: allowlist secret
    api_key="your-api-key-here", # pragma: allowlist secret
    description="My API service credentials" # pragma: allowlist secret
)
```

## Common Use Cases:
- OpenAI API: Store GPT model API keys
- Third-party APIs: Store authentication tokens
- External Services: Store service credentials
- Custom APIs: Store your own API keys

## Benefits:
- Secure: Secure storage with AWS encryption
- Target: Runtime injection via decorators
- Note: No hardcoded keys in agent code
- Reuse: Reusable across multiple agents"""

                    # Format results
                    result_parts = []
                    result_parts.append('# Security: Credential Providers')
                    result_parts.append('')
                    result_parts.append(f'Region: {region}')
                    result_parts.append(f'Total Providers: {len(providers)}')
                    result_parts.append('')

                    # List each provider
                    for i, provider in enumerate(providers, 1):
                        name = provider.get('name', 'Unknown')
                        provider_type = provider.get('type', 'API Key')
                        created_at = provider.get('createdAt', 'Unknown')
                        description = provider.get('description', '')

                        result_parts.append(f'## {i}. {name}')
                        result_parts.append(f'- Type: {provider_type}')
                        result_parts.append(f'- Created: {created_at}')
                        if description:
                            result_parts.append(f'- Description: {description}')
                        result_parts.append(
                            f'- Usage: `@requires_api_key(provider_name="{name}")`'
                        )
                        result_parts.append(
                            f'- Delete: `manage_credentials(action="delete", provider_name="{name}")`'
                        )
                        result_parts.append('')

                    result_parts.append('## Usage Example:')
                    result_parts.append('```python')
                    result_parts.append(
                        'from bedrock_agentcore.identity.auth import requires_api_key'
                    )
                    result_parts.append('')
                    result_parts.append(
                        f'@requires_api_key(provider_name="{providers[0].get("name", "your-provider")}")'
                    )
                    result_parts.append('async def call_external_api(*, api_key: str):')
                    result_parts.append("    headers = {'Authorization': f'Bearer {api_key}'}")
                    result_parts.append('    # Make your API calls...')
                    result_parts.append('```')
                    result_parts.append('')
                    result_parts.append('## Management:')
                    result_parts.append(
                        '- Create new: `manage_credentials(action="create", provider_name="name", api_key="key")`'  # pragma: allowlist secret
                    )
                    result_parts.append(
                        '- Get details: `manage_credentials(action="get", provider_name="name")`'
                    )
                    result_parts.append(
                        '- Update: `manage_credentials(action="update", provider_name="name", api_key="new_key")`'  # pragma: allowlist secret
                    )

                    return '\n'.join(result_parts)

                except Exception as list_error:
                    return f"""X Failed to List Credential Providers

Region: {region}
Error: {str(list_error)}

Possible Causes:
- AWS credentials not configured
- Insufficient permissions for AgentCore Identity service
- Network connectivity issues

Troubleshooting:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify AgentCore permissions
3. Try creating a provider first"""

            # Action: delete - Delete credential provider
            elif action == 'delete':
                if not provider_name:
                    return 'X Error: provider_name is required for delete action'

                try:
                    # Delete the credential provider
                    identity_client.delete_credential_provider(provider_name)

                    return f"""# OK Credential Provider Deleted

## Deleted Provider:
- Name: `{provider_name}`
- Status: Permanently deleted
- Region: `{region}`

## ! Important Notes:
- Deletion is permanent and cannot be undone
- Any agents using this provider will lose access to the API key
- Update agent code to remove references to this provider

## Next Steps:
1. Update agents: Remove `@requires_api_key(provider_name="{provider_name}")` decorators
2. Check remaining: `manage_credentials(action="list")`
3. Create new if needed: `manage_credentials(action="create", ...)`

Provider `{provider_name}` has been completely removed."""

                except Exception as delete_error:
                    return f"""X Failed to Delete Credential Provider

Provider Name: `{provider_name}`
Error: {str(delete_error)}

Possible Causes:
- Provider doesn't exist
- Provider is currently in use by agents
- Insufficient permissions

Check Status: `manage_credentials(action="list")` to see available providers"""

            # Action: get - Get provider details
            elif action == 'get':
                if not provider_name:
                    return 'X Error: provider_name is required for get action'

                try:
                    # Get provider details
                    provider = identity_client.get_credential_provider(provider_name)

                    return f"""# Security: Credential Provider Details

## Provider Information:
- Name: `{provider.get('name', provider_name)}`
- Type: {provider.get('type', 'API Key')}
- Region: `{region}`
- Created: {provider.get('createdAt', 'Unknown')}
- Status: {provider.get('status', 'Active')}
{f'- Description: {provider.get("description", "")}' if provider.get('description') else ''}

## Usage in Agent Code:
```python
from bedrock_agentcore.identity.auth import requires_api_key

@requires_api_key(provider_name="{provider_name}")
async def my_function(*, api_key: str):
    # API key automatically injected here
    headers = {{"Authorization": f"Bearer {{api_key}}"}}
    # Use for API calls...
```

## Management Options:
- Update: `manage_credentials(action="update", provider_name="{provider_name}", api_key="new_key")` # pragma: allowlist secret
- Delete: `manage_credentials(action="delete", provider_name="{provider_name}")`
- List all: `manage_credentials(action="list")`

Secure: Security: API key value is never displayed for security reasons."""

                except Exception as get_error:
                    return f"""X Failed to Get Credential Provider

Provider Name: `{provider_name}`
Error: {str(get_error)}

Possible Causes:
- Provider doesn't exist
- Insufficient permissions

Check Available: `manage_credentials(action="list")`"""

            # Action: update - Update credential provider
            elif action == 'update':
                if not provider_name:
                    return 'X Error: provider_name is required for update action'
                if not api_key:
                    return 'X Error: api_key is required for update action'

                try:
                    # Update the credential provider
                    update_config = {'name': provider_name, 'apiKey': api_key}

                    if description:
                        update_config['description'] = description

                    result = identity_client.update_credential_provider(
                        provider_name, update_config
                    )
                    # print(result)

                    return f"""# OK Credential Provider Updated

## Updated Provider:
- Name: `{provider_name}`
- Status: Successfully updated
- Region: `{region}`
- Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}
- result: {result}
{f'- Description: {description}' if description else ''}

## ! Important Notes:
- New API key is now active
- Old API key is permanently invalidated
- Agents using this provider will automatically use the new key

## Next Steps:
1. Test agents: Ensure they work with the new API key
2. Verify access: Check that API calls succeed
3. Monitor usage: Watch for any authentication errors

Secure: Security: Old API key is securely deleted and new key is encrypted."""

                except Exception as update_error:
                    return f"""X Failed to Update Credential Provider

Provider Name: `{provider_name}`
Error: {str(update_error)}

Possible Causes:
- Provider doesn't exist
- Invalid API key format
- Insufficient permissions

Check Status: `manage_credentials(action="get", provider_name="{provider_name}")`"""

            else:
                return f"""X Unknown Action: {action}

## Available Actions:
- create: Create new credential provider
- list: List all providers
- delete: Delete a provider
- get: Get provider details
- update: Update provider API key

## Example:
```python
manage_credentials(action="create", provider_name="my-key", api_key="secret") # pragma: allowlist secret
```"""

        except ImportError as e:
            return f"""X Required Dependencies Missing

Error: {str(e)}

To use credential provider functionality:
1. Install AgentCore: `uv add bedrock-agentcore bedrock-agentcore-starter-toolkit`
2. Configure AWS: `aws configure`

Alternative: Use AWS Console for credential management"""

        except Exception as e:
            return f"""X Credential Management Error: {str(e)}

Action: {action}
Provider: {provider_name or 'Not specified'}
Region: {region}

Troubleshooting:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify AgentCore permissions
3. Check provider exists: `manage_credentials(action="list")`"""
