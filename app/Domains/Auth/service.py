from typing import Any

from app.Shared.api import api


class AuthService:
    """Authentication API service for Laravel auth endpoints."""

    async def login(
        self,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """Authenticate a user through POST /api/login."""

        return await api.post(
            "/login",
            {
                "email": email,
                "password": password,
            },
        )

    async def telegram_login(
        self,
        *,
        email: str,
        password: str,
        telegram_id: int,
        telegram_username: str | None = None,
        telegram_first_name: str | None = None,
        telegram_last_name: str | None = None,
    ) -> dict[str, Any]:
        """Authenticate a Telegram user through POST /api/telegram/login."""

        payload: dict[str, Any] = {
            "email": email,
            "password": password,
            "telegram_id": telegram_id,
        }

        if telegram_username:
            payload["telegram_username"] = telegram_username

        return await api.post(
            "/telegram/login",
            payload,
        )

    async def register(
        self,
        name: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """Register a user through POST /api/register."""

        return await api.post(
            "/register",
            {
                "name": name,
                "email": email,
                "password": password,
            },
        )

    async def logout(
        self,
        token: str,
    ) -> dict[str, Any]:
        """Revoke the current Laravel access token through POST /api/logout."""

        return await api.post(
            "/logout",
            token=token,
        )

    async def me(
        self,
        token: str,
    ) -> dict[str, Any]:
        """Return the authenticated user through GET /api/me."""

        return await api.get(
            "/me",
            token=token,
        )

    async def telegram_logout(
        self,
        token: str,
        telegram_id: int,
    ) -> dict[str, Any]:
        """End a Telegram session through POST /api/telegram/logout."""

        return await api.post(
            "/telegram/logout",
            {
                "telegram_id": telegram_id,
            },
            token=token,
        )

    async def telegram_me(
        self,
        token: str,
        telegram_id: int,
    ) -> dict[str, Any]:
        """Return Telegram session data through GET /api/telegram/me."""

        return await api.get(
            "/telegram/me",
            token=token,
            params={
                "telegram_id": telegram_id,
            },
        )


auth_service = AuthService()
