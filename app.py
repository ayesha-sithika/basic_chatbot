import os
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from models import ChatRequest, ChatResponse, HealthResponse, Message
from typing import TypedDict

# Load environment variables
load_dotenv()

# convo history
conversation_store = []

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Chatbot API",
    description="Conversational chatbot using LangGraph and OpenRouter API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# State definition for the chatbot
class ChatState(TypedDict):
    messages: Annotated[list, "The conversation messages"]


# Initialize the LLM with OpenRouter
def get_llm():
    """Initialize and return the ChatOpenAI instance configured for OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")

    return ChatOpenAI(
        model="google/gemini-2.5-pro",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
    )


# Node function: Call the LLM
def call_model(state: ChatState) -> ChatState:
    """Node that calls the LLM with the current conversation history"""
    llm = get_llm()
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


# Build the graph
def create_chatbot_graph():
    """Creates and returns the LangGraph chatbot workflow"""
    workflow = StateGraph(ChatState)
    workflow.add_node("call_model", call_model)
    workflow.set_entry_point("call_model")
    workflow.add_edge("call_model", END)
    return workflow.compile()


# Create chatbot instance
chatbot = create_chatbot_graph()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Chatbot API is running"
    )


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user messages and returns AI responses

    Args:
        request: ChatRequest containing user message and optional conversation history

    Returns:
        ChatResponse with assistant's response and updated conversation history
    """
    try:
        # Initialize messages with system prompt
        messages = [
            SystemMessage(content="You are a concise AI assistant. Always respond in 1-2 sentences unless the user asks for detailed explanations. Avoid long greetings, avoid unnecessary elaboration, and keep responses short and to the point.")
        ]

        # Add conversation history if provided
        if request.conversation_history:
            for msg in request.conversation_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))

        # Add current user message
        messages.append(HumanMessage(content=request.message))

        # Create state
        state = {"messages": messages}

        # Invoke chatbot
        result = chatbot.invoke(state)

        # Extract AI response
        ai_response = result["messages"][-1].content

        # Build conversation history for response (excluding system message)
        conversation_history = []
        for msg in result["messages"][1:]:  # Skip system message
            if isinstance(msg, HumanMessage):
                conversation_history.append(Message(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                conversation_history.append(Message(role="assistant", content=msg.content))

        # Save conversation turn in memory
        conversation_store.append({
            "user": request.message,
            "assistant": ai_response
        })

        return {
            "user": request.message,
            "assistant": ai_response
        }

    except ValueError as ve:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/history")
async def get_history():
    """Return the in-memory full chat history"""
    return {"history": conversation_store}

@app.get("/clear")
async def clear_conversation():
    """Clear the in-memory conversation history"""
    conversation_store.clear()
    return {"message": "Conversation cleared", "status": "success"}


if __name__ == "__main__":
    import uvicorn
    print("INFO:     http://localhost:8000/docs - Endpoints")
    uvicorn.run(app, host="0.0.0.0", port=8000)


# python app.py
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
# 8000 or 8001
