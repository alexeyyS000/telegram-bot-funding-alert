from aiogram import Bot, Dispatcher
from .config import AdminSettings
from aiogram.fsm.storage.redis import RedisStorage

bot = Bot(token=AdminSettings().bot_token)

dp = Dispatcher(storage=RedisStorage.from_url(AdminSettings().redis_url))
