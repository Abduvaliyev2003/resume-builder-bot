from typing import Any

from app.Shared.api_client import api


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

    async def delete(
        self,
        resume_id: str,
    ) -> dict[str, Any]:
        """
        DELETE /api/resumes/{id}
        """

        return await api.delete(
            f"/resumes/{resume_id}"
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


resume_service = ResumeService()