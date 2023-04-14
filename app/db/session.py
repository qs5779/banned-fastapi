import re
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.constants import KUNDEFINED

SQLALCHEMY_DATABASE_URL = getenv("DB_CONNECTION", KUNDEFINED)

if re.match("sqlite", SQLALCHEMY_DATABASE_URL):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
elif re.match("post", SQLALCHEMY_DATABASE_URL):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
