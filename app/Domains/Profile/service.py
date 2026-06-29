from typing import Any

from app.Shared.api import api


class ProfileService:
    """Profile API service."""

    async def me(
        self,
        token: str,
    ) -> dict[str, Any]:
        """GET /api/me."""

        return await api.get(
            "/me",
            token=token,
        )


profile_service = ProfileService()
