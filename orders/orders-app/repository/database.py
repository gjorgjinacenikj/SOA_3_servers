import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repository.db_creds import user, password, dbname
from repository.repo_models import Base, Order
#SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@localhost/{dbname}".format(user=user,password=password,dbname=dbname)
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def initialize_database():
    Base.metadata.drop_all(bind=engine, tables=[Order.__table__])
    print("Creating")
    Base.metadata.create_all(engine)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
