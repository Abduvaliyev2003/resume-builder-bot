from __future__ import annotations

from typing import Any

import httpx

from app.Shared.config import settings
from app.Shared.logger import logger


class APIError(Exception):
    """Raised when the Laravel API request fails."""


class APIClient:
    """Async Laravel REST API client used by domain services only."""

    def __init__(self) -> None:
        """Initialize the reusable HTTP client."""

        self._client = httpx.AsyncClient(
            base_url=settings.API_URL,
            timeout=settings.REQUEST_TIMEOUT,
        )

    async def get(
        self,
        url: str,
        *,
        token: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Send a GET request to the Laravel API."""

        return await self._request(
            "GET",
            url,
            token=token,
            params=params,
        )

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        *,
        token: str | None = None,
    ) -> Any:
        """Send a POST request to the Laravel API."""

        return await self._request(
            "POST",
            url,
            token=token,
            json=data,
        )

    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        *,
        token: str | None = None,
    ) -> Any:
        """Send a PUT request to the Laravel API."""

        return await self._request(
            "PUT",
            url,
            token=token,
            json=data,
        )

    async def delete(
        self,
        url: str,
        *,
        token: str | None = None,
    ) -> Any:
        """Send a DELETE request to the Laravel API."""

        return await self._request(
            "DELETE",
            url,
            token=token,
        )

    async def get_bytes(
        self,
        url: str,
        *,
        token: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> tuple[bytes, str | None]:
        """Send a GET request and return raw response bytes."""

        headers = self._auth_headers(token)

        try:
            response = await self._client.request(
                "GET",
                url,
                headers=headers,
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "Laravel API returned {} for GET {}",
                exc.response.status_code,
                url,
            )
            raise APIError(self._error_message(exc.response)) from exc
        except httpx.HTTPError as exc:
            logger.error("Laravel API bytes request failed for GET {}: {}", url, exc)
            raise APIError("API service is temporarily unavailable.") from exc

        return response.content, response.headers.get("content-type")

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""

        await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        *,
        token: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Execute a request and normalize API failures."""

        headers = self._auth_headers(token)

        try:
            response = await self._client.request(
                method,
                url,
                headers=headers,
                **kwargs,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "Laravel API returned {} for {} {}",
                exc.response.status_code,
                method,
                url,
            )
            raise APIError(self._error_message(exc.response)) from exc
        except httpx.HTTPError as exc:
            logger.error(
                "Laravel API request failed for {} {}: {}",
                method,
                url,
                exc,
            )
            raise APIError("API service is temporarily unavailable.") from exc

        if response.status_code == httpx.codes.NO_CONTENT:
            return {}

        try:
            return response.json()
        except ValueError as exc:
            logger.error("Laravel API returned invalid JSON for {} {}", method, url)
            raise APIError("API returned an invalid response.") from exc

    @staticmethod
    def _auth_headers(token: str | None) -> dict[str, str]:
        """Build bearer-token headers when the user is authenticated."""

        headers = {
            "Accept": "application/json",
        }

        if not token:
            return headers

        headers["Authorization"] = f"Bearer {token}"

        return headers

    @staticmethod
    def _error_message(response: httpx.Response) -> str:
        """Extract the best user-safe error message from Laravel JSON."""

        try:
            payload = response.json()
        except ValueError:
            return "API request failed."

        if isinstance(payload, dict):
            message = payload.get("message")
            if isinstance(message, str):
                return message

            errors = payload.get("errors")

            if isinstance(errors, dict):
                first_error = next(iter(errors.values()), None)

                if isinstance(first_error, list) and first_error:
                    return str(first_error[0])

                if isinstance(first_error, str):
                    return first_error

        return "API request failed."


api = APIClient()
