from sqlalchemy import text

from app.database import create_database_engine, create_session_factory


def test_database_engine_connects_to_postgresql():
    engine = create_database_engine("postgresql+psycopg:///shiftlist_test")

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))

            assert result.scalar_one() == 1
    finally:
        engine.dispose()


def test_session_factory_creates_working_session():
    engine = create_database_engine("postgresql+psycopg:///shiftlist_test")
    session_factory = create_session_factory(engine)

    try:
        with session_factory() as session:
            result = session.execute(text("SELECT 1"))

            assert result.scalar_one() == 1
    finally:
        engine.dispose()
