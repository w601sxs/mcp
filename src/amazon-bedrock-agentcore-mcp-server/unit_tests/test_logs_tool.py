#!/usr/bin/env python3
"""
Test: get_agent_logs tool with strandsv3 example
"""

import sys
import asyncio
from pathlib import Path

# Add our MCP server to the path
sys.path.insert(0, str(Path(__file__).parent / "awslabs" / "amazon_bedrock_agentcore_mcp_server"))

async def test_get_agent_logs():
    """Test the get_agent_logs tool with strandsv3 agent."""
    
    print("Testing get_agent_logs tool")
    print("=" * 40)
    
    try:
        from server import create_server
        server = create_server()
        
        # Test 1: Get all logs for strandsv3
        print("Test 1: Getting all logs for strandsv3...")
        result = await server.call_tool('get_agent_logs', {
            'agent_name': 'strandsv3',
            'hours_back': 2,
            'max_events': 20,
            'error_only': False
        })
        
        print("Result:")
        print(result[0][0].text)
        print("\n" + "="*60 + "\n")
        
        # Test 2: Get only error logs
        print("Test 2: Getting error logs only...")
        result = await server.call_tool('get_agent_logs', {
            'agent_name': 'strandsv3',
            'hours_back': 24,
            'max_events': 10,
            'error_only': True
        })
        
        print("Result:")
        print(result[0][0].text)
        
        return True
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

async def main():
    """Run the logs tool test."""
    success = await test_get_agent_logs()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)