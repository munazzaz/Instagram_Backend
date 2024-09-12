# main app file

from fastapi import FastAPI
from .database import Base, engine
from .api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Instagram Backend",
    version= "0.1",
    description= "Welcome to Instagram Backend remember to give your feedback!"
)
app.include_router(router)