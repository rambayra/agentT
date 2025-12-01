import asyncio
import os
import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.llm import LLMService
from google.generativeai.types import FunctionDeclaration, Tool
# Add parent directory to path to import mcp_server if needed, 
# but we will run it as a subprocess.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
async def run():
    # Define server parameters
    # We run the server using the same python interpreter
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server/server.py"],
        env=os.environ.copy()
    )
    async with AsyncExitStack() as stack:
        # Connect to MCP server
        read_stream, write_stream = await stack.enter_async_context(stdio_client(server_params))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        
        await session.initialize()
        
        # List tools
        mcp_tools = await session.list_tools()
        print(f"Connected to MCP Server. Found {len(mcp_tools.tools)} tools.")
        # Initialize LLM
        # We need to convert MCP tools to Gemini tools
        # For this simplified version, we will manually map them or just use a system prompt 
        # that describes the tools if automatic mapping is too complex for this snippet.
        # However, Gemini supports function calling. Let's try to map them.
        
        gemini_tools = []
        for tool in mcp_tools.tools:
            # Simplified mapping. In a real app, we'd map types more carefully.
            # Gemini expects a specific format.
            # For now, let's rely on the LLM's ability to understand the tool descriptions
            # and we will handle the execution.
            # We will pass the tool definitions to the LLM configuration.
            pass
        # For this , we'll use a powerful system prompt and manual tool execution loop
        # or rely on the LLM to output JSON for tool calls if we don't fully wire up the SDK's auto-tools.
        # Let's try to wire it up properly in the next iteration if needed.
        # For now, let's start with a basic loop that describes tools in the system prompt.
        
        tools_desc = "\n".join([f"- {t.name}: {t.description}" for t in mcp_tools.tools])
        
        system_prompt = f"""You are an AI Agent for Terraform.
You have access to the following tools via an MCP server:
{tools_desc}
To use a tool, you must respond with a JSON block in this format:
```json
{{
  "tool": "tool_name",
  "arguments": {{ "arg1": "value1" }}
}}
If you want to send a message to the user, just write text. Do not combine JSON tool calls with normal text in the same response if possible. Always check for drift before applying changes if the user asks to "fix" or "update" infrastructure. """

llm = LLMService(system_instruction=system_prompt)
    
    print("Agent is ready. Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        # Send to LLM
        # We append a reminder about the tool format to ensure compliance
        response = llm.send_message(user_input)
        
        # Simple loop to handle tool calls
        # In a real production agent, this would be more robust (handling multiple calls, etc.)
        while True:
            text = response.text
            import json
            import re
            
            # Check for JSON code block
            match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if not match:
                # Try finding raw JSON if no code block
                match = re.search(r'(\{.*"tool":.*\})', text, re.DOTALL)
            
            if match:
                try:
                    tool_call = json.loads(match.group(1))
                    tool_name = tool_call.get("tool")
                    tool_args = tool_call.get("arguments", {})
                    
                    print(f"\n[Agent calling tool: {tool_name} with args: {tool_args}]")
                    
                    # Execute tool via MCP session
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    
                    # Format result
                    tool_output = ""
                    if result.content:
                        for content in result.content:
                            if content.type == "text":
                                tool_output += content.text
                    
                    print(f"[Tool Output]: {tool_output[:200]}...") # Truncate for display
                    
                    # Feed back to LLM
                    response = llm.send_message(f"Tool '{tool_name}' output:\n{tool_output}")
                    
                except Exception as e:
                    print(f"Error executing tool: {e}")
                    response = llm.send_message(f"Error executing tool: {e}")
            else:
                # No tool call, just print response
                print(f"\nAgent: {text}")
                break
if name == "main": asyncio.run(run())