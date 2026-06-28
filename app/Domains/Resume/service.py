from typing import Any

from app.Shared.api_client import api
from app.Shared.storage import token_storage


class ResumeService:
    """
    Resume Service

    Responsible only for communicating with Laravel API.
    """

    async def list(self) -> list[dict[str, Any]]:
        """
        GET /api/resumes
        """

        return await api.get("/resumes")

    async def show(
        self,
        resume_id: str,
    ) -> dict[str, Any]:
        """
        GET /api/resumes/{id}
        """

        return await api.get(
            f"/resumes/{resume_id}"
        )

    async def create(
        self,
        *,
        title: str,
        template_id: str | None,
        sections: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        POST /api/resumes
        """

        payload = {
            "title": title,
            "template_id": template_id,
            "sections": sections,
        }

        return await api.post(
            "/resumes",
            json=payload,
        )

    async def update(
        self,
        resume_id: str,
        *,
        title: str,
        template_id: str | None,
        sections: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        PUT /api/resumes/{id}
        """

        payload = {
            "title": title,
            "template_id": template_id,
            "sections": sections,
        }

        return await api.put(
            f"/resumes/{resume_id}",
            json=payload,
        )

    async def delete_resume(
            self,
            telegram_id: int,
            resume_id: str,
    ) -> dict:
        token = token_storage.get(
            telegram_id,
        )

        return await self.api.delete(
            f"/resumes/{resume_id}",
            token=token,
        )
    async def duplicate(
        self,
        resume_id: str,
    ) -> dict[str, Any]:
        """
        POST /api/resumes/{id}/duplicate
        """

        return await api.post(
            f"/resumes/{resume_id}/duplicate"
        )

    async def export_resume(
            self,
            telegram_id: int,
            resume_id: str,
            export_format: str = "pdf",
    ):
        token = token_storage.get_token(
            telegram_id,
        )

        return await self.api.post(

            f"/resumes/{resume_id}/export",

            token=token,

            json={
                "format": export_format,
            },
        )

resume_service = ResumeService()