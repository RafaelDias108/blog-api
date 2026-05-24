import asyncio
import os
import pytest_asyncio

from src.settings import settings
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("DATABASE_URL", settings.database_test_url)

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
    from src.main import app

    transport = ASGITransport(app=app)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with AsyncClient(base_url="http://test", transport=transport, headers=headers) as client:
        yield client

@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    response = await client.post("/auth/login", json={"user_id": 1})
    return response.json()["access_token"]