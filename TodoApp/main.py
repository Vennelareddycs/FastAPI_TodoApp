#root folder to create fast api appl

from fastapi import FastAPI, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/healthy', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)