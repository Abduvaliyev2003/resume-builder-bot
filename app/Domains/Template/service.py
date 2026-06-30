from typing import Any

from app.Shared.api import api
from app.Shared.storage import token_storage


class TemplateService:
    """Template API service for Laravel template endpoints."""

    async def get_templates(
       self,
       telegram_id: int | None = None,
    ) -> list[dict[str, Any]]:
    
        token = None
        if telegram_id is not None:
           token = token_storage.get_token(telegram_id)

        response = await api.get(
           "/templates",
           token=token,
        )

        if isinstance(response, dict):
            templates = response.get("data") or response.get("templates") or []
        else:
            templates = response

        return templates


    async def get_template(
        self,
        template_id: str,
        telegram_id: int | None = None,
    ) -> dict[str, Any]:
        """Return one template by id."""

        token = None

        if telegram_id is not None:
            token = token_storage.get_token(telegram_id)

        return await api.get(
            f"/templates/{template_id}",
            token=token,
        )


template_service = TemplateService()
