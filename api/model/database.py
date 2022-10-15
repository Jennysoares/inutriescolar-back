from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRE_DATABASE_URL = "postgres://elgixmap:j1ELns7Q6pC9sN2VYvK5U1P-wh-eFUr6@peanut.db.elephantsql.com/elgixmap"


engine = create_engine(
    POSTGRE_DATABASE_URL, echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

