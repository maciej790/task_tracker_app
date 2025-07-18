from fastapi import FastAPI
from databse.config import create_db_and_tables
from api.routers import auth, projects, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()