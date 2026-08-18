from fastapi import APIRouter
from fastapi import status, HTTPException, Depends
from src.context_manager.mipa_context_manager import context_manager
from src.DTO.api_key_update_body import APIKeyUpdateBody
from src.api.jwt_decode import extract_username
import json

user_secrets_router = APIRouter(
    tags=["secrets"]
)

with open("config.json", "r") as f:
    config = json.load(f)


@user_secrets_router.post("/mipa/api/add/api_key")
async def add_or_update_api_key(api_key_update_body: APIKeyUpdateBody, username: str = Depends(extract_username)):
    provider_name: str = api_key_update_body.provider_name
    api_key: str = api_key_update_body.api_key
    if provider_name not in frozenset(config.get("model_providers")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "ERROR",
                "message": "provider is not supposrted yet"
            }
        )

    map: dict[str, str] = config.get("provider_to_api_key_mapping")
    flag = context_manager.get_user_secrets_repository().add_or_update_key(
            username=username,
            key_name=map.get(provider_name),
            key=api_key
        )

    if flag:
        return {
            "status": "OK",
            "message": "api key added successfully"
        }

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "status": "ERROR",
            "message": "something went wrong"
        }
    )
