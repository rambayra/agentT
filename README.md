# agentT

TerraAgent 🌍🤖
An Autonomous Infrastructure Agent powered by MCP and Google Gemini.

TerraAgent is an AI-powered DevOps assistant that helps you manage infrastructure using Terraform through natural language. Built for the Kaggle Agents Intensive Capstone, it leverages the Model Context Protocol (MCP) to safely and intelligently interact with your cloud resources.

🚀 Features
Natural Language Infrastructure: Describe what you want (e.g., "Create an S3 bucket"), and TerraAgent writes the Terraform code.
Autonomous Execution: Handles terraform init, 
plan
, and 
apply
 workflows automatically.
Drift Detection & Healing: Proactively checks if your live infrastructure matches your configuration and offers to fix discrepancies.
MCP-Powered: Uses a custom Model Context Protocol server to bridge the gap between the LLM and the Terraform CLI.
🛠️ Architecture
The project consists of two main components:

Agent (agent/): A Python application using Google Gemini 2.0 Flash to reason about tasks and control the workflow.
MCP Server (mcp_server/): A dedicated server that exposes Terraform capabilities (init, plan, apply, file management) as standardized tools.
📋 Prerequisites
Python 3.10+
Terraform installed and available in your system PATH.
A Google Gemini API Key (Get one at aistudio.google.com).
⚡ Quick Start
Clone the repository:


Set up the environment:

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
Configure API Key: Copy the example environment file and add your key:

cp .env.example .env
# Open .env and paste your GOOGLE_API_KEY
Run the Agent:

python -m agent.main
🎮 Usage Example
Once the agent is running, you can interact with it in the terminal:

You: Create a file named main.tf that defines a local text file resource.
Agent: I will create a main.tf file with a local_file resource.
[Agent calls tool: write_file]
...
You: Apply the changes.
Agent: Running terraform init and apply...
[Agent calls tool: terraform_init]
[Agent calls tool: terraform_apply]
...
📂 Project Structure
.
├── agent/              # Agent logic and LLM integration
│   ├── main.py         # Main entry point
│   └── llm.py          # Gemini wrapper
├── mcp_server/         # Custom MCP Server
│   └── server.py       # Terraform tool definitions
├── terraform_workspace/# Directory where TF files are generated
├── requirements.txt    # Python dependencies
└── README.md           # This file
