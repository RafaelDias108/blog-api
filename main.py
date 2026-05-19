from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, metadata, engine
from controllers import post


@asynccontextmanager
async def lifespan(app: FastAPI):
    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(router=post.router, tags=["Posts"])