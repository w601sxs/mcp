#!/bin/bash
# Simple script to test agent-test implementation

# Install dependencies using uv
echo "Installing dependencies..."
cd "$(dirname "$0")"

# Create virtual env with uv if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  uv venv
fi

# Install the package and its dependencies
echo "Installing package dependencies..."
uv sync --all-groups

# Run pytest using uv run
echo "Running tests..."
uv run pytest tests/test_agent_tools.py -v