"""
Types and models for the MCP server
"""
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """Service type for identifying MCP services"""
    GITHUB = "github"
    LINEAR = "linear"


class ToolParameter(BaseModel):
    """Model for a tool parameter"""
    type: str
    description: str
    required: bool = True


class ToolSchema(BaseModel):
    """Schema definition for a tool"""
    type: str = "object"
    properties: Dict[str, Any]
    required: List[str] = []


class Tool(BaseModel):
    """Tool definition"""
    name: str
    service: ServiceType
    description: str
    parameters: ToolSchema
    
    # This will be set programmatically and not part of the JSON schema
    function: Optional[Callable] = None


class MCPService(BaseModel):
    """MCP Service definition"""
    type: ServiceType
    name: str
    description: str
    base_url: str
    api_key: Optional[str] = None
    tools: List[Tool] = []


class ToolRequest(BaseModel):
    """Tool request model"""
    tool_name: str
    parameters: Dict[str, Any] = {}


class ToolResponse(BaseModel):
    """Tool response model"""
    status: str = "success"
    service: ServiceType
    data: Optional[Any] = None
    error: Optional[str] = None