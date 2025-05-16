"""
GitHub MCP Service implementation
"""
import os
import logging
from typing import Dict, Any, List

from src.utils.types import MCPService, Tool, ToolSchema, ServiceType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock GitHub data - In a real scenario, this would be fetched from the GitHub API
MOCK_GITHUB_REPOS = [
    {"id": 1, "name": "security-project", "private": False, "description": "A project about security"},
    {"id": 2, "name": "private-repo", "private": True, "description": "Contains sensitive data"},
    {"id": 3, "name": "public-apis", "private": False, "description": "Collection of public APIs"}
]

MOCK_GITHUB_ISSUES = [
    {
        "id": 101,
        "repo_id": 1,
        "title": "Security vulnerability found",
        "body": "Found a critical security issue in the authentication module",
        "labels": ["security", "critical"],
        "state": "open"
    },
    {
        "id": 102,
        "repo_id": 1,
        "title": "Update documentation",
        "body": "Documentation needs to be updated for the new features",
        "labels": ["documentation"],
        "state": "closed"
    },
    {
        "id": 103,
        "repo_id": 2,
        "title": "API Keys exposed",
        "body": "The API keys for production are exposed in the code",
        "labels": ["security", "critical", "confidential"],
        "state": "open"
    },
    {
        "id": 104,
        "repo_id": 3,
        "title": "Add new API endpoints",
        "body": "Need to add endpoints for the new features",
        "labels": ["enhancement"],
        "state": "open"
    }
]

MOCK_GITHUB_USERS = [
    {"id": 201, "username": "admin", "email": "admin@example.com", "role": "admin"},
    {"id": 202, "username": "developer", "email": "dev@example.com", "role": "developer"},
    {"id": 203, "username": "guest", "email": "guest@example.com", "role": "guest"}
]


# GitHub tool implementations
def list_repos(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List GitHub repositories"""
    logger.info("Executing GitHub list_repos tool")
    
    # Filter private repos if specified
    include_private = params.get("include_private", False)
    
    if not include_private:
        return [repo for repo in MOCK_GITHUB_REPOS if not repo["private"]]
    
    return MOCK_GITHUB_REPOS


def list_issues(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List GitHub issues
    
    This function has the same name as the Linear service's list_issues,
    which creates the name conflict vulnerability
    """
    logger.info("Executing GitHub list_issues tool")
    
    repo_id = params.get("repo_id")
    state = params.get("state")
    labels = params.get("labels", [])
    
    # Filter issues
    filtered_issues = MOCK_GITHUB_ISSUES
    
    if repo_id is not None:
        filtered_issues = [issue for issue in filtered_issues if issue["repo_id"] == repo_id]
    
    if state:
        filtered_issues = [issue for issue in filtered_issues if issue["state"] == state]
    
    if labels:
        filtered_issues = [
            issue for issue in filtered_issues 
            if any(label in issue["labels"] for label in labels)
        ]
    
    return filtered_issues


def get_user(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get a GitHub user by ID or username"""
    logger.info("Executing GitHub get_user tool")
    
    user_id = params.get("user_id")
    username = params.get("username")
    
    if user_id is not None:
        for user in MOCK_GITHUB_USERS:
            if user["id"] == user_id:
                return user
    
    if username:
        for user in MOCK_GITHUB_USERS:
            if user["username"] == username:
                return user
    
    return {"error": "User not found"}


def create_issue(params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new GitHub issue"""
    logger.info("Executing GitHub create_issue tool")
    
    repo_id = params.get("repo_id")
    title = params.get("title")
    body = params.get("body", "")
    labels = params.get("labels", [])
    
    if not repo_id or not title:
        return {"error": "repo_id and title are required"}
    
    # Check if repo exists
    repo_exists = any(repo["id"] == repo_id for repo in MOCK_GITHUB_REPOS)
    if not repo_exists:
        return {"error": f"Repository with ID {repo_id} not found"}
    
    # Create a new issue (this is a mock, so we're not actually persisting it)
    new_issue = {
        "id": max(issue["id"] for issue in MOCK_GITHUB_ISSUES) + 1,
        "repo_id": repo_id,
        "title": title,
        "body": body,
        "labels": labels,
        "state": "open"
    }
    
    return new_issue


def initialize_github_service() -> MCPService:
    """Initialize and return the GitHub MCP service"""
    # Create the service
    github_service = MCPService(
        type=ServiceType.GITHUB,
        name="GitHub",
        description="GitHub API service for repository management",
        base_url="https://api.github.com",
        api_key=os.environ.get("GITHUB_API_KEY", "mock_github_api_key")
    )
    
    # Create tools
    
    # List repositories tool
    list_repos_tool = Tool(
        name="list_repos",
        service=ServiceType.GITHUB,
        description="List GitHub repositories",
        parameters=ToolSchema(
            properties={
                "include_private": {
                    "type": "boolean",
                    "description": "Whether to include private repositories"
                }
            },
            required=[]
        )
    )
    list_repos_tool.function = list_repos
    
    # List issues tool - This has a name conflict with Linear's list_issues tool
    list_issues_tool = Tool(
        name="list_issues",
        service=ServiceType.GITHUB,
        description="List GitHub issues",
        parameters=ToolSchema(
            properties={
                "repo_id": {
                    "type": "integer",
                    "description": "Repository ID to filter issues by"
                },
                "state": {
                    "type": "string",
                    "description": "Issue state (open, closed)"
                },
                "labels": {
                    "type": "array",
                    "description": "Labels to filter issues by"
                }
            },
            required=[]
        )
    )
    list_issues_tool.function = list_issues
    
    # Get user tool
    get_user_tool = Tool(
        name="get_user",
        service=ServiceType.GITHUB,
        description="Get a GitHub user by ID or username",
        parameters=ToolSchema(
            properties={
                "user_id": {
                    "type": "integer",
                    "description": "User ID"
                },
                "username": {
                    "type": "string",
                    "description": "Username"
                }
            },
            required=[]
        )
    )
    get_user_tool.function = get_user
    
    # Create issue tool
    create_issue_tool = Tool(
        name="create_issue",
        service=ServiceType.GITHUB,
        description="Create a new GitHub issue",
        parameters=ToolSchema(
            properties={
                "repo_id": {
                    "type": "integer",
                    "description": "Repository ID"
                },
                "title": {
                    "type": "string",
                    "description": "Issue title"
                },
                "body": {
                    "type": "string",
                    "description": "Issue body"
                },
                "labels": {
                    "type": "array",
                    "description": "Issue labels"
                }
            },
            required=["repo_id", "title"]
        )
    )
    create_issue_tool.function = create_issue
    
    # Add tools to the service
    github_service.tools = [
        list_repos_tool,
        list_issues_tool,
        get_user_tool,
        create_issue_tool
    ]
    
    return github_service