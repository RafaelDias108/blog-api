from httpx import AsyncClient
from fastapi import status

async def test_create_post_success(client: AsyncClient, access_token: str):
    response = await client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is a test post."},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] is not None
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post."

async def test_create_post_invalid_payload_fail(client: AsyncClient, access_token: str):
    # Given | Arrange
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"title": "Test Post"}  # Missing 'content'

    # When | Act
    response = await client.post(
        "/posts",
        json=payload,
        headers=headers
    )
    
    # Then | Assert
    content = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert content["detail"][0]["msg"] == "Field required"
    assert content["detail"][0]["loc"] == ["body", "content"]

async def test_create_post_not_authenticated_fail(client: AsyncClient):
    # Given | Arrange
    payload = {"title": "Test Post", "content": "This is a test post.", "published": True, "published_at": "2024-06-01T12:00:00Z"}

    # When | Act
    response = await client.post(
        "/posts",
        json=payload,
        headers={}
    )
    
    # Then | Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED