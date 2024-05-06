import os
from contextlib import contextmanager
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()


@lru_cache(maxsize=1)
def is_test():
    return os.getenv("PYTEST_CURRENT_TEST") is not None


@lru_cache(maxsize=1)
def get_db_url():
    if is_test():
        return "sqlite:////tmp/test_db.db"
    return os.getenv("DATABASE_URL")


@lru_cache(maxsize=1)
def get_engine(DB_URL=get_db_url()):
    return create_engine(DB_URL)


@contextmanager
def db_scope(DB_URL=get_db_url(), auto_flush=True):
    engine = get_engine(DB_URL)
    session_factory = sessionmaker(bind=engine, autoflush=auto_flush)
    s = scoped_session(session_factory)
    try:
        yield s
    except:
        raise
    finally:
        s.close()


def db_init():
    # Import models for metadata registration
    import models

    # Create tables
    db = get_engine()
    models.Base.metadata.create_all(db)
