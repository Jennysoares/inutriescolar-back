from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRE_DATABASE_URL = "postgresql://postgres:200812@localhost/inutriescolar_db"


engine = create_engine(
    POSTGRE_DATABASE_URL, echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

