import asyncio
import websockets
import openai
import os
import json

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

            # Ensure the message is a valid JSON object
            try:
                data = json.loads(message)
                sender = data.get("sender", "Unknown")
                text = data.get("message", "")

                if text.lower().startswith("@llm"):
                    # Broadcast user's question
                    await broadcast({"sender": sender, "message": text})
                    
                    # Query LLM for response
                    llm_response = await query_llm(text[4:].strip())

                    # Broadcast LLM response
                    await broadcast({"sender": "LLM", "message": llm_response})
                else:
                    # Broadcast regular messages
                    await broadcast({"sender": sender, "message": text})
            
            except json.JSONDecodeError:
                print("Error: Received invalid JSON message.")
                continue

    except Exception as e:
        print(f"Error handling message: {e}")
    finally:
        async with clients_lock:
            clients.remove(websocket)

async def broadcast(message):
    async with clients_lock:
        # Convert the message to JSON format
        message_json = json.dumps(message)
        for client in list(clients):
            try:
                await client.send(message_json)
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
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    # Start the WebSocket server
    server = await websockets.serve(handle_client, HOST, PORT, ping_interval=None)
    print(f"Server started on ws://{HOST}:{PORT} ✅")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

