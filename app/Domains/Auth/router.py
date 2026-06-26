from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.Domains.Auth.keyboards import auth_keyboard
from app.Domains.Auth.states import LoginState

router = Router(name="auth")


@router.message(CommandStart())
async def start(message: Message):

    await message.answer(
        text=(
            "👋 Welcome!\n\n"
            "Resume Builder Bot"
        ),
        reply_markup=auth_keyboard(),
    )

@router.callback_query(F.data == "login")
async def login(callback: CallbackQuery, state: FSMContext):

    await state.set_state(LoginState.email)

    await callback.message.answer(
        "📧 Enter your email:"
    )

    await callback.answer()

@router.message(LoginState.email)
async def login_email(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        email=message.text,
    )

    await state.set_state(
        LoginState.password,
    )

    await message.answer(
        "🔑 Enter your password:"
    )


@router.message(LoginState.password)
async def login_password(
    message: Message,
    state: FSMContext,
):

    data = await state.get_data()

    response = await auth_service.login(
        email=data["email"],
        password=message.text,
    )

    token = response["token"]

    await state.clear()

    await message.answer(
        f"✅ Login successful!\n\nToken:\n{token}"
    )