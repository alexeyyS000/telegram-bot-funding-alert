from aiogram import BaseMiddleware
from services.user import get_user_service
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable


class PreMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        with get_user_service() as user:
            user = user.get_one_or_none(event.from_user.id)
        data["user"] = user
        return await handler(event, data)
