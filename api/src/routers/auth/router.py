from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from config import config
from schemas.auth import Token
from schemas.user import CreateUser, ResponseUser, LoginUser
from services.auth import AuthService, get_current_user

router = APIRouter(prefix="/user/auth", tags=["User Authorization"])
templates = config.templates


@router.post("/sign-up", response_model=Token, status_code=201)
async def sign_up(data: CreateUser, service: AuthService = Depends()):
    return await service.register_new_user(data)


@router.post("/sign-in", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    return await service.authenticate_user(
        form_data.username,
        form_data.password
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(user: LoginUser, service: AuthService = Depends()):
    return await service.authenticate_user(
        username=user.username,
        password=user.password
    )


@router.get("/user", response_model=ResponseUser)
async def get_user(user: ResponseUser = Depends(get_current_user)):
    return user


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "url": router.url_path_for})


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "url": router.url_path_for})
