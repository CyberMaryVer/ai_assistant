from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    login: str
    email: Optional[str] = None
    username: Optional[str] = None
    is_expert: Optional[bool] = False
    is_devops: Optional[bool] = False
    disabled: Optional[bool] = False
    app_settings: Optional[dict] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, login: str):
    if login in db:
        user_dict = db[login]
        return UserInDB(**user_dict)


def mock_users():
    users = []
    for i in range(10):
        user = User()
        user.login = f"login{i}"
        user.email = f"email{i}"
        user.username = f"username{i}"
        user.is_expert = True if i % 2 == 0 else False
        user.is_devops = True if i % 3 == 0 else False
        user.app_settings = {"setting1": "value1", "setting2": "value2"}
        users.append(user)
    return users


def get_db():
    users = mock_users()
    db = {}
    for idx, user in enumerate(users):
        user.pop("_id")
        user["hashed_password"] = f"fakehashed{idx}"
        user["disabled"] = False
        db[user["login"]] = user
    return db


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    users_db = get_db()
    user = get_user(users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user