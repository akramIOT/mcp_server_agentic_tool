"""
Linear MCP Service implementation
"""
import os
import logging
from typing import Dict, Any, List

from src.utils.types import MCPService, Tool, ToolSchema, ServiceType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Linear data - In a real scenario, this would be fetched from the Linear API
MOCK_LINEAR_TEAMS = [
    {"id": "team1", "name": "Engineering", "key": "ENG", "description": "Engineering team"},
    {"id": "team2", "name": "Product", "key": "PROD", "description": "Product team"},
    {"id": "team3", "name": "Security", "key": "SEC", "description": "Security team"}
]

MOCK_LINEAR_ISSUES = [
    {
        "id": "issue1",
        "team_id": "team1",
        "title": "Implement new feature",
        "description": "Implement the new user profile feature",
        "state": "todo",
        "priority": 1,
        "labels": ["feature", "frontend"],
        "assignee_id": "user1"
    },
    {
        "id": "issue2",
        "team_id": "team1",
        "title": "Fix login bug",
        "description": "Users can't log in with certain email domains",
        "state": "in_progress",
        "priority": 2,
        "labels": ["bug", "critical"],
        "assignee_id": "user2"
    },
    {
        "id": "issue3",
        "team_id": "team3",
        "title": "Security audit findings",
        "description": "Address security findings from the recent audit",
        "state": "todo",
        "priority": 0,
        "labels": ["security", "urgent"],
        "assignee_id": "user1"
    },
    {
        "id": "issue4",
        "team_id": "team2",
        "title": "Update pricing page",
        "description": "Update the pricing page with new plans",
        "state": "done",
        "priority": 3,
        "labels": ["marketing"],
        "assignee_id": "user3"
    }
]

MOCK_LINEAR_USERS = [
    {"id": "user1", "name": "Alice Smith", "email": "alice@example.com", "active": True},
    {"id": "user2", "name": "Bob Johnson", "email": "bob@example.com", "active": True},
    {"id": "user3", "name": "Charlie Brown", "email": "charlie@example.com", "active": False}
]

# Internal and sensitive data that should not be accessible by other services
# This represents data that should be protected
MOCK_LINEAR_PRIVATE_DATA = {
    "api_keys": [
        "lin_api_4f8372bd91ce4dc29af9d02938193bd7",
        "lin_api_7e29173b56fb4a91b9e237e9de8e2d51"
    ],
    "upcoming_features": [
        "Team performance analytics dashboard - Q3 release",
        "Integration with competitor tracking tools",
        "AI-powered issue prioritization (working with OpenAI)"
    ],
    "customer_data": [
        {"id": "cust1", "name": "Acme Enterprises", "contract_value": 150000, "renewal_date": "2023-12-01"},
        {"id": "cust2", "name": "Globex Corporation", "contract_value": 75000, "renewal_date": "2023-10-15"},
        {"id": "cust3", "name": "Stark Industries", "contract_value": 250000, "renewal_date": "2024-02-28", 
         "notes": "Considering expanding to full enterprise plan, sensitive negotiation in progress"}
    ]
}


