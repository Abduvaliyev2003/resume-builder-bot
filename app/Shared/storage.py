from typing import Dict, Optional


class TokenStorage:


    def __init__(self):
        self._tokens: Dict[int, str] = {}

    def set_token(
        self,
        telegram_id: int,
        token: str,
    ) -> None:
        self._tokens[telegram_id] = token

    def get_token(
        self,
        telegram_id: int,
    ) -> Optional[str]:
        return self._tokens.get(telegram_id)

    def remove_token(
        self,
        telegram_id: int,
    ) -> None:
        self._tokens.pop(telegram_id, None)

    def is_authenticated(
        self,
        telegram_id: int,
    ) -> bool:
        return telegram_id in self._tokens


token_storage = TokenStorage()