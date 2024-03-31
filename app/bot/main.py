from aiogram import Bot
from commands import dp
from middleware import PreMessageMiddleware
import asyncio
from aiogram.methods.delete_webhook import DeleteWebhook
from config import AdminSettings

bot = Bot(token=AdminSettings().bot_token)


async def main():
    dp.message.outer_middleware(PreMessageMiddleware())
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
