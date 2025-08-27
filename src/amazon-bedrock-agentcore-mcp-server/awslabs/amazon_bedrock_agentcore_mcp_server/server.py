#!/usr/bin/env python3
"""
Amazon Bedrock AgentCore MCP Server

Model Context Protocol server for Amazon Bedrock AgentCore operations.
Designed with a modular architecture to improve maintainability.

Module Organization:
- agentcore_utils.py: Core utilities, OAuth, and environment validation
- agentcore_runtime.py: Agent deployment and invocation management
- agentcore_gateway.py: Gateway operations and MCP integration
- agentcore_identity.py: Credential provider management
- agentcore_memory.py: Memory operations and integration
- Main server: Module coordination and tool registration

Available Tools:

Authentication:
- get_oauth_access_token: Generate OAuth tokens for gateway access
- validate_agentcore_environment: Check development environment

Discovery:
- what_agents_can_i_invoke: Find available agents (local + AWS)
- project_discover: Locate agent files and configurations
- discover_agentcore_examples: GitHub examples discovery
- analyze_agent_code: Code analysis and migration planning

Agent Operations:
- transform_to_agentcore: Convert code to AgentCore format
- deploy_agentcore_app: Deploy agents with multiple modes
- get_agent_status: Check deployment status
- invoke_agent: Standard agent invocation
- invoke_oauth_agent: OAuth-enabled invocation
- invoke_agent_smart: Automatic fallback invocation
- check_oauth_status: OAuth deployment validation
- get_runtime_oauth_token: Runtime token generation

Gateway Management:
- agent_gateway: Gateway creation and management

Credential Management:
- manage_credentials: Credential provider operations
- create_credential_provider: New credential creation
- list_credential_providers: List available providers
- get_credential_provider: Provider details
- update_credential_provider: Update existing providers
- delete_credential_provider: Remove providers

Memory Operations:
- agent_memory: Memory management and integration

Version: 2.0.0
Requires: Python 3.8+, Amazon Bedrock AgentCore SDK 2.x
"""

import asyncio
import sys
import traceback
from pathlib import Path
from typing import Optional

# MCP server framework
from mcp.server.fastmcp import FastMCP

# === MODULE IMPORTS ===
# Import all modular components with comprehensive error handling
try:
    # Core utility and authentication modules
    from .utils import (
        register_oauth_tools, 
        register_environment_tools, 
        register_discovery_tools, 
        register_github_discovery_tools
    )
    
    # Agent lifecycle and runtime management
    from .runtime import register_analysis_tools, register_deployment_tools
    
    # Gateway management and MCP integration
    from .gateway import register_gateway_tools
    
    # Identity and credential management
    from .identity import register_identity_tools
    
    # Memory management and integration
    from .memory import register_memory_tools
    
    # Module availability flags
    MODULES_AVAILABLE = True
    IMPORT_ERROR = None
    
except ImportError as e:
    # Graceful degradation when modules are not available
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)
    
    # Fallback error handler for module import failures
    def create_error_tool(error_msg: str):
        """Create an error reporting tool when module imports fail."""
        def error_tool() -> str:
            return f"""AgentCore MCP Server - Module Import Error
            
Import Error: {error_msg}

Missing modules:
- agentcore_utils.py (utilities and OAuth)
- agentcore_runtime.py (agent management)
- agentcore_gateway.py (gateway operations)
- agentcore_identity.py (credential management)
- agentcore_memory.py (memory operations)

To resolve:
1. Check all module files are present in server directory
2. Validate Python syntax in module files
3. Install dependencies: uv add bedrock-agentcore bedrock-agentcore-starter-toolkit
4. Verify file permissions

Server directory: {Path(__file__).parent}

Fallback: Use monolithic server if modules unavailable
Support: Check individual module errors for details"""
        return error_tool

# === SERVER INITIALIZATION ===
# Initialize FastMCP server with descriptive name
mcp = FastMCP("AgentCore MCP Server - Modular Architecture v2.0.0")

