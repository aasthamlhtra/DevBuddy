from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, models
from ..database import get_db
from ..utils import get_current_user
from app.rag.pipeline.router import build_router

router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="app/templates")

# Instantiate the query classifier & RAG chain router once
rag_router = build_router()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    current_user: Annotated[schemas.user.User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Renders the main user dashboard with tech stack context and history."""
    stmt = (
        select(models.conversation.Conversation)
        .where(models.conversation.Conversation.user_id == current_user.id)
        .order_by(models.conversation.Conversation.created_at.desc())
        .limit(10)
    )
    history = (await db.scalars(stmt)).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "history": history
        }
    )

@router.post("/chat")
async def query_mapping_engine(
    question: Annotated[str, Form()],
    current_user: Annotated[schemas.user.User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Receives questions from dashboard UI and returns RAG/Mapping answers."""
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Execute RAG classifier and pipeline routing
    raw_answer = rag_router.invoke({"question": question})
    answer = str(raw_answer)

    # 2. Persist conversation entry
    chat_record = models.conversation.Conversation(
        user_id=current_user.id,
        question=question,
        response=answer
    )
    db.add(chat_record)
    await db.commit()

    return {"question": question, "response": answer}