# Valid AgentCore app for testing
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
async def main(ctx, request):
    return "Test agent"

if __name__ == "__main__":
    app.run()