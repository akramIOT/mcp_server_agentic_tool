"""
Client API for interacting with the MCP server
"""
import requests
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    """
    Client for interacting with the MCP server
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize the client with the MCP server URL"""
        self.base_url = base_url
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        url = f"{self.base_url}/tools"
        response = requests.get(url)
        return response.json()
    
    def list_services(self) -> List[Dict[str, Any]]:
        """List all available services"""
        url = f"{self.base_url}/services"
        response = requests.get(url)
        return response.json()
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool directly via the /execute endpoint
        
        This method is generic and doesn't specify which service should handle
        the request, relying on the server's tool routing logic
        """
        url = f"{self.base_url}/execute"
        payload = {
            "tool_name": tool_name,
            "parameters": parameters
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def execute_github_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a GitHub tool via the /github/{tool_name} endpoint
        
        This method explicitly specifies the GitHub service should handle
        the request, but the vulnerability may route it elsewhere
        """
        url = f"{self.base_url}/github/{tool_name}"
        response = requests.post(url, json=parameters)
        return response.json()
    
    def execute_linear_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a Linear tool via the /linear/{tool_name} endpoint
        
        This method explicitly specifies the Linear service should handle
        the request, but the vulnerability may route it elsewhere
        """
        url = f"{self.base_url}/linear/{tool_name}"
        response = requests.post(url, json=parameters)
        return response.json()


# Create a singleton instance
client = MCPClient()