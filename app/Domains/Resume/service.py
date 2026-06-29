from __future__ import annotations

from typing import Any

from app.Shared.api import api
from app.Shared.storage import token_storage


class ResumeService:
    """
    Resume Service

    Responsible only for communicating with Laravel API.
    """

    async def list(
        self,
        token: str,
    ) -> list[dict[str, Any]]:
        """
        GET /api/resumes
        """

        return await api.get(
            "/resumes",
            token=token,
        )

    async def get_all(
        self,
        token: str,
        page: int = 1,
    ) -> dict[str, Any]:
        """GET /api/resumes with Laravel pagination support."""

        return await api.get(
            "/resumes",
            token=token,
            params={
                "page": page,
            },
        )

    async def show(
        self,
        token: str,
        resume_id: str,
    ) -> dict[str, Any]:
        """
        GET /api/resumes/{id}
        """

        return await api.get(
            f"/resumes/{resume_id}",
            token=token,
        )

    async def get_resume(
        self,
        telegram_id: int,
        resume_id: str,
    ) -> dict[str, Any]:
        """GET /api/resumes/{id} using a stored user token."""

        token = token_storage.get_token(telegram_id)

        return await self.show(
            token=token or "",
            resume_id=resume_id,
        )

    async def create_resume(
            self,
            telegram_id: int,
            title: str,
            template_id: str | None = None,
            sections: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """POST /api/resumes using a stored user token."""

        token = token_storage.get_token(
            telegram_id,
        )

        return await api.post(
            "/resumes",
            token=token,
            data={
                "title": title,
                "template_id": template_id,
                "sections": sections or [],
            },
        )

    async def update(
        self,
        token: str,
        resume_id: str,
        *,
        title: str,
        template_id: str | None = None,
        sections: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        PUT /api/resumes/{id}
        """

        payload = {
            "title": title,
            "template_id": template_id,
            "sections": sections or [],
        }

        return await api.put(
            f"/resumes/{resume_id}",
            data=payload,
            token=token,
        )

    async def delete_resume(
            self,
            telegram_id: int,
            resume_id: str,
    ) -> dict[str, Any]:
        """DELETE /api/resumes/{id} using a stored user token."""

        token = token_storage.get_token(
            telegram_id,
        )

        return await api.delete(
            f"/resumes/{resume_id}",
            token=token,
        )

    async def duplicate(
        self,
        token: str,
        resume_id: str,
    ) -> dict[str, Any]:
        """
        POST /api/resumes/{id}/duplicate
        """

        return await api.post(
            f"/resumes/{resume_id}/duplicate",
            token=token,
        )

    async def export_resume(
            self,
            telegram_id: int,
            resume_id: str,
            file_type: str = "pdf",
    ) -> dict[str, Any]:
        """POST /api/resumes/{id}/export using a stored user token."""

        token = token_storage.get_token(
            telegram_id,
        )

        return await api.post(
            f"/resumes/{resume_id}/export",
            token=token,
            data={
                "file_type": file_type,
            },
        )

    async def download_file(
        self,
        download_token: str,
    ) -> tuple[bytes, str | None]:
        """GET /api/downloads/{token} as bytes."""

        return await api.get_bytes(
            f"/downloads/{download_token}",
        )

    async def grammar_check(
        self,
        token: str,
        resume_id: str,
        text: str,
    ) -> dict[str, Any]:
        """POST /api/resumes/{id}/grammar-check."""

        return await api.post(
            f"/resumes/{resume_id}/grammar-check",
            token=token,
            data={
                "text": text,
            },
        )

    async def ats_analyze(
        self,
        token: str,
        resume_id: str,
    ) -> dict[str, Any]:
        """POST /api/resumes/{id}/ats-analyze."""

        return await api.post(
            f"/resumes/{resume_id}/ats-analyze",
            token=token,
        )

    async def missing_sections(
        self,
        token: str,
        resume_id: str,
    ) -> dict[str, Any]:
        """POST /api/resumes/{id}/missing-sections."""

        return await api.post(
            f"/resumes/{resume_id}/missing-sections",
            token=token,
        )

    async def job_match(
        self,
        token: str,
        resume_id: str,
        *,
        job_title: str,
        job_description: str,
    ) -> dict[str, Any]:
        """POST /api/resumes/{id}/job-match."""

        return await api.post(
            f"/resumes/{resume_id}/job-match",
            token=token,
            data={
                "job_title": job_title,
                "job_description": job_description,
            },
        )

    async def ai_reviews(
        self,
        token: str,
        resume_id: str,
    ) -> dict[str, Any]:
        """GET /api/resumes/{id}/ai-reviews."""

        return await api.get(
            f"/resumes/{resume_id}/ai-reviews",
            token=token,
        )

resume_service = ResumeService()
