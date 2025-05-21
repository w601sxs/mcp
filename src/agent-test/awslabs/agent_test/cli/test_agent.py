#!/usr/bin/env python
"""CLI runner for agent tool tests using DeepEval."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run agent tests with DeepEval."""
    parser = argparse.ArgumentParser(description='Run agent tool tests using DeepEval')
    parser.add_argument('--dataset', '-d', help='Path to test dataset YAML or JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument(
        '--model',
        '-m',
        default='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        help='Model ID to use for testing',
    )
    parser.add_argument('--region', '-r', default='us-west-2', help='AWS region for Bedrock')
    parser.add_argument(
        '--mcp-server', default='awslabs.mcp-server', help='MCP server to use for tests'
    )
    args = parser.parse_args()

    # Set environment variables
    if args.dataset:
        os.environ['AGENT_TEST_DATASET'] = args.dataset
    os.environ['AGENT_TEST_MODEL_ID'] = args.model
    os.environ['AGENT_TEST_REGION'] = args.region
    os.environ['AGENT_TEST_MCP_SERVER'] = args.mcp_server

    # Find the test file
    common_dir = Path(__file__).parent.parent.parent
    test_file = common_dir / 'awslabs' / 'common' / 'tests' / 'test_agent_tools.py'

    # Build command
    cmd = ['deepeval', 'test', 'run', str(test_file)]
    if args.verbose:
        cmd.append('-v')

    # Run the command
    print(f'Running DeepEval tests with model {args.model} in {args.region}')
    if args.dataset:
        print(f'Using test cases from: {args.dataset}')
    print('=' * 50)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
