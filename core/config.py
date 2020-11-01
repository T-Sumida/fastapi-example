import os
from functools import lru_cache
from pydantic import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Environment(BaseSettings):
    """ 環境変数を読み込むファイル
    """
    debug: bool  # .envから読み込んだ値をbool型にキャッシュ
    database_url: str
    test_database_url: str  # 追加

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')


@lru_cache
def get_env():
    """ 「@lru_cache」でディスクから読み込んだ.envの結果をキャッシュする
    """
    return Environment()