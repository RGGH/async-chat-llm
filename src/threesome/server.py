import asyncio
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

# Global list to track connected clients
clients = set()
clients_lock = asyncio.Lock()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    
    async with clients_lock:
        clients.add(writer)
    
    print(f"Client connected: {addr}")
    
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode().strip()
            print(f"Received from {addr}: {message}")
            
            if message.lower().startswith("@llm"):
                # Query LLM for the response
                try:
                    llm_response = await query_llm(message[4:].strip())
                    broadcast_message = f"LLM: {llm_response}"
                    await broadcast(broadcast_message)
                except Exception as e:
                    print(f"LLM query error: {e}")
                    broadcast_message = f"Error processing LLM request: {e}"
                    await broadcast(broadcast_message)
            else:
                # Broadcast regular messages to all clients
                await broadcast(f"{addr}: {message}")
    
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        # Handle client disconnection
        print(f"Client disconnected: {addr}")
        
        async with clients_lock:
            if writer in clients:
                clients.remove(writer)
        
        writer.close()
        await writer.wait_closed()

async def broadcast(message):
    print(f"Broadcasting: {message}")
    
    # Create a copy of clients to safely iterate
    async with clients_lock:
        current_clients = list(clients)
    
    for client_writer in current_clients:
        try:
            # Ensure message is sent to each client
            client_writer.write(message.encode() + b"\n")
            await client_writer.drain()
            print(f"Message sent to {client_writer.get_extra_info('peername')}")
        except Exception as e:
            print(f"Error sending message to a client: {e}")
            
            # Remove problematic client
            async with clients_lock:
                if client_writer in clients:
                    clients.remove(client_writer)

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
        print(f"LLM Response: {llm_response}")
        return llm_response
    
    except Exception as e:
        print(f"LLM query failed: {e}")
        return f"Error: {str(e)}"

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
