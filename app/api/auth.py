from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Path, Query
from fastapi.responses import RedirectResponse , HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, Text
from .. import schemas, models
from ..database import get_db
from ..utils import create_password_hash, authenticate_user, create_access_token, get_current_user, check_valid_username
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
import os

load_dotenv()

ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUUTES", 30))

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request : Request):
    return templates.TemplateResponse(
        "login.html",
        {"request":request}
    )


@router.post("/login", response_model=schemas.auth.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token  = create_access_token({"sub":user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))

    redirect_url = "/auth/dashboard"
    response = RedirectResponse(redirect_url, status_code=303)
    response.set_cookie(
            key = "access_token",
            value = f"Bearer {access_token}",
            httponly=True,
            samesite="lax"
        )

    return response

@router.get("/register", response_class=HTMLResponse)
def register_page(request : Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/email", response_class=RedirectResponse)
async def register_user(
    email_model: Annotated[schemas.register.RegisterEmail, Form()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    data = (await db.scalars(select(models.user.User.email).where(models.user.User.email == email_model.email))).one_or_none()
    if data is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    else:
        return RedirectResponse(f"/auth/register/details?email={email_model.email}", status_code=status.HTTP_303_SEE_OTHER)
    
@router.get("/register/details", response_class=HTMLResponse)
def register_email_page(request : Request, email : Annotated[str, Query(...)]):
    return templates.TemplateResponse("register_email.html", {"request": request, "email":email})

@router.post("/register/details", response_class=RedirectResponse)
async def register_email_page(request : Request, 
                        email : Annotated[str, Query(...)], 
                        data : Annotated[schemas.register.RegisterUser, Form()],
                        db: Annotated[AsyncSession, Depends(get_db)]):
    
    data_dict = data.model_dump()

    hashed_password = create_password_hash(data_dict["password"])

    data_dict.update({"password" : hashed_password}) 

    data_dict.update({"email" : email}) 

    new_user = models.user.User(**data_dict)

    if await check_valid_username(db, data_dict["username"]):
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        access_token  = create_access_token({"sub":data_dict["username"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))
        redirect_url = "/auth/onboarding"
        response = RedirectResponse(redirect_url, status_code=303)
        response.set_cookie(
            key = "access_token",
            value = f"Bearer {access_token}",
            httponly=True,
            samesite="lax"
        )

        return response

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username is already taken!")
   

@router.get("/onboarding", response_class=HTMLResponse)
async def info_page(request : Request, 
              current_user: Annotated[schemas.user.User, Depends(get_current_user)],
              db: Annotated[AsyncSession, Depends(get_db)]):
    """Onboarding page with tech stack selection"""
    
    # Get all tech stacks
    result = await db.execute(
    select(models.techstack.TechStack).order_by(
        models.techstack.TechStack.category,
        models.techstack.TechStack.name
    )
)

    tech_stacks = result.scalars().all()
    
    # Group by category (optional but nice)
    tech_stacks_by_category = defaultdict(list)
    for ts in tech_stacks:
        tech_stacks_by_category[ts.category].append(ts)
    
    # Pass data to template
    return templates.TemplateResponse(
        "onboarding.html",
        {
            "request": request,
            "user": current_user,
            "tech_stacks_by_category": tech_stacks_by_category
        }
    )


# Same file: app/api/pages.py

@router.post("/onboarding", response_class=RedirectResponse)
async def submit_onboarding_form(
    request: Request,
    current_user: Annotated[schemas.user.User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    primary_tech_stack: str = Form(...),      # Gets value from <select name="primary_tech_stack">
    learning_tech_stack: str = Form(...),     # Gets value from <select name="learning_tech_stack">
):
    """
    Process onboarding form submission
    """
    
    # Validate selections are different
    if primary_tech_stack == learning_tech_stack:
        # Re-render form with error message
        result = await db.execute(
        select(models.techstack.TechStack).order_by(
            models.techstack.TechStack.category,
            models.techstack.TechStack.name
            )
        )

        tech_stacks = result.scalars().all()
        
        # Group by category (optional but nice)
        tech_stacks_by_category = defaultdict(list)
        for ts in tech_stacks:
            tech_stacks_by_category[ts.category].append(ts)
        
        return templates.TemplateResponse(
            "onboarding.html",
            {
                "request": request,
                "user": current_user,
                "tech_stacks_by_category": tech_stacks_by_category,
                "error": "Please select different technologies",
                "primary_tech_stack": primary_tech_stack,      # Preserve selection
                "learning_tech_stack": learning_tech_stack     # Preserve selection
            }
        )

    # Update user in database
    stmt = update(models.user.User).where(models.user.User.username == current_user.username).values(primary_tech_stack=primary_tech_stack, learning_tech_stack=learning_tech_stack, updated_at=datetime.now())
    await db.execute(stmt)
    await db.commit()
    
    # Redirect to dashboard
    return RedirectResponse(url="/user/dashboard", status_code=status.HTTP_303_SEE_OTHER)



# @router.get("/feedtech")
# def feed_tech_stacks(db: Session = Depends(get_db)):
#     tech_stacks = [
#         # Languages
#         {"name": "Python", "category": "language", 
#          "description": "High-level, general-purpose programming language"},
#         {"name": "JavaScript", "category": "language",
#          "description": "Programming language for web development"},
#         {"name": "Java", "category": "language",
#          "description": "Object-oriented programming language"},
#         {"name": "TypeScript", "category": "language",
#          "description": "Typed superset of JavaScript"},
#         {"name": "Go", "category": "language",
#          "description": "Statically typed, compiled language by Google"},
#         {"name": "Rust", "category": "language",
#          "description": "Systems programming language focused on safety"},
        
#         # Frameworks
#         {"name": "FastAPI", "category": "framework",
#          "description": "Modern Python web framework"},
#         {"name": "Express", "category": "framework",
#          "description": "Minimalist Node.js web framework"},
#         {"name": "React", "category": "framework",
#          "description": "JavaScript library for building UIs"},
#         {"name": "Django", "category": "framework",
#          "description": "High-level Python web framework"},
#         {"name": "Flask", "category": "framework",
#          "description": "Lightweight Python web framework"},
        
#         # Databases
#         {"name": "PostgreSQL", "category": "database",
#          "description": "Advanced relational database"},
#         {"name": "MongoDB", "category": "database",
#          "description": "NoSQL document database"},
#         {"name": "Redis", "category": "database",
#          "description": "In-memory data structure store"},
#     ]
    
#     for ts_data in tech_stacks:
#         # Check if already exists
#         existing = db.query(models.techstack.TechStack).filter(
#             models.techstack.TechStack.name == ts_data["name"]
#         ).first()
        
#         if not existing:
#             ts = models.techstack.TechStack(**ts_data)
#             db.add(ts)
    
#     db.commit()
#     print("✅ Tech stacks seeded")
#     db.close()
#     return {"message":"database seeded!"}