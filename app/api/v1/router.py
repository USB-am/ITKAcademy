from fastapi import APIRouter

from .endpoints.wallets import wallets_router


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(wallets_router)


@api_router.get('/version')
def get_version() -> dict[str, str]:
    return {'version': 'Version 1.0.0'}
