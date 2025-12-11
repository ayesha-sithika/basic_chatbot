# LangGraph Conversational Chatbot

A simple end-to-end conversational chatbot built with LangGraph, using OpenRouter API with Gemini 2.5 Pro model. Features a FastAPI backend with REST endpoints.

## Features

- FastAPI REST API backend with comprehensive endpoints
- Built with LangGraph for workflow management
- Uses OpenRouter API to access Gemini 2.5 Pro
- Maintains conversation history throughout the session
- Real-time chat experience with loading indicators

## Project Structure

```
basic_chatbot/
├── app.py              # FastAPI backend application
├── models.py           # Pydantic models for API
├── requirements.txt    # Python dependencies
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

Edit the `.env` file and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

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
http://localhost:8000/docs
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
  "message": "string",
  "conversation_history": [
    {
      "role": "string",
      "content": "string"
    }
  ]
}
```

**Response:**
```json
{
  "user": "hi",
  "assistant": "Hello, how can I help you?"
}
```
### 3. Conversation history
```
GET /history
```
Get the conversation history.

**Response:**
```json
{
  "history": [
    {
      "user": "hi",
      "assistant": "Hello, how can I help you?"
    }
  ]
}
```

### 4. Clear Conversation
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