import asyncio
import sys
import json
import logging
from mcp import StdioServer, StdioServerParameters
from mcp.server import Server

# Logging setup for better debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to handle incoming messages from the client
async def handle_message(message):
    logger.debug(f"Received message: {message}")
    response = {"response": "Hello from MCP server"}
    return json.dumps(response)

# Main async function to set up and run the server
async def main():
    # Create server parameters, including the command to launch the server
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp-server.py"],  # Ensure this is the correct script
        env=None  # Optional: define environment variables if needed
    )
    
    # Create the server instance
    server = StdioServer(server_params)
    
    # Ensure the server stays running and listens for incoming requests
    await server.start()

    # Set the message handler
    server.set_message_handler(handle_message)
    
    # Run the server indefinitely (keep the server alive)
    logger.info("Server is running and listening for connections...")
    await server.run_forever()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

