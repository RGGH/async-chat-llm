# Async Chat Server with OpenAI LLM Integration

![Screenshot from 2025-03-29 17-13-01](https://github.com/user-attachments/assets/12fdd9cf-93e6-4ac5-8adc-e46211927c98)


## Overview

This project is an asynchronous chat server that supports multiple client connections and integrates OpenAI's language model for intelligent responses. The application uses Python's `asyncio` for non-blocking I/O operations and the OpenAI API to provide AI-powered chat interactions.

## Features

- **Asynchronous Networking**: Handles multiple client connections concurrently
- **Real-time Messaging**: Broadcasts messages to all connected clients
- **AI-Powered Responses**: Integrated OpenAI language model for intelligent chat interactions
- **Error Handling**: Robust error management for network and API interactions

## Prerequisites

- Python 3.8+
- `openai` Python library
- OpenAI API Key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RGGH/async-chat-llm.git
   cd async-chat-llm
   ```

2. Install required dependencies:
   ```bash
   pip install asyncio openai
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key_here'
   ```

## Usage

### Server

Run the server:
```bash
python server.py
```

The server will start and listen on `0.0.0.0:12345`.

### Client

Open the index.html file in your web browser. This will connect to the WebSocket server and allow you to send messages and receive LLM responses directly in the browser.

### Chat Commands

- Send a regular message to broadcast to all clients
- Use `@llm [your prompt]` to trigger an AI-powered response

## Example

```
> Hello everyone!  # Regular message
> @llm Tell me a joke  # AI-powered response
```

## Configuration

- **Host**: Configurable in `server.py` (default: `0.0.0.0`)
- **Port**: Configurable in `server.py` (default: `12345`)
- **LLM Model**: Currently using `gpt-3.5-turbo` (modifiable in `query_llm()`)

## Security Considerations

- Ensure your OpenAI API key is kept secret
- Use environment variables for sensitive credentials
- Implement additional authentication for production use

## Limitations

- Basic error handling
- No persistent message storage
- Single AI model configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/RGGH/async-chat-llm](https://github.com/RGGH/async-chat-llm)
