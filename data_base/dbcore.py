from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from decouple import config
from sqlalchemy_utils import database_exists


database_url = config('DATABASE_URL', default='sqlite:///./db.sqlite3')

engine = create_engine(database_url)

Base = declarative_base()


async def get_db():
    db = Session(engine)
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def create_database():
    if database_exists(engine.url):
        pass
    else:
        Base.metadata.create_all(engine)
