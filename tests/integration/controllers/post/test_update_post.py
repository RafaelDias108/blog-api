from httpx import AsyncClient
from fastapi import status
import pytest_asyncio

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.posts import PostService

    service = PostService()

    await service.create(PostIn(title="First Post", content="Content of the first post.", published=True))
    await service.create(PostIn(title="Second Post", content="Content of the second post.", published=True))
    await service.create(PostIn(title="Third Post", content="Content of the third post.", published=False))


async def test_update_post_success(client: AsyncClient, access_token: str):
    post_id = 1
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"title": "Updated Title first post"}

    response = await client.patch(
        f"/posts/{post_id}",
        headers=headers,
        json=payload,
    )
    
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == post_id
    assert content["title"] == payload["title"]


async def test_update_post_authenticated_fail(client: AsyncClient):
    post_id = 1
    headers = {}
    payload = {"title": "Updated Title first post"}

    response = await client.patch(
        f"/posts/{post_id}",
        headers=headers,
        json=payload,
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_update_post_not_found_fail(client: AsyncClient, access_token: str):
    post_id = 999
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"title": "Updated Title first post"}

    response = await client.patch(
        f"/posts/{post_id}",
        headers=headers,
        json=payload,
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND