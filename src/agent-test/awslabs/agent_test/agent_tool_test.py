"""Tools for testing agent tool usage with DeepEval."""

import asyncio
from awslabs.agent_test.agent_test_harness import AgentTestHarness
from deepeval.metrics.tool_correctness.tool_correctness import ToolCorrectnessMetric
from deepeval.test_case.llm_test_case import LLMTestCase, ToolCall
from langchain_core.messages import AIMessage, ToolMessage
from loguru import logger
from typing import Any, Dict, List, Optional


class AgentToolTest:
    """Test class for evaluating agent tool usage."""

    def __init__(
        self,
        mcp_args: List[str],
        mcp_env: Optional[Dict[str, str]],
        model_id: str = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        region_name: str = 'us-west-2',
    ):
        """Initialize the AgentToolTest.

        Args:
            mcp_args: MCP server arguments
            mcp_env: MCP environment variables
            model_id: Bedrock model ID to use
            region_name: AWS region name
        """
        self.mcp_args = mcp_args
        self.mcp_env = mcp_env
        self.model_id = model_id
        self.region_name = region_name
        self._harness = None

    async def __aenter__(self):
        """Enter context manager."""
        self._harness = AgentTestHarness(
            mcp_args=self.mcp_args,
            mcp_env=self.mcp_env,
            model_id=self.model_id,
            region_name=self.region_name,
        )
        await self._harness.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and clean up resources."""
        if self._harness is not None:
            await self._harness.__aexit__(exc_type, exc_val, exc_tb)
            self._harness = None

    async def create_test_case(
        self, prompt: str, expected_tools: List[str], actual_output: Optional[str] = None
    ) -> LLMTestCase:
        """Create a DeepEval test case by running the agent and capturing tool usage.

        Args:
            prompt: The input prompt to send to the agent
            expected_tools: List of expected tool names that should be called
            actual_output: Optional expected output text

        Returns:
            A LLMTestCase with populated tools_called based on actual agent execution
        """
        if self._harness is None:
            raise RuntimeError('AgentToolTest must be used as a context manager')

        # Get agent from the harness
        agent = await self._harness.get_agent()

        # Invoke the agent with the prompt
        response = await agent.ainvoke({'messages': [{'role': 'user', 'content': prompt}]})

        logger.info(f'Response: {response}')

        # Extract actual tools called from response messages
        tools_called = []
        for message in response['messages']:
            # Check for assistant messages with tool calls
            if isinstance(message, AIMessage) and hasattr(message, 'tool_calls'):
                for tool_call in message.tool_calls:
                    tools_called.append(tool_call['name'])

            # Also check for direct ToolMessage instances
            elif isinstance(message, ToolMessage):
                # Extract the tool name from ToolMessage
                if hasattr(message, 'name'):
                    tools_called.append(message.name)

            # Handle any direct dictionary format (for backward compatibility)
            elif (
                isinstance(message, dict)
                and message.get('role') == 'assistant'
                and 'tool_calls' in message
            ):
                for tool_call in message.get('tool_calls', []):
                    tools_called.append(tool_call['name'])

        # Use the last message as the actual output if not provided
        if actual_output is None and response['messages']:
            last_message = response['messages'][-1]
            if hasattr(last_message, 'content'):
                actual_output = last_message.content
            elif isinstance(last_message, dict):
                actual_output = last_message.get('content', '')
            else:
                actual_output = ''

        # Make sure actual_output is a string for DeepEval
        if actual_output is None:
            actual_output = ''

        # Create the DeepEval test case with required parameters
        return LLMTestCase(
            input=prompt,
            actual_output=actual_output,
            tools_called=[ToolCall(name=tool, input_parameters={}) for tool in tools_called],
            expected_tools=[ToolCall(name=tool, input_parameters={}) for tool in expected_tools],
        )

    def run_test(self, prompt: str, expected_tools: List[str], **kwargs) -> Dict[str, Any]:
        """Synchronous wrapper to run a test and return metrics."""

        async def _run_test():
            async with self:
                test_case = await self.create_test_case(prompt, expected_tools, **kwargs)
                metric = ToolCorrectnessMetric()
                metric.measure(test_case)
                return {'score': metric.score, 'reason': metric.reason, 'test_case': test_case}

        return asyncio.run(_run_test())
