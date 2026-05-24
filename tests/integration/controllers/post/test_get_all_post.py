from httpx import AsyncClient
from fastapi import status
import pytest_asyncio
import pytest

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.posts import PostService

    service = PostService()

    await service.create(PostIn(title="First Post", content="Content of the first post.", published=True))
    await service.create(PostIn(title="Second Post", content="Content of the second post.", published=True))
    await service.create(PostIn(title="Third Post", content="Content of the third post.", published=False))

@pytest.mark.parametrize("published, total", [
    (True, 2),
    (False, 1)
])
async def test_get_all_posts_by_status_success(client: AsyncClient, access_token: str, published: bool, total: int):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(
        f"/posts",
        params=params,
        headers=headers
    )
    
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == total

async def test_get_all_posts_limit_success(client: AsyncClient, access_token: str):
    params = {"published": True, "limit": 1}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = await client.get(
        f"/posts",
        params=params,
        headers=headers
    )
    
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1

async def test_get_all_posts_not_authenticated_fail(client: AsyncClient):
    params = {"published": True, "limit": 1}
    headers = {}
    
    response = await client.get(
        f"/posts",
        params=params,
        headers=headers
    )
    
    data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_get_all_posts_empty_params_fail(client: AsyncClient, access_token: str):
    params = {}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = await client.get(
        f"/posts",
        params=params,
        headers=headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT