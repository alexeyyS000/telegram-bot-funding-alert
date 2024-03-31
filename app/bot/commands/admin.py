# flake8: noqa: F811
from aiogram import types
from bot.variable import dp
from .keyboards import actions_keyboard, pagination_keyboard
from services.user import get_user_service
from bot.decorators import check_admin
from services.exceptions import *


def get_id(callback_query_data):
    id = int(callback_query_data.split("#")[1])
    return id


def get_page(callback_query_data):
    page = int(callback_query_data.split("#")[2])
    return page


@dp.callback_query(lambda c: c.data.startswith("add"))
async def handler(callback_query: types.CallbackQuery):
    id = get_id(callback_query.data)
    try:
        with get_user_service() as user:
            user.add(id)
        await callback_query.answer(text=f"id {id} added")
    except AlreadyAdded:
        await callback_query.answer(text=f"id {id} already added")


@dp.callback_query(lambda c: c.data.startswith("ban"))
async def handler(callback_query: types.CallbackQuery):
    id = get_id(callback_query.data)
    try:
        with get_user_service() as user:
            user.ban(id)
        await callback_query.answer(text=f"id {id} banned")
    except AlreadyBanned:
        await callback_query.answer(text=f"id {id} already banned")


@dp.callback_query(lambda c: c.data.startswith("refusal"))
async def handler(callback_query: types.CallbackQuery):
    id = get_id(callback_query.data)
    try:
        with get_user_service() as user:
            user.refusal(id)
        await callback_query.answer(text=f"id {id} refusaled")
    except AlreadyRefusaled:
        await callback_query.answer(
            text=f"id {id} already refusaled"
        )  # тоже не знаю как избедать дублирования кода тут


@dp.callback_query(lambda c: c.data.startswith("make_admin"))
async def handler(callback_query: types.CallbackQuery):
    id = get_id(callback_query.data)
    try:
        with get_user_service() as user:
            user.make_admin(id)
        await callback_query.answer(text=f"id {id} admin")
    except AlreadyAdmin:
        await callback_query.answer(text=f"id {id} already admin")


@dp.message(lambda message: message.text == "/adminboard")
@check_admin
async def handler(message: types.Message):
    with get_user_service() as user:
        user_data = user.get_pagination()
    keyboard = pagination_keyboard(
        user_data["current_page"],
        user_data["prev_page"],
        user_data["next_page"],
        user_data["total_pages"],
        user_data["result"],
    )
    await message.answer(text="adminboard", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("page"))
async def handler(callback_query: types.CallbackQuery = None):
    page = callback_query.data.split("#")[1]

    # user_data = UserDAL(session).fetch(3, page)
    with get_user_service() as user:
        user_data = user.get_pagination(page)
    keyboard = pagination_keyboard(
        user_data["current_page"],
        user_data["prev_page"],
        user_data["next_page"],
        user_data["total_pages"],
        user_data["result"],
    )
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("id"))
async def handler(callback_query: types.CallbackQuery = None):
    id = get_id(callback_query.data)
    page = get_page(callback_query.data)
    await callback_query.message.edit_reply_markup(
        reply_markup=actions_keyboard(id, page)
    )
