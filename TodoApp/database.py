
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# url is to able to create a location of this database on our fast api appli
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/TodoAppDB'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



