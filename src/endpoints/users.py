from fastapi.routing import APIRouter
from fastapi import Response, Request, Depends
from schemas.user import AddUser, UserAuthentication
from models import Users
from services.users import (
    user_authentication,
    create_access_token,
    create_refresh_token,
    is_refresh_token_valid,
    refresh_access_token,
    deleted_user_by_user_id,
    access_token_verification,
)
from repositories.tools import add_object_to_the_database
from argon2 import PasswordHasher
from datetime import timedelta


user_router = APIRouter()
ph = PasswordHasher()


@user_router.post("/")
async def reg_user(user_schema: AddUser):
    user_schema.password = ph.hash(user_schema.password)
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await add_object_to_the_database(data(Users, user_schema))


@user_router.post("/login")
async def log_user(auth_user_schema: UserAuthentication, response: Response):
    user_info = await user_authentication(auth_user_schema)

    access_token = create_access_token(user_info.model_dump())
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    refresh_token = await create_refresh_token(user_info.model_dump())

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"code": 200, "access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/refresh")
async def refresh_user(response: Response, request: Request):
    if await is_refresh_token_valid(request):
        refresh_token = request.headers.get("X-Refresh-Token")
        print(refresh_token)
        new_access_token = await refresh_access_token(refresh_token)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return {"code": 200, "access_token": new_access_token}
    else:
        return {"code": 401}


@user_router.delete(
    "/by-id/{user_id}", dependencies=[Depends(access_token_verification)]
)
async def del_user(user_id: str):
    return await deleted_user_by_user_id(user_id)
