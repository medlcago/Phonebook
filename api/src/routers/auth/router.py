from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import Token
from schemas.user import CreateUser, ResponseUser
from services.auth import AuthService, get_current_user

router = APIRouter(prefix="/user/auth", tags=["User Authorization"])


@router.post("/sign-up", response_model=Token)
async def sign_up(data: CreateUser, service: AuthService = Depends()):
    return await service.register_new_user(data)


@router.post("/sign-in", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    return await service.authenticate_user(
        form_data.username,
        form_data.password
    )


@router.get("/user", response_model=ResponseUser)
async def get_user(user: ResponseUser = Depends(get_current_user)):
    return user
