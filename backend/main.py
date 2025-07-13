from fastapi import FastAPI
from databse.config import create_db_and_tables
from api.routers import auth, projects

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()