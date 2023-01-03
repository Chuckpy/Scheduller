from fastapi import APIRouter, Depends

from core.schemas.user_schema import UserSchema
from core.apps.auth.services.user_services import (
    UserLogin,
    UserRegister,
    UserToken,
    UserUpdate,
)


router = APIRouter(
    prefix="/auth", tags=["auth"], responses={200: {"Bearer": "access token"}}
)


@router.get("/me")
async def detailed_user(token: UserToken = Depends()):
    user = token.user
    return UserSchema(**(user.__dict__))


@router.put("/me")
async def detailed_user(token: UserUpdate = Depends()):
    user = token.update_user()
    return UserSchema(**(user.__dict__))


@router.post("/token")
async def login(user: UserLogin = Depends()):
    return user._create_access_token()


@router.post("/sign-in")
async def register(user_form: UserRegister = Depends()):
    user = user_form.create_user()
    return {"message": "success", "data": UserSchema(**(user.__dict__))}
