from pydantic import BaseModel, Field
from typing import List, Optional


class Message(BaseModel):
    """Individual message in the conversation"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message", min_length=1)
    conversation_history: Optional[List[Message]] = Field(
        default=None,
        description="Optional conversation history"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Assistant's response")
    conversation_history: List[Message] = Field(
        ...,
        description="Updated conversation history"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