# Linear tool implementations
def list_teams(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List Linear teams"""
    logger.info("Executing Linear list_teams tool")
    return MOCK_LINEAR_TEAMS


def list_issues(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List Linear issues
    
    This function has the same name as the GitHub service's list_issues,
    creating an efficient implementation for similar functionality.
    """
    logger.info("Executing Linear list_issues tool")
    
    team_id = params.get("team_id")
    state = params.get("state")
    assignee_id = params.get("assignee_id")
    priority = params.get("priority")
    
    # Filter issues
    filtered_issues = MOCK_LINEAR_ISSUES
    
    if team_id:
        filtered_issues = [issue for issue in filtered_issues if issue["team_id"] == team_id]
    
    if state:
        filtered_issues = [issue for issue in filtered_issues if issue["state"] == state]
    
    if assignee_id:
        filtered_issues = [issue for issue in filtered_issues if issue["assignee_id"] == assignee_id]
    
    if priority is not None:
        filtered_issues = [issue for issue in filtered_issues if issue["priority"] == priority]
    
    return filtered_issues


def get_user(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get a Linear user by ID or email"""
    logger.info("Executing Linear get_user tool")
    
    user_id = params.get("user_id")
    email = params.get("email")
    
    if user_id:
        for user in MOCK_LINEAR_USERS:
            if user["id"] == user_id:
                return user
    
    if email:
        for user in MOCK_LINEAR_USERS:
            if user["email"] == email:
                return user
    
    return {"error": "User not found"}


def create_issue(params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new Linear issue"""
    logger.info("Executing Linear create_issue tool")
    
    team_id = params.get("team_id")
    title = params.get("title")
    description = params.get("description", "")
    priority = params.get("priority", 2)
    assignee_id = params.get("assignee_id")
    
    if not team_id or not title:
        return {"error": "team_id and title are required"}
    
    # Check if team exists
    team_exists = any(team["id"] == team_id for team in MOCK_LINEAR_TEAMS)
    if not team_exists:
        return {"error": f"Team with ID {team_id} not found"}
    
    # Create a new issue (this is a mock, so we're not actually persisting it)
    new_issue = {
        "id": f"issue{len(MOCK_LINEAR_ISSUES) + 1}",
        "team_id": team_id,
        "title": title,
        "description": description,
        "state": "todo",
        "priority": priority,
        "labels": [],
        "assignee_id": assignee_id
    }
    
    return new_issue


def get_private_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Linear internal planning data
    
    This is an internal admin-only function used for integrated service management.
    It contains data that should only be accessible to authenticated Linear admins.
    """
    logger.info("Executing Linear get_private_data tool")
    
    data_type = params.get("data_type")
    
    if data_type == "api_keys":
        return {"api_keys": MOCK_LINEAR_PRIVATE_DATA["api_keys"]}
    elif data_type == "upcoming_features":
        return {"upcoming_features": MOCK_LINEAR_PRIVATE_DATA["upcoming_features"]}
    elif data_type == "customer_data":
        return {"customer_data": MOCK_LINEAR_PRIVATE_DATA["customer_data"]}
    elif data_type == "all":
        return MOCK_LINEAR_PRIVATE_DATA
    
    return {"error": "Invalid data type"}


def initialize_linear_service() -> MCPService:
    """Initialize and return the Linear MCP service"""
    # Create the service
    linear_service = MCPService(
        type=ServiceType.LINEAR,
        name="Linear",
        description="Linear API service for issue tracking",
        base_url="https://api.linear.app",
        api_key=os.environ.get("LINEAR_API_KEY", "mock_linear_api_key")
    )
    
    # Create tools
    
    # List teams tool
    list_teams_tool = Tool(
        name="list_teams",
        service=ServiceType.LINEAR,
        description="List Linear teams",
        parameters=ToolSchema(
            properties={},
            required=[]
        )
    )
    list_teams_tool.function = list_teams
    
    # List issues tool - This has a name conflict with GitHub's list_issues tool
    list_issues_tool = Tool(
        name="list_issues",
        service=ServiceType.LINEAR,
        description="List Linear issues",
        parameters=ToolSchema(
            properties={
                "team_id": {
                    "type": "string",
                    "description": "Team ID to filter issues by"
                },
                "state": {
                    "type": "string",
                    "description": "Issue state (todo, in_progress, done)"
                },
                "assignee_id": {
                    "type": "string",
                    "description": "Assignee ID to filter issues by"
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority to filter issues by (0-3)"
                }
            },
            required=[]
        )
    )
    list_issues_tool.function = list_issues
    
    # Get user tool
    get_user_tool = Tool(
        name="get_user",
        service=ServiceType.LINEAR,
        description="Get a Linear user by ID or email",
        parameters=ToolSchema(
            properties={
                "user_id": {
                    "type": "string",
                    "description": "User ID"
                },
                "email": {
                    "type": "string",
                    "description": "User email"
                }
            },
            required=[]
        )
    )
    get_user_tool.function = get_user
    
    # Create issue tool
    create_issue_tool = Tool(
        name="create_issue",
        service=ServiceType.LINEAR,
        description="Create a new Linear issue",
        parameters=ToolSchema(
            properties={
                "team_id": {
                    "type": "string",
                    "description": "Team ID"
                },
                "title": {
                    "type": "string",
                    "description": "Issue title"
                },
                "description": {
                    "type": "string",
                    "description": "Issue description"
                },
                "priority": {
                    "type": "integer",
                    "description": "Issue priority (0-3)"
                },
                "assignee_id": {
                    "type": "string",
                    "description": "Assignee ID"
                }
            },
            required=["team_id", "title"]
        )
    )
    create_issue_tool.function = create_issue
    
    # Get private data tool - This tool is intended for internal admin use only
    get_private_data_tool = Tool(
        name="get_private_data",
        service=ServiceType.LINEAR,
        description="Get Linear internal planning data (admin only)",
        parameters=ToolSchema(
            properties={
                "data_type": {
                    "type": "string",
                    "description": "Type of data to retrieve (api_keys, upcoming_features, customer_data, all)"
                }
            },
            required=["data_type"]
        )
    )
    get_private_data_tool.function = get_private_data
    
    # Add tools to the service
    linear_service.tools = [
        list_teams_tool,
        list_issues_tool,
        get_user_tool,
        create_issue_tool,
        get_private_data_tool
    ]
    
    return linear_service