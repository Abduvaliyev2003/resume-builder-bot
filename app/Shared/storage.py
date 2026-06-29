from typing import Dict, Optional


class TokenStorage:
    """In-memory Telegram user token storage."""

    def __init__(self) -> None:
        """Initialize an empty token map."""

        self._tokens: Dict[int, str] = {}

    def set_token(
        self,
        telegram_id: int,
        token: str,
    ) -> None:
        """Store a Laravel access token by Telegram user id."""

        self._tokens[telegram_id] = token

    def get_token(
        self,
        telegram_id: int,
    ) -> Optional[str]:
        """Return a stored token for a Telegram user."""

        return self._tokens.get(telegram_id)

    def get(
        self,
        telegram_id: int,
    ) -> Optional[str]:
        """Compatibility alias for existing handlers."""

        return self.get_token(telegram_id)

    def remove_token(
        self,
        telegram_id: int,
    ) -> None:
        """Remove the stored token for a Telegram user."""

        self._tokens.pop(telegram_id, None)

    def is_authenticated(
        self,
        telegram_id: int,
    ) -> bool:
        """Check whether a Telegram user has an access token."""

        return telegram_id in self._tokens


token_storage = TokenStorage()
