from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connector import Database
import configparser
from routers import users, blogs, documents, comments

cfg = configparser.ConfigParser()
cfg.read("blog.conf")

server_info = dict(cfg.items("API"))
connection_info = dict(cfg.items("DB"))
app = FastAPI(**server_info)


@app.on_event("startup")
async def startup():
    db_inst = Database(**connection_info)
    await db_inst.connect()
    app.state.db = db_inst


app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(documents.router)
app.include_router(comments.router)


@app.get("/")
async def root():
    return {"message": "My Blog API"}
