from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .posts.views import router as post_router


async def get_api_key(
    api_key_header: str = Security(APIKeyHeader(name="API-KEY", auto_error=True)),
) -> str:
    if api_key_header != "API-KEY":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return api_key_header


router = APIRouter(dependencies=[Depends(get_api_key)])
router.include_router(post_router)
