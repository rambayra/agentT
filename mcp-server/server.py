import os
import subprocess
import mcp.types as types
from mcp.server.fastmcp import FastMCP
# Initialize FastMCP server
mcp = FastMCP("terraform-server")
WORKSPACE_DIR = os.path.abspath("terraform_workspace")
# Ensure workspace exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)
def run_terraform_command(command, args=None):
    """Helper to run terraform commands."""
    cmd = ["terraform", command]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(
            cmd,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            check=False # Don't raise on error, return output
        )
        return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nExit Code: {result.returncode}"
    except Exception as e:
        return f"Error running terraform {command}: {str(e)}"
@mcp.tool()
def terraform_init() -> str:
    """Initialize the terraform workspace."""
    return run_terraform_command("init")
@mcp.tool()
def terraform_plan() -> str:
    """Run terraform plan."""
    return run_terraform_command("plan", ["-no-color"])
@mcp.tool()
def terraform_apply() -> str:
    """Run terraform apply (auto-approve)."""
    return run_terraform_command("apply", ["-auto-approve", "-no-color"])
@mcp.tool()
def terraform_show() -> str:
    """Run terraform show to inspect state."""
    return run_terraform_command("show", ["-no-color"])
@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """Write content to a file in the workspace."""
    try:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        # Security check: prevent writing outside workspace
        if not os.path.abspath(filepath).startswith(WORKSPACE_DIR):
             return "Error: Cannot write outside workspace directory."
        
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing file: {str(e)}"
@mcp.tool()
def read_file(filename: str) -> str:
    """Read content from a file in the workspace."""
    try:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        if not os.path.abspath(filepath).startswith(WORKSPACE_DIR):
             return "Error: Cannot read outside workspace directory."
        
        if not os.path.exists(filepath):
            return f"Error: File {filename} not found."
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
@mcp.tool()
def list_files() -> str:
    """List files in the workspace."""
    try:
        files = os.listdir(WORKSPACE_DIR)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"
if __name__ == "__main__":
    mcp.run()