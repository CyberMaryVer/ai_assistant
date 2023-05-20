from fastapi import Depends, APIRouter, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.types import Json
from typing import Optional
from loguru import logger

from fastapi_app.utils.auth import get_current_active_user
# from fastapi_app.sql_tools.database import get_entries_from_collection, create_user

router = APIRouter()


class User(BaseModel):
    login: str
    email: Optional[str] = None
    username: Optional[str] = None
    is_disabled: Optional[bool] = None
    settings: Optional[dict] = None


class UserSettingsEntry(BaseModel):
    login: str
    email: str
    username: str
    is_disabled: bool
    settings: dict


class UserInDB(BaseModel):
    def __init__(self,
                 login: str = Query(..., example="test", description="User login"),
                 email: str = Query(..., example="test@mail.com", description="User email"),
                 username: str = Query(..., example="test_user", description="User username"),
                 is_disabled: bool = Query(False, description="User disabled"),
                 settings: dict = Query({}, description="User settings"),
                 **kwargs):
        self.login = login
        self.email = email
        self.username = username
        self.is_disabled = is_disabled
        self.settings = settings


@router.get("/db_users/")
async def get_users():
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /db_users/ called")
    # return {"users": user_entries}
    return {"users": "not implemented"}

@router.get("/edit_user/")
async def edit_user(login: str = Query(..., example="user12345", description="User login"),
                    email: str = Query(..., example="user@yahoo.com", description="User email"),
                    username: str = Query(..., example="user", description="User username"),
                    is_disabled: bool = Query(False, description="If true, user is disabled"),
                    topic_enabled: bool = Query(True, description="If true, topic selection is enabled"),
                    source_enabled: bool = Query(True, description="If true, sources are shown"),
                    new_user: bool = Query(True, description="If true, new user is created")
                    ):
    new_entry = UserSettingsEntry(login=login, email=email, username=username, is_disabled=is_disabled,
                                  settings=dict(topic_enabled=topic_enabled,
                                                source_enabled=source_enabled,))
    new_entry_dict = new_entry.dict()
    new_entry_dict = jsonable_encoder(new_entry_dict)

    if new_user:
        # status = create_user(new_entry_dict)
        logger.debug(f"New user created: {new_entry.login}")
    else:
        # await edit_user(new_entry_dict)
        status = "not implemented"
        logger.debug(f"User edited: {new_entry.login}")

    return {"new_entry": new_entry_dict, "status": status}


# @router.post("/token")
# async def login_by_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     users_db = get_db()
#     user_dict = users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
