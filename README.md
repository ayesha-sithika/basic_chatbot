# LangGraph Conversational Chatbot

A simple end-to-end conversational chatbot built with LangGraph, using OpenRouter API with Gemini 2.5 Pro model. Features both a FastAPI backend with REST endpoints and a beautiful web interface.

## Features

- FastAPI REST API backend with comprehensive endpoints
- Beautiful, responsive web chat interface
- Built with LangGraph for workflow management
- Uses OpenRouter API to access Gemini 2.5 Pro
- Maintains conversation history throughout the session
- CLI version also available
- Real-time chat experience with loading indicators

## Project Structure

```
chatbot1/
├── app.py              # FastAPI backend application
├── models.py           # Pydantic models for API
├── chatbot.py          # CLI version of chatbot
├── requirements.txt    # Python dependencies
├── static/
│   └── index.html      # Web frontend
├── .env.example        # Example environment variables
├── .env                # Your actual API key (create this)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key

## Setup Instructions

### 1. Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

#### Option A: Web Interface (Recommended)

Start the FastAPI server:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

#### Option B: CLI Version

```bash
python chatbot.py
```

## API Endpoints

The FastAPI backend provides the following endpoints:

### 1. Health Check
```
GET /health
```
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "message": "Chatbot API is running"
}
```

### 2. Chat
```
POST /chat
```
Send a message and get a response from the chatbot.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**
```json
{
  "response": "I'm doing great, thank you for asking!",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    },
    {
      "role": "user",
      "content": "Hello, how are you?"
    },
    {
      "role": "assistant",
      "content": "I'm doing great, thank you for asking!"
    }
  ]
}
```

### 3. Clear Conversation
```
GET /clear
```
Clear the conversation history.

**Response:**
```json
{
  "message": "Conversation cleared",
  "status": "success"
}
```

### 4. Web Interface
```
GET /
```
Serves the web chat interface.

## Usage

### Web Interface

1. Open your browser to `http://localhost:8000`
2. Type your message in the input box
3. Click "Send" or press Enter
4. The chatbot will respond in real-time
5. Use "Clear" button to start a new conversation

### CLI Interface

Once the CLI chatbot is running:

1. Type your message and press Enter
2. The chatbot will respond using Gemini 2.5 Pro
3. Continue the conversation naturally
4. Type `quit`, `exit`, or `q` to end the conversation

## API Documentation

When the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## Example Usage with cURL

```bash
# Health check
curl http://localhost:8000/health

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is LangGraph?",
    "conversation_history": []
  }
```

## Example Usage with Python

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Hello!",
        "conversation_history": []
    }
)

data = response.json()
print(f"Assistant: {data['response']}")
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file exists and contains `OPENROUTER_API_KEY`
- Verify your API key is valid at https://openrouter.ai/

### Port Already in Use
If port 8000 is already in use, you can change it:
```bash
uvicorn app:app --reload --port 8001