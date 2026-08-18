from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.context_manager.mipa_context_manager import context_manager

# GET THE SCHEME
bearer_scheme = HTTPBearer()
security_manager = context_manager.get_security_manager()


def extract_username(credential: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    # RETURNS ONLY THE JWT TOKEN WITHOUT BEAERER HEAD
    token = credential.credentials

    username = security_manager.verify_token(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "ERROR",
                "message": "invalid credentials or jwt has expired"
            }
        )

    return username
