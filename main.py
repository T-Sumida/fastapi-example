from api.endpoints.v1 import api_v1_router
from fastapi import FastAPI
# from middleware import HttpRequestMiddleware

app = FastAPI()

app.include_router(api_v1_router, prefix='/api/v1')

# ミドルウェアの設定
# app.add_middleware(HttpRequestMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}