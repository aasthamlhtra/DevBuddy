from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.api import auth, user

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base  # Adjust import paths to your project
import app.models  # Ensure models are imported so Base knows about them!

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Recreate missing tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")

# Mount authentication and user routers
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
async def landing_page(request: Request):
    """Renders the main public landing page (index.html)."""
    return templates.TemplateResponse("index.html", {"request": request})

