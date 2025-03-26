import asyncio

HOST = '127.0.0.1'
PORT = 12345

async def send_message(message):
    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    print(f'Sending: {message}')  # Debug: Show the message being sent
    writer.write(message.encode())
    await writer.drain()

    # Read the response
    data = await reader.read(1024)
    print(f"Received: {data.decode()}")  # Debug: Show the response received

    writer.close()
    await writer.wait_closed()

async def main():
    message = input("> ")
    await send_message(message)

if __name__ == "__main__":
    asyncio.run(main())

