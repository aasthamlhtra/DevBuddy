from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Path, Query
from fastapi.responses import RedirectResponse , HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, models
from ..database import get_db
from ..utils import get_current_user
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUUTES", 30))

router = APIRouter(prefix="/user", tags=["user"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
async def dashboard_page(
    request: Request,
    current_user: Annotated[schemas.user.User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # """Dashboard page - could also render as HTML"""
    
    # # You could query mappings here and render them
    # # OR fetch via JavaScript API calls
    
    # return templates.TemplateResponse(
    #     "dashboard.html",
    #     {
    #         "request": request,
    #         "user": current_user
    #     }
    # )
    return {"message":"You're on dashboard"}