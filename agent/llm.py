import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
class LLMService:
    def __init__(self, system_instruction: str = None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
    def send_message(self, message: str, tools=None):
        # Note: In a real implementation with mcp, we'd bind tools to the model
        # For this simplified version, we'll assume the main loop handles tool execution
        # or we pass tools here if using the SDK's auto-function calling with compatible tools.
        # Since we are bridging MCP tools to Gemini, we might need a custom loop.
        # But for now, let's just return the response.
        
        response = self.chat.send_message(message)
        return response