import uvicorn
import os
import re
import requests
from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    APIRouter,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from datetime import datetime
import redis.asyncio as redis
import db_handle
import jwt
from db_handle import get_user, SessionLocal, Session, add_user, Person
from logger_config import setup_logger


logger = setup_logger(__name__)

load_dotenv("/root/backend/.env")
TOKEN_ADMIN = os.getenv("TOKEN_ADMIN")
TOKEN_VALID_ADMIN = os.getenv("TOKEN_VALID_ADMIN")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
v1 = FastAPI()
app.mount("/v1", v1)
router = APIRouter()
v1.include_router(db_handle.router)
v1.include_router(router)


origins = [
    "http://localhost:5173",
    "https://10.128.0.24/",
    "https://10.128.0.24",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def headerget(token):
    return {
        "PI-Authorization": token,
    }


def headerpost(token):
    return {
        "Content-Type": "application/json",
        "PI-Authorization": token,
    }


@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_connection)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
    username: str | None = None

class UserInfo(BaseModel):
    username: str
    email: Optional[str] = Field(default=None)
    full_name: str | None = None
    @field_validator("email", mode="before", check_fields=True)
    def validate_email(cls, value):
        if value in (None, ""):
            return value
        pattern = r"^[a-zA-Z0-9._%]+@(gmail\.com|outlook\.com|outlook\.com\.vn|icloud\.com)$"
        if not re.match(pattern, value):
            logger.warning(f"Email {value} does not match the required pattern.")
            raise ValueError("Email must match the required pattern or be empty.")
        return value

class UserInPI(UserInfo):
    password: str
    
class User(UserInfo):
    id: int
    
@v1.post('/create_user/')
def create_user(user: UserInPI, resolver: str):
    try:
        print(user)
        print(resolver)
        db: Session = SessionLocal()
        data = {
            "user": user.username,
            "password": user.password,
            "resolver": resolver,
        }
        url="https://10.128.0.23/user/"
        req = requests.post(url, headers=headerpost(TOKEN_ADMIN), json=data, verify=False)
        print(req)
        if req.status_code != 200:
            return HTTPException(status_code=400, detail="Failed to create user")
        data = Person(email=user.email,full_name=user.full_name)
        add_user(user.username, data, db=db)
        return JSONResponse(content={"msg":"User created successfully"}, status_code=200)
    except Exception as e:
        logger.error(f"Error function >> [create_user] >> [except]: {e}")
        raise HTTPException(status_code=400, detail=e)


@v1.post("/privacy-auth/", dependencies=[Depends(RateLimiter(times=3, seconds=30))])
def privacy_auth(username: str, password: str):
    print(os.getenv("SECRET_KEY"))
    try:
        db: Session = SessionLocal()
        url = "https://10.128.0.23/validate/check"
        req = requests.post(
            url,
            headers=headerpost(TOKEN_VALID_ADMIN),
            json={"user": username, "pass": password},
            verify=False,
        )
        raw = req.json()
        auth = raw["result"]["authentication"]
        if auth != "ACCEPT":
            logger.error(f"Error function >> [privacy_auth] >> [check ACCEPT]: Failed to validate account: {username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")
        user = raw["detail"]["user"]
        id = int(user["id"])
        info_user_authenticate = get_user(id, db)
        return User(**info_user_authenticate)
    except Exception as e:
        logger.error(f"Error function >> [privacy_auth] >> [except]: {e}")
        raise HTTPException(status_code=400, detail="Failed to validate account")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    db: Session = SessionLocal()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(id=id, username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(id=token_data.id, db=db)
    if user is None:
        raise credentials_exception
    return User(**user)


@v1.post("/token", dependencies=[Depends(RateLimiter(times=3, seconds=30))])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = privacy_auth(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "fullname": user.full_name,
            "email": user.email,
        },
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@v1.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@v1.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
    

if __name__ == "__main__":
    config = uvicorn.Config(
        "handle:app",
        port=5000,
        log_level="info",
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem",
    )
    server = uvicorn.Server(config)
    server.run()
