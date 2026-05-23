import time
import uuid
import jwt

from pydantic import BaseModel
from src.settings import settings

SECRET = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes

class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    nbf: float
    iat: float
    jti: str

class JWTToken(BaseModel):
    access_token: AccessToken


def sign_jwt(user_id: int) -> dict[str, str]:
    now = time.time()
    payload = {
        "iss": "bootcamp-fastapi.com.br",
        "sub": str(user_id),
        "aud": "bootcamp-fastapi",
        "exp": now + (60 * ACCESS_TOKEN_EXPIRE_MINUTES),
        "nbf": now,
        "iat": now,
        "jti": uuid.uuid4().hex,
    }
    token = jwt.encode(payload=payload, key=SECRET, algorithm=ALGORITHM)
    return { "access_token": token }

async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, key=SECRET, audience="bootcamp-fastapi", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({ "access_token": decoded_token })
        return _token if _token.access_token.exp >= time.time() else None
    except jwt.PyJWTError:
        return None
    except Exception:
        return None