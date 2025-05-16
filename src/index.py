"""
Enterprise MCP Server - Main Entry Point

This module serves as the main entry point for the MCP server.
It initializes all services and starts the Flask application.
"""
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import and run the server
from src.server.app import app, initialize_services

# Initialize application
def init_app():
    # Initialize services
    initialize_services()
    return app

# Application instance for WSGI servers
app = init_app()

if __name__ == "__main__":
    # Start the server
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Enterprise MCP Server on port {port}")
    logger.info("Press Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=port, debug=True)