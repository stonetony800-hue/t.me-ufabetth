import os
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ============================================================
# CONFIGURATION
# ============================================================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8080"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# CHECK BOT TOKEN
# ============================================================

if not TOKEN:
    logger.error("BOT_TOKEN is NOT available in the environment.")
    raise ValueError(
        "BOT_TOKEN environment variable is missing. "
        "Add BOT_TOKEN to your Railway service Variables."
    )

# Do NOT print the actual token.
logger.info("BOT_TOKEN is available.")


# ============================================================
# TELEGRAM BOT
# ============================================================

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ============================================================
# MAIN KEYBOARD
# ============================================================

def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Information",
                    callback_data="information"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    text="💬 Support",
                    callback_data="support"
                )
            ]
        ]
    )


# ============================================================
# /START
# ============================================================

@dp.message(Command("start"))
async def start_handler(message: types.Message):

    text = (
        "Welcome! 👋\n\n"
        "This bot provides useful information and quick assistance.\n\n"
        "Choose an option below to get started."
    )

    await message.answer(
        text,
        reply_markup=main_keyboard()
    )


# ============================================================
# /HELP
# ============================================================

@dp.message(Command("help"))
async def help_handler(message: types.Message):

    text = (
        "Available commands:\n\n"
        "/start - Open the main menu\n"
        "/help - View available commands\n"
        "/info - Get information\n"
        "/support - Contact support"
    )

    await message.answer(text)


# ============================================================
# /INFO
# ============================================================

@dp.message(Command("info"))
async def info_handler(message: types.Message):

    text = (
        "📚 Information\n\n"
        "Use the menu to explore the available features "
        "and information provided by this bot."
    )

    await message.answer(
        text,
        reply_markup=main_keyboard()
    )


# ============================================================
# /SUPPORT
# ============================================================

@dp.message(Command("support"))
async def support_handler(message: types.Message):

    await message.answer(
        "💬 Support\n\n"
        "If you need assistance, please describe your question "
        "and our support team will respond."
    )


# ============================================================
# INFORMATION BUTTON
# ============================================================

@dp.callback_query(lambda callback: callback.data == "information")
async def information_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "📚 Information\n\n"
        "Here you can provide your users with useful "
        "information about your service or project.",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# ============================================================
# HELP BUTTON
# ============================================================

@dp.callback_query(lambda callback: callback.data == "help")
async def help_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "❓ Help\n\n"
        "/start - Main menu\n"
        "/info - Information\n"
        "/support - Support",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# ============================================================
# SUPPORT BUTTON
# ============================================================

@dp.callback_query(lambda callback: callback.data == "support")
async def support_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "💬 Support\n\n"
        "Send your question here and we'll help you.",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# ============================================================
# NORMAL TEXT MESSAGES
# ============================================================

@dp.message()
async def text_handler(message: types.Message):

    await message.answer(
        "Thanks for your message.\n\n"
        "Use /start to open the main menu or /help "
        "to see the available commands."
    )


# ============================================================
# RAILWAY HEALTH SERVER
# ============================================================

async def health(request):
    return web.Response(text="Bot is running")


async def start_web_server():

    app = web.Application()

    # Railway health endpoint
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=PORT
    )

    await site.start()

    logger.info(f"Health server running on port {PORT}")


# ============================================================
# MAIN
# ============================================================

async def main():

    # Start Railway web server
    await start_web_server()

    # Remove any existing Telegram webhook.
    # This allows polling to work correctly.
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Telegram bot starting...")
    logger.info("Polling started.")

    # Start Telegram polling
    await dp.start_polling(bot)


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
