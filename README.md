# Enterprise MCP Server

A robust Microservice Control Plane (MCP) server implementation for managing tool execution across multiple service integrations.

## Overview

This project provides a complete MCP server implementation for integrating multiple third-party services (GitHub, Linear, etc.) into a unified tool execution platform. The server orchestrates API requests across service boundaries, enabling seamless multi-service workflows through a single interface.

## Features

- **Multi-Service Integration**: Connect to GitHub, Linear, and other services through a unified API
- **Tool Orchestration**: Route tool requests to the appropriate service automatically
- **Flexible Configuration**: Easy service registration and configuration
- **Robust Error Handling**: Consistent error responses across all services

## Architecture

The MCP server follows a modular architecture:

- **MCP Registry**: Core component that manages service and tool registration
- **Service Implementations**: Adapters for each integrated service (GitHub, Linear)
- **Client API**: Interface for executing tools across services

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd mcp_server_agentic_tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your service API keys
   ```

### Running the Server

Start the MCP server:

```bash
python src/index.py
```

The server will start on port 5000 (configurable via PORT environment variable).

## Usage

### API Endpoints

- `GET /services`: List all available services
- `GET /tools`: List all available tools across all services
- `POST /execute`: Execute a tool by name
- `POST /github/{tool_name}`: Execute a GitHub tool
- `POST /linear/{tool_name}`: Execute a Linear tool

### Example Request

Execute a GitHub tool to list issues:

```bash
curl -X POST http://localhost:5000/github/list_issues \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Client Library

The project includes a Python client library for interacting with the MCP server:

```python
from src.client.api import client

# List all tools
tools = client.list_tools()

# Execute a GitHub tool
response = client.execute_github_tool('list_issues', {})
```

## Integration Showcase

The project includes a showcase of how to integrate multiple services through the MCP server:

```bash
python src/client/integration_showcase.py
```

This demonstrates how the MCP server can be used to create seamless workflows across multiple services, enabling unified project management.

## Project Structure

- `src/server`: Core MCP server implementation
- `src/services`: Service-specific implementations
- `src/client`: Client API and demo scripts
- `src/utils`: Shared utilities and type definitions