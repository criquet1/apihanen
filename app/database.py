from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# https://dev.to/cuongld2/build-simple-api-service-with-python-fastapi-part-1-581o
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/serversiderendering" "3306"
SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name} '

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()