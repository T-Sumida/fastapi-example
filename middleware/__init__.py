from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)

        # 予期せぬ例外
        except Exception as e:
            print(e)
            getattr(request.state, 'db_session', Session).rollback()  # これに書き換え
            raise e

        # 正常終了時
        else:
            getattr(request.state, 'db_session', Session).commit()  # これに書き換え
            return response

        # DBセッションの破棄は必ず行う
        finally:
            getattr(request.state, 'db_session', Session).remove()  # これに書き換え
