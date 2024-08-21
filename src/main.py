from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connector import Database
from loaders import routers
from configs import SERVER, DB, LOG
from loggers import default_logger
import configparser


log = default_logger(LOG)

app = FastAPI(**SERVER)

try:
    log.info("loading routes")
    routers(app)
except Exception as e:
    log.error(e)
    raise Exception(e)


@app.on_event("startup")
async def startup():
    # Configuring DB with connection pulling and storing application state for resulablity
    try:
        log.info("initializing DB connector")
        db_inst = Database(**DB)
    except Expecption as e:
        log.error(e)
    await db_inst.connect()
    app.state.db = db_inst
    app.log = log


@app.get("/")
async def root():
    return {"message": "My Blog API"}
