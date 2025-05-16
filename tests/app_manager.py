import os
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt
from fastapi import FastAPI
from httpx import AsyncClient

from app.account.auth_record import RefreshTokenRecord
from app.pet.pet_record import PetRecord


class AppManager:
    _app: FastAPI
    _client: AsyncClient

    def __init__(self, app: FastAPI, client: AsyncClient) -> None:
        self._app = app
        self._client = client

    def get_username(self) -> str:
        return os.getenv("ADMIN_USERNAME", "admin")

    def get_password(self) -> str:
        return os.getenv("ADMIN_PASSWORD", "password")

    def generate_access_token(self) -> str:
        payload = {
            "iss": os.getenv("JWT_ISS", "COOK_DING_SAASAAS"),
            "jti": uuid4().hex,
            "sub": os.getenv("ADMIN_USERNAME", "admin"),
            "aud": "API_ACCESS",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(
            payload=payload,
            key=bytes.fromhex(
                os.getenv("JWT_PRIVATE_KEY_HEX", ""),
            ).decode(),
            algorithm=os.getenv("JWT_SIGNING_ALGORITHM", "RS256"),
        )
        return token

    def generate_updated_jwt_token(self, token: str, fields: dict[str, Any]) -> str:
        payload = jwt.decode(jwt=token, options={"verify_signature": False})
        updated_payload = {
            **payload,
            **fields,
        }
        updated_token = jwt.encode(
            payload=updated_payload,
            key=bytes.fromhex(
                os.getenv("JWT_PRIVATE_KEY_HEX", ""),
            ).decode(),
            algorithm=os.getenv("JWT_SIGNING_ALGORITHM", "RS256"),
        )
        return updated_token

    async def reset_data(self) -> None:
        await PetRecord.all().delete()
        await RefreshTokenRecord.all().delete()
