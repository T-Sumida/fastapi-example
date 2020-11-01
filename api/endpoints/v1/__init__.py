from fastapi import APIRouter
from api.endpoints.v1 import user

api_v1_router = APIRouter()
api_v1_router.include_router(
    user.router,
    prefix='/users',
    tags=['users'])