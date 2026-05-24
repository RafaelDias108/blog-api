from httpx import AsyncClient
from fastapi import status

async def test_login_success(client: AsyncClient):
    # Given
    payload = {"user_id": 1}
    
    # When
    response = await client.post("/auth/login", json=payload)
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None