# flake8: noqa: F811
import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.variable import dp
from .keyboards import (
    user_keyboard_chenel_application,
    user_keyboard_unsubscribe_or_subscribe,
)
from services.user import get_user_service
from aiogram import F
from bot.states import ClientState
from decorators import check_not_banned_subscriber_user
from services.exceptions import *


@dp.message(ClientState.birth_date, F.text == "/start")
@check_not_banned_subscriber_user
async def echo_send(message: types.Message):
    await message.answer(
        text="unsubscribe or subscribe to alerts",
        reply_markup=user_keyboard_unsubscribe_or_subscribe(),
    )


@dp.message(F.text == "/start")
async def echo_send(message: types.Message, state: FSMContext):
    await message.answer(
        text="inter enter your full name",
        reply_markup=user_keyboard_chenel_application(),
    )

    await state.set_state(ClientState.start)


@dp.message(ClientState.start)
async def echo_send(message: types.Message, state: FSMContext):
    if message.text == "cancel of registration":
        await state.clear()
        return 1
    elif len(message.text.split()) != 3:
        await message.answer(text="incorrect try again")
        await state.set_state(ClientState.start)
    else:
        await message.answer(text="Enter your date of birth in the format DD/MM/YYYY")
        await state.update_data(name=message.text)
        await state.set_state(ClientState.full_name)


@dp.message(ClientState.full_name)
async def echo_send(message: types.Message, state: FSMContext):
    if message.text == "cancel of registration":
        await state.clear()
        return 1
    try:
        date_of_birth = datetime.datetime.strptime(message.text, "%d/%m/%Y")
    except:
        await message.answer(text="incorrect try again")
        await state.set_state(ClientState.full_name)
        return 1
    await message.answer(text="registration completed wait")
    await state.update_data(date=str(date_of_birth))
    user_data = await state.get_data()
    user_model = {
        "id": message.from_user.id,
        "birth_date": user_data["date"],
        "full_name": user_data["name"],
        "pending": True,
    }
    with get_user_service() as user:
        user.create(**user_model)
    await state.set_state(ClientState.birth_date)


@dp.message(F.text == "cancel of registration")
async def echo_send(message: types.Message, state: FSMContext):
    with get_user_service() as user:
        user.refusal(message.from_user.id)
    await state.clear()
    await message.answer(text="done")


@dp.message(F.text == "/unsubscribe")
@check_not_banned_subscriber_user
async def echo_send(message: types.Message):
    try:
        with get_user_service() as user:
            user.unsubscribe(message.from_user.id)
    except AlreadyUnSubscribed:
        await message.answer(
            text="already unsubscribed",
            reply_markup=user_keyboard_unsubscribe_or_subscribe(),
        )
        return 1
    await message.answer(
        text="unsubscribed", reply_markup=user_keyboard_unsubscribe_or_subscribe()
    )


@dp.message(F.text == "/subscribe")
@check_not_banned_subscriber_user
async def echo_send(message: types.Message):
    try:
        with get_user_service() as user:
            user.subscribe(message.from_user.id)
    except AlreadySubscribed:
        await message.answer(
            text="already subscribed",
            reply_markup=user_keyboard_unsubscribe_or_subscribe(),
        )
        return 1
    await message.answer(
        text="subscribed", reply_markup=user_keyboard_unsubscribe_or_subscribe()
    )