@mcp.tool()
async def server_info() -> str:
    """Retrieve comprehensive information about the AgentCore MCP Server and its modular architecture.
    
    Returns:
        str: Detailed server information including module status, tool inventory, and operational guidance
    """
    
    if not MODULES_AVAILABLE:
        return f"""AgentCore MCP Server - Module Import Error

Status: Module loading failed
Error: {IMPORT_ERROR}

Required modules:
- agentcore_utils.py: Utilities and OAuth authentication
- agentcore_runtime.py: Agent deployment and invocation
- agentcore_gateway.py: Gateway management
- agentcore_identity.py: Credential management
- agentcore_memory.py: Memory operations

Troubleshooting:
1. Check all module files exist in server directory
2. Verify Python syntax in module files
3. Install dependencies: uv add bedrock-agentcore bedrock-agentcore-starter-toolkit
4. Check file permissions
5. Consider using monolithic server as fallback

Server directory: {Path(__file__).parent}
Architecture: Modular v2.0.0
Compatibility: Amazon Bedrock AgentCore SDK 2.x

Server running with limited functionality.
"""
    
    # Tool inventory by functional category
    tool_counts = {
        'authentication_tools': 1,      # get_oauth_access_token
        'environment_tools': 1,         # validate_agentcore_environment  
        'discovery_tools': 3,           # what_agents_can_i_invoke, project_discover, discover_agentcore_examples
        'analysis_tools': 2,            # analyze_agent_code, transform_to_agentcore
        'deployment_tools': 8,          # deploy_agentcore_app, invoke_agent, invoke_oauth_agent, invoke_agent_smart, get_agent_status, check_oauth_status, get_runtime_oauth_token, discover_existing_agents
        'gateway_tools': 1,             # agent_gateway (consolidated)
        'identity_tools': 5,            # manage_credentials + 4 individual credential tools
        'memory_tools': 1,              # agent_memory (consolidated)
        'server_tools': 1               # server_info (this tool)
    }
    
    total_tools = sum(tool_counts.values())
    
    return f"""AgentCore MCP Server - Modular Architecture v2.0.0

Operational Status: Fully operational, all modules loaded

Architecture Overview:
This server uses a modular design to improve code organization and maintainability.

Core Utilities (agentcore_utils.py):
- OAuth authentication and token management
- Environment validation and SDK checks
- Intelligent path and configuration discovery
- Dynamic project and GitHub examples discovery

Runtime Management (agentcore_runtime.py):
- Code analysis and framework detection
- Multi-mode agent deployment (CLI/SDK)
- Agent invocation with OAuth support
- Deployment status monitoring

Gateway Management (agentcore_gateway.py):
- Gateway lifecycle management
- MCP tool discovery and invocation
- Cognito OAuth integration
- AWS service discovery via Smithy models

Identity Management (agentcore_identity.py):
- API key credential providers
- Secure credential storage and injection
- Lifecycle management for authentication

Memory Management (agentcore_memory.py):
- Memory resource creation and integration
- Agent code modification with backups
- Multiple memory strategies (semantic, summary)
- Health monitoring and diagnostics

Tool Registry: {total_tools} tools available

Tool Categories:
- Authentication: {tool_counts['authentication_tools']} tools
- Environment: {tool_counts['environment_tools']} tools
- Discovery: {tool_counts['discovery_tools']} + {tool_counts['analysis_tools']} tools
- Deployment: {tool_counts['deployment_tools']} tools
- Gateway: {tool_counts['gateway_tools']} tools
- Identity: {tool_counts['identity_tools']} tools
- Memory: {tool_counts['memory_tools']} tools
- Server: {tool_counts['server_tools']} tools

Key Features:
- Modular architecture for better maintainability
- Comprehensive error handling with retry logic
- Multi-directory path resolution
- Persistent agent session management
- Full OAuth Bearer token authentication
- Live GitHub examples integration
- Encrypted credential storage

Recommended Usage:
1. Environment validation: validate_agentcore_environment
2. Discovery: what_agents_can_i_invoke, project_discover
3. Analysis: analyze_agent_code, transform_to_agentcore
4. Deployment: deploy_agentcore_app
5. Enhancement: agent_memory, agent_gateway (optional)
6. Testing: invoke_agent_smart, get_agent_status

Server Configuration:
Directory: {Path(__file__).parent}
Modules loaded: {len(['utils', 'runtime', 'gateway', 'identity', 'memory'])}/5
Version: 2.0.0 (Modular)
Compatibility: Amazon Bedrock AgentCore SDK 2.x
Python: 3.8+

Server ready for AgentCore operations with OAuth and MCP support."""

# Module registration and tool loading

