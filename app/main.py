from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import models
from .database import Base, engine
from . import api

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan = lifespan)


@app.get("/")
def main():
    return {"Message" : "Welcome to DevBuddy!"}

app.include_router(api.auth_router)
app.include_router(api.user_router)





















# from pydantic import BaseModel

# class QuestionRequest(BaseModel):
#     question: str

# from app.rag.pipeline.router import build_router

# router = build_router()

# @app.post("/ask")
# def ask(request: QuestionRequest):
#     response = router.invoke(request.question)
#     return {"answer": response}