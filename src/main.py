from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import database, metadata, engine
from src.controllers import post
from src.controllers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Blog API", version="1.0.0", lifespan=lifespan)
app.include_router(router=auth.router, tags=["Authentication"])
app.include_router(router=post.router, tags=["Posts"])