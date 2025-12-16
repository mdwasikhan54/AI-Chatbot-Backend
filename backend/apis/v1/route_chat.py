from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.db.models.chat import ChatHistory
from backend.db.models.user import User
from backend.schemas.schemas import ChatRequest, ChatResponse, ChatHistorySchema
from backend.services.rag_service import chat_service
from backend.apis.v1.route_auth import get_current_user

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    Handles user chat: saves message, retrieves AI response via RAG, saves response.
    Requires authentication.
    """
    # 1. Save User Message
    user_msg = ChatHistory(user_id=current_user.id, message=request.message, is_user_message=True)
    db.add(user_msg)
    db.commit()

    # 2. Get AI Response (RAG Pipeline)
    response_text = await chat_service.get_response(request.message)

    # 3. Save AI Response
    ai_msg = ChatHistory(user_id=current_user.id, message=response_text, is_user_message=False)
    db.add(ai_msg)
    db.commit()

    return {"response": response_text}

@router.get("/chat-history", response_model=List[ChatHistorySchema])
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all chat history for the currently logged-in user.
    """
    return db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).all()

# --- New Delete Endpoint ---
@router.delete("/chat-history", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes all chat history for the logged-in user.
    Returns 204 No Content on success.
    """
    db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).delete()
    db.commit()
    return None