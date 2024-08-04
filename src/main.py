from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connector import Database
from loaders import routers
from configs import SERVER, DB
import configparser


cfg = configparser.ConfigParser()
cfg.read("blog.conf")

app = FastAPI(**SERVER)
routers(app)


@app.on_event("startup")
async def startup():
    # Configuring DB with connection pulling and storing application state for resulablity
    db_inst = Database(**DB)
    await db_inst.connect()
    app.state.db = db_inst


@app.get("/")
async def root():
    return {"message": "My Blog API"}
