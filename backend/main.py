from fastapi import FastAPI
from databse.config import create_db_and_tables

app = FastAPI()

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "TaskFlow API running"}