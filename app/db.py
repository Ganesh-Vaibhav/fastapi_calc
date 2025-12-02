import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/fastapi_db",
    ),
)

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(DATABASE_URL, future=True, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
