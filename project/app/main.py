from contextlib import asynccontextmanager

from app.api import router as api_router
from app.database import create_database_if_not_exist
from app.exceptions import init_exception_handler
from app.log import init_log
from app.middlewares import init_middlewares
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await create_database_if_not_exist()
    yield


app = FastAPI(title="Insta Influencer API", lifespan=lifespan)

init_log()
init_exception_handler(app)
init_middlewares(app)
app.include_router(api_router, prefix="/api")
