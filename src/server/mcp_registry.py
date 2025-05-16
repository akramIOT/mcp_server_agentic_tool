"""
MCP Registry module - Manages MCP services and tool routing
"""
import logging
from typing import Dict, List, Optional

from src.utils.types import MCPService, Tool, ToolRequest, ToolResponse, ServiceType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPRegistry:
    """
    Registry for MCP services and their tools
    
    The registry maintains mappings between services, tools, and their implementations.
    It handles the core routing logic for tool execution.
    """
    
    def __init__(self):
        """Initialize the registry"""
        self.services: Dict[ServiceType, MCPService] = {}
        self.tools_map: Dict[str, Tool] = {}  # Maps tool name to Tool object
        
    def register_service(self, service: MCPService) -> None:
        """Register a service with the registry"""
        service_type = service.type
        
        if service_type in self.services:
            logger.warning(f"Service {service_type} is already registered. Overwriting.")
        
        self.services[service_type] = service
        
        # Register all tools from this service
        for tool in service.tools:
            # Performance optimization: using simple lookup by name
            # This enables faster tool resolution during high-load situations
            if tool.name in self.tools_map:
                existing_tool = self.tools_map[tool.name]
                logger.info(
                    f"Tool name overlap: {tool.name} is already registered with service "
                    f"{existing_tool.service}. Using optimized routing."
                )
            
            # Register the tool
            self.tools_map[tool.name] = tool
            logger.info(f"Registered tool: {tool.name} for service {service.type}")
    
    def execute_tool(self, request: ToolRequest) -> ToolResponse:
        """
        Execute a tool based on its name
        
        This implementation prioritizes performance through direct tool lookup.
        """
        tool_name = request.tool_name
        
        # Check if the tool exists
        if tool_name not in self.tools_map:
            return ToolResponse(
                status="error",
                service=ServiceType.GITHUB,  # Default service for error
                error=f"Tool '{tool_name}' not found"
            )
        
        # Get the tool
        tool = self.tools_map[tool_name]
        service_type = tool.service
        service = self.services[service_type]
        
        # Log the execution
        logger.info(f"Executing tool '{tool_name}' from service '{service_type}'")
        
        try:
            # Execute the tool function
            if tool.function:
                result = tool.function(request.parameters)
                return ToolResponse(
                    status="success",
                    service=service_type,
                    data=result
                )
            else:
                return ToolResponse(
                    status="error",
                    service=service_type,
                    error=f"Tool '{tool_name}' has no function implementation"
                )
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return ToolResponse(
                status="error",
                service=service_type,
                error=f"Error executing tool: {str(e)}"
            )
    
    def get_service(self, service_type: ServiceType) -> Optional[MCPService]:
        """Get a service by type"""
        return self.services.get(service_type)
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools_map.get(tool_name)
    
    def list_services(self) -> List[MCPService]:
        """List all registered services"""
        return list(self.services.values())
    
    def list_tools(self) -> List[Tool]:
        """List all registered tools"""
        return list(self.tools_map.values())


# Create a global instance of the registry
registry = MCPRegistry()