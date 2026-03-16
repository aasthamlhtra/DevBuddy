from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from typing import Annotated
from . import models
import os
import pytz
from dotenv import load_dotenv
from . import schemas
from .database import get_db
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ENCODING_ALGORITHM")


def create_access_token(data : dict, expires_at : timedelta | None = None):
    to_encode = data.copy()
    if expires_at is not None:
        expiry = datetime.now(timezone.utc) + expires_at
    else:
        expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp" : expiry})
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return access_token


password_hash = PasswordHash.recommended()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_password_hash(password : str):
    hash = password_hash.hash(password)
    return hash

def verify_password(entered_password, stored_hash):
    return password_hash.verify(entered_password, stored_hash)


async def get_user(db : AsyncSession, username : str):
    user = (await db.scalars(select(models.user.User).where(models.user.User.username == username))).one_or_none()
    return user

async def authenticate_user(db: AsyncSession, username : str, password : str):
    user = await get_user(db, username)
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def check_valid_username(db : AsyncSession, username : str):
    usr = (await db.scalars(select(models.user.User.username).where(models.user.User.username==username))).one_or_none()
    if usr is None:
        return True
    return False


async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_db)
):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if access_token.lower().startswith("bearer "):
        token = access_token.split(" ")[1]

        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user", headers={"WWW-Authenticate": "Bearer"})
        try : 
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = await get_user(db, username)
        if user is None:
            raise credentials_exception
        user_pydantic = schemas.user.User.model_validate(user)
        return user_pydantic