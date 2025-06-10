from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.common.common_schema import JWTAudience
from tests.app_manager import AppManager


@pytest.mark.anyio
async def test_auth(
    app: FastAPI,
    client: AsyncClient,
    app_manager: AppManager,
):
    res = await client.post(
        "/api/auth/verify",
        json={
            "username": app_manager.get_username(),
            "password": app_manager.get_password(),
        },
    )

    assert res.status_code == 200
    assert res.json()["data"]["accessToken"] is not None
    assert res.json()["data"]["accessTokenExpiresAt"] is not None
    assert res.json()["data"]["refreshToken"] is not None
    assert res.json()["data"]["refreshTokenExpiresAt"] is not None

    access_token_payload = jwt.decode(
        jwt=res.json()["data"]["accessToken"], options={"verify_signature": False}
    )

    assert access_token_payload["sub"] is not None
    assert access_token_payload["aud"] == "API_ACCESS"
    refresh_token_payload = jwt.decode(
        jwt=res.json()["data"]["refreshToken"], options={"verify_signature": False}
    )

    assert refresh_token_payload["sub"] is not None
    assert refresh_token_payload["aud"] == "TOKEN_REFRESH"


@pytest.mark.anyio
async def test_auth_validation(
    app: FastAPI,
    client: AsyncClient,
    app_manager: AppManager,
):
    res = await client.post(
        "/api/auth/verify",
        json={
            "username": app_manager.get_username(),
            "password": uuid4().hex,
        },
    )

    assert res.status_code == 401
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "UNAUTHORIZED_ERROR"


@pytest.mark.anyio
async def test_auth_refresh_token(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    res = await client.post(
        "/api/auth/verify",
        json={
            "username": app_manager.get_username(),
            "password": app_manager.get_password(),
        },
    )
    refresh_token = res.json()["data"]["refreshToken"]

    res = await client.post(
        "/api/auth/refresh",
        json={
            "refreshToken": refresh_token,
        },
    )

    assert res.status_code == 200
    assert res.json()["data"]["accessToken"] is not None
    assert res.json()["data"]["accessTokenExpiresAt"] is not None
    assert res.json()["data"]["refreshToken"] is not None
    assert res.json()["data"]["refreshTokenExpiresAt"] is not None

    new_access_token_payload = jwt.decode(
        jwt=res.json()["data"]["accessToken"], options={"verify_signature": False}
    )

    assert new_access_token_payload["aud"] == "API_ACCESS"
    new_refresh_token = res.json()["data"]["refreshToken"]
    new_refresh_token_payload = jwt.decode(
        jwt=res.json()["data"]["refreshToken"], options={"verify_signature": False}
    )

    assert new_refresh_token_payload["aud"] == "TOKEN_REFRESH"

    res = await client.post(
        "/api/auth/refresh",
        json={
            "refreshToken": refresh_token,
        },
    )

    assert res.status_code == 401
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "INVALID_TOKEN_ERROR"

    res = await client.post(
        "/api/auth/refresh",
        json={
            "refreshToken": new_refresh_token,
        },
    )

    assert res.status_code == 200


@pytest.mark.anyio
async def test_auth_refresh_token_validation(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    res = await client.post(
        "/api/auth/verify",
        json={
            "username": app_manager.get_username(),
            "password": app_manager.get_password(),
        },
    )
    access_token = res.json()["data"]["accessToken"]
    refresh_token = res.json()["data"]["refreshToken"]
    expired_refresh_token = app_manager.generate_updated_jwt_token(
        refresh_token,
        {
            "iat": datetime.now(timezone.utc) - timedelta(seconds=600),
            "exp": datetime.now(timezone.utc) - timedelta(seconds=300),
        },
    )

    res = await client.post(
        "/api/auth/refresh",
        json={
            "refreshToken": expired_refresh_token,
        },
    )

    assert res.status_code == 401
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "EXPIRED_TOKEN_ERROR"

    res = await client.post(
        "/api/auth/refresh",
        json={
            "refreshToken": access_token,
        },
    )

    assert res.status_code == 401
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "INVALID_TOKEN_ERROR"


@pytest.mark.anyio
async def test_auth_cleanup(app: FastAPI, client: AsyncClient, app_manager: AppManager):
    access_token = app_manager.generate_access_token()
    res = await client.post(
        "/api/auth/cleanup-expired-token",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "limit": 100,
        },
    )

    assert res.status_code == 200

    refresh_token = app_manager.generate_updated_jwt_token(
        access_token,
        {
            "aud": JWTAudience.TOKEN_REFRESH,
        },
    )
    res = await client.post(
        "/api/auth/cleanup-expired-token",
        headers={
            "Authorization": f"Bearer {refresh_token}",
        },
        json={
            "limit": 100,
        },
    )

    assert res.status_code == 403
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "FORBIDDEN_ERROR"

    res = await client.post(
        "/api/auth/cleanup-expired-token",
        headers={
            "Authorization": f"Bearer {uuid4().hex}",
        },
        json={
            "limit": 100,
        },
    )

    assert res.status_code == 403
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "FORBIDDEN_ERROR"

    res = await client.post(
        "/api/auth/cleanup-expired-token",
        json={
            "limit": 100,
        },
    )

    assert res.status_code == 403
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "FORBIDDEN_ERROR"
