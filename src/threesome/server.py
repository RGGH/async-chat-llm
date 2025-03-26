import asyncio
import websockets
import openai
import os

HOST = "0.0.0.0"
PORT = 12345

# Load OPENAI_API_KEY from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    print("Error: OPENAI_API_KEY is not set in environment variables.")
    exit(1)

# Initialize the OpenAI client
client = openai.Client(api_key=OPENAI_API_KEY)

# Global set to track connected clients and a lock for thread safety
clients = set()
clients_lock = asyncio.Lock()

async def handle_client(websocket, path):
    async with clients_lock:
        clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            if message.lower().startswith("@llm"):
                # Broadcast the user's question to all clients
                await broadcast(f"Question: {message}")
                
                # Query LLM for the response
                llm_response = await query_llm(message[4:].strip())
                
                # Broadcast the LLM response to all clients
                await broadcast(f"LLM: {llm_response}")
            else:
                # Broadcast regular messages to all clients
                await broadcast(f"Message: {message}")
    except Exception as e:
        print(f"Error handling message: {e}")
    finally:
        async with clients_lock:
            clients.remove(websocket)

async def broadcast(message):
    async with clients_lock:
        # Send message to all connected clients
        for client in list(clients):
            try:
                await client.send(message)
            except:
                # If the client fails, remove it from the set
                clients.remove(client)

async def query_llm(prompt):
    print(f"Querying LLM with prompt: {prompt}")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI in a chat."},
                {"role": "user", "content": prompt}
            ]
        )
        llm_response = response.choices[0].message.content
        return llm_response
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    # Start the WebSocket server
    server = await websockets.serve(handle_client, HOST, PORT, ping_interval=None)
    print(f"Server started on ws://{HOST}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

