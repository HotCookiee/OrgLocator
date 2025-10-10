from repositories.users import delete_user_by_id, get_user_by_name, verify_password

from argon2.exceptions import VerifyMismatchError

from fastapi.exceptions import HTTPException
from fastapi import status, Request


from schemas.user import AddTokenToUser, UserInfo

from uuid import uuid4

from datetime import datetime, timedelta, timezone

from repositories.users import add_refresh_token, get_jti_by_user_id, get_user_by_id

from core import JWT_SECRET_KEY, ALGORITHM

import jwt


async def user_authentication(auth_user_schema) -> UserInfo:
    user = await get_user_by_name(auth_user_schema.name)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    try:
        verify_password(user.password, auth_user_schema.password)
        return UserInfo(id=str(user.id), name=user.name, email=user.email)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
        )


def create_access_token(
    user_info: UserInfo, lifetime: timedelta = timedelta(minutes=30)
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + lifetime
    jti = str(uuid4())
    payload = {
        "sub": str(user_info["id"]),
        "name": user_info["name"],
        "email": user_info["email"],
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }

    access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return access_token


async def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(
            refresh_token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp"], "verify_exp": True},
        )

        user = await get_user_by_id(payload.get("sub"))
        user_info = UserInfo(id=str(user.id), name=user.name, email=user.email)
        return create_access_token(user_info.model_dump())
    except Exception as e:
        ...


async def create_refresh_token(
    user_info: UserInfo, lifetime: timedelta = timedelta(days=30)
) -> str:

    jti_record = await get_jti_by_user_id(user_id=str(user_info["id"]))

    if jti_record is not None:
        return jwt.encode(
            {
                "sub": str(user_info["id"]),
                "jti": jti_record.jti,
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int(jti_record.expires_at.timestamp()),
                "type": "refresh",
            },
            JWT_SECRET_KEY,
            algorithm=ALGORITHM,
        )

    now = datetime.now(timezone.utc)
    expire = now + lifetime
    jti = str(uuid4())

    payload = {
        "sub": str(user_info["id"]),
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "refresh",
    }

    refresh_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

    info_add_token = AddTokenToUser(
        user_id=user_info["id"],
        jti=jti,
        expires_at=expire,
        revoked=False,
        created_at=now,
        updated_at=now,
    )

    await add_refresh_token(info_add_token)
    return refresh_token


def is_access_token_valid(request: Request) -> bool:
    access_token = request.headers.get("Authorization")
    if not access_token:
        return False
    try:
        payload = jwt.decode(
            access_token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp"], "verify_exp": True},
        )
        if payload.get("type") != "access":
            return False
        return True
    except jwt.ExpiredSignatureError:
        # Токен истёк
        return False
    except jwt.InvalidTokenError:
        # Любая другая ошибка валидации
        return False


async def is_refresh_token_valid(request: Request) -> bool:
    refresh_token = request.headers.get("X-Refresh-Token")
    try:
        if refresh_token is None:
            return False
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False

    user_id = payload.get("sub")
    if user_id is None:
        return False

    exp = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
    if datetime.now(timezone.utc) > exp:
        return False

    if payload.get("type") != "refresh":
        return False

    jti_record = await get_jti_by_user_id(user_id=user_id)
    if jti_record is None or jti_record.jti != payload.get("jti"):
        return {"type_error": "database_error"}

    if jti_record.revoked:
        return False

    return True


async def deleted_user_by_user_id(user_id: str):
    try:
        await delete_user_by_id(user_id)
        return {"code": 200, "message": "Пользователь удален"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Данные не прошли проверку",
        )


def access_token_verification(request: Request):
    if not is_access_token_valid(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ошибка доступа"
        )

    else:
        return request
