import asyncio
import os
import pytest_asyncio

from src.settings import settings
from httpx import AsyncClient

os.environ.setdefault("DATABASE_URL", settings.DATABASE_TEST_URL)

@pytest_asyncio.fixture
async def db(request):
    from src.database import database, metadata, engine
    
    await database.connect()
    metadata.create_all(engine)
    
    def teardown():
        async def __teardown():
            await database.disconnect()
            metadata.drop_all(engine)

        asyncio.run(__teardown())
    request.addfinalizer(teardown)


@pytest_asyncio.fixture
async def client(db):
    pass

@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    pass