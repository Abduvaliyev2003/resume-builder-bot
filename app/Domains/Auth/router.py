from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Domains.Auth.keyboards import auth_keyboard
from app.Domains.Auth.service import auth_service
from app.Domains.Auth.states import LoginState
from app.Shared.callbacks import AuthCallback
from app.Shared.enums import AuthAction

router = Router(name="auth")


@router.message(CommandStart())
async def start(message: Message) -> None:
    """
    Start command.
    """

    await message.answer(
        text=(
            "👋 <b>Welcome!</b>\n\n"
            "Resume Builder Bot\n\n"
            "Please login or create a new account."
        ),
        reply_markup=auth_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(
    AuthCallback.filter(
        F.action == AuthAction.LOGIN,
    )
)
async def login(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: AuthCallback,
) -> None:
    """
    Start login process.
    """

    await state.set_state(LoginState.email)

    await callback.message.edit_text(
        "📧 Enter your email:"
    )

    await callback.answer()


@router.message(LoginState.email)
async def login_email(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Save email.
    """

    await state.update_data(
        email=message.text.strip(),
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
) -> None:
    """
    Login user.
    """

    data = await state.get_data()

    response = await auth_service.login(
        email=data["email"],
        password=message.text,
    )

    # Laravel Sanctum token
    token = response["token"]

    # User data
    user = response["user"]

    # Temporary token storage
    await state.update_data(
        token=token,
        user=user,
    )

    await state.clear()

    await message.answer(
        (
            "✅ <b>Login successful!</b>\n\n"
            f"Welcome, <b>{user['name']}</b> 🎉"
        ),
        parse_mode="HTML",
    )