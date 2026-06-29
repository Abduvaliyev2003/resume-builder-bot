from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Domains.Auth.keyboards import auth_keyboard
from app.Domains.Auth.service import auth_service
from app.Domains.Auth.states import LoginState, RegisterState
from app.Domains.Resume.keyboards import resume_menu_keyboard
from app.Shared.api import APIError
from app.Shared.callbacks import AuthCallback
from app.Shared.enums import AuthAction
from app.Shared.storage import token_storage

router = Router(name="auth")


@router.message(CommandStart())
async def start(message: Message) -> None:
    """
    Start command.
    """

    if token_storage.is_authenticated(message.from_user.id):
        await message.answer(
            text=(
                "👋 <b>Welcome back!</b>\n\n"
                "Choose one of the actions below."
            ),
            reply_markup=resume_menu_keyboard(),
            parse_mode="HTML",
        )
        return

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

    try:
        response = await auth_service.telegram_login(
            email=data["email"],
            password=message.text,
            telegram_id=message.from_user.id,
            telegram_username=message.from_user.username,
            telegram_first_name=message.from_user.first_name,
            telegram_last_name=message.from_user.last_name,
        )
    except APIError as exc:
        await message.answer(f"❌ Login failed: {exc}")
        return

    # Laravel Sanctum token
    token = response["token"]

    # User data
    user = response["user"]

    token_storage.set_token(
        telegram_id=message.from_user.id,
        token=token,
    )

    await state.clear()

    await message.answer(
        (
            "✅ <b>Login successful!</b>\n\n"
            f"Welcome, <b>{user['name']}</b> 🎉\n\n"
            "Choose one of the actions below."
        ),
        reply_markup=resume_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(
    AuthCallback.filter(
        F.action == AuthAction.REGISTER,
    )
)
async def register(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: AuthCallback,
) -> None:
    """Start registration process."""

    await state.set_state(RegisterState.name)

    await callback.message.edit_text(
        "👤 Enter your name:"
    )

    await callback.answer()


@router.message(RegisterState.name)
async def register_name(
    message: Message,
    state: FSMContext,
) -> None:
    """Save registration name."""

    await state.update_data(
        name=message.text.strip(),
    )

    await state.set_state(RegisterState.email)

    await message.answer(
        "📧 Enter your email:"
    )


@router.message(RegisterState.email)
async def register_email(
    message: Message,
    state: FSMContext,
) -> None:
    """Save registration email."""

    await state.update_data(
        email=message.text.strip(),
    )

    await state.set_state(RegisterState.password)

    await message.answer(
        "🔑 Enter your password (minimum 8 characters):"
    )


@router.message(RegisterState.password)
async def register_password(
    message: Message,
    state: FSMContext,
) -> None:
    """Register user and create a Telegram API session."""

    password = message.text

    if len(password) < 8:
        await message.answer(
            "❌ Password must be at least 8 characters. Try again:"
        )
        return

    data = await state.get_data()

    try:
        await auth_service.register(
            name=data["name"],
            email=data["email"],
            password=password,
        )

        response = await auth_service.telegram_login(
            email=data["email"],
            password=password,
            telegram_id=message.from_user.id,
            telegram_username=message.from_user.username,
            telegram_first_name=message.from_user.first_name,
            telegram_last_name=message.from_user.last_name,
        )
    except APIError as exc:
        await message.answer(f"❌ Registration failed: {exc}")
        return

    token_storage.set_token(
        telegram_id=message.from_user.id,
        token=response["token"],
    )

    await state.clear()

    user = response.get("user", {})

    await message.answer(
        (
            "✅ <b>Registration successful!</b>\n\n"
            f"Welcome, <b>{user.get('name', data['name'])}</b> 🎉\n\n"
            "Choose one of the actions below."
        ),
        reply_markup=resume_menu_keyboard(),
        parse_mode="HTML",
    )
