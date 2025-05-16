"""
MCP Server Flask application
"""
import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from src.utils.types import ToolRequest, ServiceType
from src.server.mcp_registry import registry
from src.services.github.service import initialize_github_service
from src.services.linear.service import initialize_linear_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize MCP services
def initialize_services():
    """Initialize and register all MCP services"""
    # Initialize GitHub service
    github_service = initialize_github_service()
    registry.register_service(github_service)
    
    # Initialize Linear service
    linear_service = initialize_linear_service()
    registry.register_service(linear_service)
    
    logger.info("All MCP services initialized and registered")


@app.route('/tools', methods=['GET'])
def list_tools():
    """List all available tools"""
    tools = registry.list_tools()
    return jsonify([{
        "name": tool.name,
        "service": tool.service,
        "description": tool.description,
        "parameters": tool.parameters.dict()
    } for tool in tools])


@app.route('/services', methods=['GET'])
def list_services():
    """List all available services"""
    services = registry.list_services()
    return jsonify([{
        "type": service.type,
        "name": service.name,
        "description": service.description,
        "tools": [tool.name for tool in service.tools]
    } for service in services])


@app.route('/execute', methods=['POST'])
def execute_tool():
    """Execute a tool"""
    data = request.json
    
    try:
        # Parse the request
        tool_request = ToolRequest(**data)
        
        # Execute the tool
        response = registry.execute_tool(tool_request)
        
        # Return the response
        return jsonify(response.dict())
    
    except Exception as e:
        logger.error(f"Error executing tool: {str(e)}")
        return jsonify({
            "status": "error",
            "service": ServiceType.GITHUB,  # Default service for error
            "error": f"Error processing request: {str(e)}"
        }), 400


@app.route('/github/<tool_name>', methods=['POST'])
def execute_github_tool(tool_name):
    """
    Execute a GitHub tool directly
    """
    data = request.json or {}
    
    try:
        # Create a tool request
        tool_request = ToolRequest(
            tool_name=tool_name,
            parameters=data
        )
        
        # Execute the tool
        response = registry.execute_tool(tool_request)
        
        # Return the response
        return jsonify(response.dict())
    
    except Exception as e:
        logger.error(f"Error executing GitHub tool: {str(e)}")
        return jsonify({
            "status": "error",
            "service": ServiceType.GITHUB,
            "error": f"Error processing request: {str(e)}"
        }), 400


@app.route('/linear/<tool_name>', methods=['POST'])
def execute_linear_tool(tool_name):
    """
    Execute a Linear tool directly
    """
    data = request.json or {}
    
    try:
        # Create a tool request
        tool_request = ToolRequest(
            tool_name=tool_name,
            parameters=data
        )
        
        # Execute the tool
        response = registry.execute_tool(tool_request)
        
        # Return the response
        return jsonify(response.dict())
    
    except Exception as e:
        logger.error(f"Error executing Linear tool: {str(e)}")
        return jsonify({
            "status": "error",
            "service": ServiceType.LINEAR,
            "error": f"Error processing request: {str(e)}"
        }), 400


if __name__ == '__main__':
    # Initialize services
    initialize_services()
    
    # Start the server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)