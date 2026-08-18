from fastapi import APIRouter, status, Depends, HTTPException
from src.api.jwt_decode import extract_username
from src.DTO.user_registration_body import UserRegistrationBody
from src.DTO.user_login_body import UserLoginBody
from src.context_manager.mipa_context_manager import context_manager

user_router = APIRouter(
    tags=["user"]
)

user_repository = context_manager.get_user_repository()
security_manager = context_manager.get_security_manager()
password_encoder = context_manager.get_password_encoder()


@user_router.post("/mipa/api/user/register")
async def register_user(user: UserRegistrationBody):
    s = user_repository.register(user)
    if s:
        return {
            "status": "OK",
            "message": "user registered successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username, mobile number or email id already exists"
        )


@user_router.post("/mipa/api/user/login")
async def login_user(user_login_body: UserLoginBody):
    user = user_repository.find_user(user_login_body.username)
    if user is not None and password_encoder.match_password(user_login_body.password, user.password):
        return {
            "status": "OK",
            "token": security_manager.generate_token(user.username)
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "ERROR",
            "message": "invalid credentials"
        }
    )


@user_router.delete("/mipa/api/user/delete")
async def delete_user(username: str = Depends(extract_username)):
    flag = user_repository.delete(username)
    if flag:
        return {
            "status": "OK",
            "message": "account deleted successfully"
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "status": "ERROR",
            "message": "user not found"
        }
    )
