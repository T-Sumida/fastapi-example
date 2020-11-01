import psycopg2
from core.config import get_env
from crud.base import get_db_session
from fastapi.testclient import TestClient
from main import app
from migrations.models import Base
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, drop_database

test_db_connection = create_engine(
    get_env().test_database_url,
    encoding='utf8',
    pool_pre_ping=True,
)


class BaseTestCase:
    def setup_method(self, method):
        """ 前処理
        """
        # テストDB作成
        self.__create_test_database()

        self.db_session = self.get_test_db_session()

        # APIクライアントの設定
        self.client = TestClient(app, base_url='https://localhost',)

        # DBをテスト用のDBでオーバーライド
        app.dependency_overrides[get_db_session] = \
            self.override_get_db

    def teardown_method(self, method):
        """ 後処理
        """
        # テストDB削除
        self.__drop_test_database()

        # オーバーライドしたDBを元に戻す
        app.dependency_overrides[self.override_get_db] = \
            get_db_session

    def override_get_db(self):
        """ DBセッションの依存性オーバーライド関数
        """
        yield self.db_session

    def get_test_db_session(self):
        """ テストDBセッションを返す
        """
        return scoped_session(sessionmaker(bind=test_db_connection))

    def __create_test_database(self):
        """ テストDB作成
        """
        # テストDBが削除されずに残ってしまっている場合は削除
        if database_exists(get_env().test_database_url):
            drop_database(get_env().test_database_url)

        # テストDB作成
        _con = \
            psycopg2.connect('host=db user=postgres password=postgres')
        _con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        _cursor = _con.cursor()
        _cursor.execute('CREATE DATABASE test_db_fastapi_sample')

        # テストDBにExtension追加
        _test_db_con = psycopg2.connect(
            'host=db dbname=test_db_fastapi_sample user=postgres password=postgres'
        )
        _test_db_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # テストDBにテーブル追加
        Base.metadata.create_all(bind=test_db_connection)

    def __drop_test_database(self):
        """ テストDB削除
        """
        drop_database(get_env().test_database_url)