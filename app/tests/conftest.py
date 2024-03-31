from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from db.config import DatabaseSettings
import alembic.config
import alembic.command
import pytest
from db.dal.user import UserDAL
from services.user import UserService


def make_migrations(settings):
    config = alembic.config.Config()
    config.set_main_option("is_test", "True")
    config.set_main_option("script_location", "app/migrations")
    config.set_main_option("test_db_name", settings.db_name)
    alembic.command.upgrade(config, "head")


@pytest.fixture(scope="session")
def make_engine():
    settings = DatabaseSettings(db_name="databasefortest")
    create_database(settings.url)
    engine = create_engine(settings.url)
    make_migrations(settings)
    yield engine
    drop_database(settings.url)


@pytest.fixture(scope="function")
def create_session(make_engine):
    connection = make_engine.connect()
    transaction = connection.begin()
    session_maker = sessionmaker(bind=connection, expire_on_commit=False)
    session = session_maker()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def user_dal(create_session):
    return UserDAL(create_session)


@pytest.fixture(scope="function")
def user_service(user_dal):
    return UserService(user_dal)