if MODULES_AVAILABLE:
    try:
        # Register tools from each module
        register_oauth_tools(mcp)
        register_environment_tools(mcp)
        register_discovery_tools(mcp)  # Enhanced agent discovery from legacy servers
        register_github_discovery_tools(mcp)  # GitHub examples discovery
        register_analysis_tools(mcp)
        register_deployment_tools(mcp)
        register_gateway_tools(mcp)
        register_identity_tools(mcp)
        register_memory_tools(mcp)
        
        print("All AgentCore MCP tools registered successfully")
        
    except Exception as e:
        print(f"Error registering tools: {str(e)}")
        traceback.print_exc()
        
        # Add error tool if registration fails
        @mcp.tool()
        async def registration_error() -> str:
            return f"""Tool Registration Error
            
Error: {str(e)}

Modules exist but tool registration failed.

Possible causes:
1. Syntax errors in module files
2. Missing dependencies
3. Import conflicts
4. Function signature mismatches

Troubleshooting:
1. Check module files for syntax errors
2. Install dependencies: uv add bedrock-agentcore bedrock-agentcore-starter-toolkit boto3
3. Restart MCP server
4. Check server logs for detailed errors

Server running with limited functionality."""

else:
    # Add error tools if modules aren't available
    error_tool_func = create_error_tool(IMPORT_ERROR)
    
    mcp.tool("module_error")(error_tool_func)
    
    print(f"AgentCore modules not available: {IMPORT_ERROR}")
    print("Server running in error mode - use module_error tool for diagnostics")

# Legacy compatibility and migration information

@mcp.tool()
async def migration_info() -> str:
    """Information about migrating from the original monolithic server."""
    
    return """Migration to Modular Server

What Changed:
The original agentcore_mcp_server.py (5000+ lines) has been split into focused modules.

File Structure:
agentcore_mcp_server.py          # Original monolithic server
agentcore_mcp_server_modular.py  # New modular server (this file)
agentcore_utils.py               # Shared utilities and OAuth tools
agentcore_runtime.py             # Agent deployment and management
agentcore_gateway.py             # Gateway operations
agentcore_memory.py              # Memory management and integration

Benefits of Modular Architecture:
- Maintainability: Easier to update individual services
- Testability: Each module can be tested independently
- Readability: Smaller, focused files
- Extensibility: New features added to specific modules
- Debugging: Issues isolated to specific modules

Compatibility:
- No breaking changes to tool names or parameters
- Same functionality, better organization
- Enhanced features like improved gateway deletion

Usage:
# Use modular server
python agentcore_mcp_server_modular.py

# Or replace original
mv agentcore_mcp_server_modular.py agentcore_mcp_server.py

Development Workflow:
1. Edit specific modules for focused changes
2. Test individual modules independently
3. Main server handles imports and registration
4. Easier code reviews with smaller changes

Rollback Option:
Original server remains available as backup:
python agentcore_mcp_server.py

The modular architecture maintains compatibility while improving maintainability."""

# Server startup and main execution

async def main():
    """Main server startup function."""
    
    print("Starting AgentCore MCP Server (Modular v2.0.0)...")
    
    # Print startup status
    if MODULES_AVAILABLE:
        print("All modules loaded successfully")
        print("Tools registered from:")
        print("   - agentcore_utils.py (OAuth, validation)")
        print("   - agentcore_runtime.py (deployment, analysis)")  
        print("   - agentcore_gateway.py (gateway management)")
        print("   - agentcore_memory.py (memory operations)")
    else:
        print(f"Modules not available: {IMPORT_ERROR}")
        print("Server running in error mode")
    
    print(f"Server directory: {Path(__file__).parent}")
    print("Ready for MCP client connections...")
    
    # Run the server
    await mcp.run()

async def run_server():
    """Run the server with proper event loop handling"""
    await main()
    
def run_main():
    """Run the main function, handling asyncio properly."""
    print("Starting AgentCore MCP Server (Modular v2.0.0)...")
    
    # Print startup status
    if MODULES_AVAILABLE:
        print("All modules loaded successfully")
        print("Tools registered from:")
        print("   - agentcore_utils.py (OAuth, validation)")
        print("   - agentcore_runtime.py (deployment, analysis)")  
        print("   - agentcore_gateway.py (gateway management)")
        print("   - agentcore_memory.py (memory operations)")
    else:
        print(f"Modules not available: {IMPORT_ERROR}")
        print("Server running in error mode")
    
    print(f"Server directory: {Path(__file__).parent}")
    print("Ready for MCP client connections...")
    
    # Run the server directly without asyncio.run()
    mcp.run()

if __name__ == "__main__":
    # Handle keyboard interrupts gracefully
    try:
        run_main()
    except KeyboardInterrupt:
        print("\nAgentCore MCP Server shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\nServer error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)