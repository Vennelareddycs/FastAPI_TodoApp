from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread': False}, # allowing the same database connection to be used across different threads (which is usually not recommended for production use without proper precautions)
                       poolclass = StaticPool, # simple static connection pool(cache of database connections that can be reused, which helps improve performance and
                                                # StaticPool is a simple connection pool that doesn't manage connections dynamically, maintains fixed set of connection pools)
                       )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)


@pytest.fixture # piece of data or setup code that can be reused across multiple tests.
def test_todo():
    todo = Todos(
        title= "Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal() # used to interact with the database in a testing environment.
    db.add(todo)
    db.commit()
    yield todo
    # After test is done, it cleans up by deleting all todo items from the database
    with engine.connect() as connection: # allows us to execute raw SQL queries
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="vennela24",
        email="vennela@email.com",
        first_name="vennela",
        last_name="gowda",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

