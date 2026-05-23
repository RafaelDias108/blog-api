from fastapi import APIRouter, status

from schemas.auth import LoginIn
from security.sign_jwt import sign_jwt
from views.auth import LoginOut

router = APIRouter(prefix="/auth")

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginOut, description="Login")
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)