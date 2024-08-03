from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connector import Database
import configparser
from routers import users, blogs

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


@app.get("/")
async def root():
    x = await app.state.db.fetch_rows("SELECT * FROM USERS;")
    print(type(x[0]), dict(x[0]))
    return {"message": "My Blog API"}
