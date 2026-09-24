import os
import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# ============================================================
# CONFIGURATION
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY", "")
PORT = int(os.getenv("PORT", "8080"))


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# ENVIRONMENT CHECK
# ============================================================

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. "
        "Add BOT_TOKEN to Railway Variables."
    )

logger.info("BOT_TOKEN loaded successfully.")

if AI_API_KEY:
    logger.info("AI_API_KEY loaded successfully.")
else:
    logger.info(
        "AI_API_KEY is not configured. "
        "AI responses will use demo mode."
    )


# ============================================================
# TELEGRAM
# ============================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖 AI Tools",
                    callback_data="tools"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ About",
                    callback_data="about"
                ),
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔐 Privacy",
                    callback_data="privacy"
                )
            ]
        ]
    )


# ============================================================
# AI TOOLS MENU
# ============================================================

def tools_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 AI Chat",
                    callback_data="ai_chat"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Summarize",
                    callback_data="summarize"
                ),
                InlineKeyboardButton(
                    text="✨ Improve Text",
                    callback_data="improve"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Translate",
                    callback_data="translate"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Main Menu",
                    callback_data="main"
                )
            ]
        ]
    )


# ============================================================
# /START
# ============================================================

@dp.message(Command("start"))
async def start_command(message: types.Message):

    text = (
        "👋 Welcome to AI Tools!\n\n"
        "A simple collection of AI-powered tools "
        "for writing, summarizing, translation and "
        "general assistance.\n\n"
        "Choose a tool below to get started."
    )

    await message.answer(
        text,
        reply_markup=main_menu()
    )


# ============================================================
# /HELP
# ============================================================

@dp.message(Command("help"))
async def help_command(message: types.Message):

    text = (
        "❓ Help\n\n"
        "Available commands:\n\n"
        "/start - Open the main menu\n"
        "/tools - View AI tools\n"
        "/about - About this bot\n"
        "/privacy - Privacy information\n"
        "/help - Show this help message\n\n"
        "You can also use the buttons in the menu."
    )

    await message.answer(text)


# ============================================================
# /TOOLS
# ============================================================

@dp.message(Command("tools"))
async def tools_command(message: types.Message):

    await message.answer(
        "🤖 AI Tools\n\n"
        "Choose a tool:",
        reply_markup=tools_menu()
    )


# ============================================================
# /ABOUT
# ============================================================

@dp.message(Command("about"))
async def about_command(message: types.Message):

    text = (
        "ℹ️ About AI Tools\n\n"
        "This bot provides user-requested AI assistance "
        "through a simple Telegram interface.\n\n"
        "The bot does not send unsolicited messages. "
        "Users initiate interactions themselves.\n\n"
        "AI responses may occasionally contain mistakes, "
        "so important information should be independently verified."
    )

    await message.answer(text)


# ============================================================
# /PRIVACY
# ============================================================

@dp.message(Command("privacy"))
async def privacy_command(message: types.Message):

    text = (
        "🔐 Privacy\n\n"
        "This bot is designed to process messages only "
        "for the purpose of providing the requested service.\n\n"
        "Do not send passwords, authentication codes, "
        "financial information or other sensitive information "
        "to the bot.\n\n"
        "The bot does not ask for your Telegram password "
        "or Telegram login code."
    )

    await message.answer(text)


# ============================================================
# MAIN MENU BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "main")
async def main_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "🏠 Main Menu\n\n"
        "Choose an option:",
        reply_markup=main_menu()
    )

    await callback.answer()


# ============================================================
# TOOLS BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "tools")
async def tools_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "🤖 AI Tools\n\n"
        "Choose a tool:",
        reply_markup=tools_menu()
    )

    await callback.answer()


# ============================================================
# ABOUT BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "about")
async def about_callback(callback: types.CallbackQuery):

    text = (
        "ℹ️ About AI Tools\n\n"
        "This bot provides user-requested AI assistance "
        "through Telegram.\n\n"
        "It is designed for writing, summarization, "
        "translation and general AI assistance."
    )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu()
    )

    await callback.answer()


# ============================================================
# HELP BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: types.CallbackQuery):

    text = (
        "❓ Help\n\n"
        "/start - Main menu\n"
        "/tools - AI tools\n"
        "/about - About the bot\n"
        "/privacy - Privacy information\n\n"
        "Choose an AI tool from the Tools menu."
    )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu()
    )

    await callback.answer()


# ============================================================
# PRIVACY BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "privacy")
async def privacy_callback(callback: types.CallbackQuery):

    text = (
        "🔐 Privacy\n\n"
        "Use this bot only for information and content "
        "you are comfortable sharing with the service.\n\n"
        "Never send passwords, OTPs, private keys or "
        "other sensitive credentials."
    )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu()
    )

    await callback.answer()


# ============================================================
# AI CHAT BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "ai_chat")
async def ai_chat_callback(callback: types.CallbackQuery):

    text = (
        "💬 AI Chat\n\n"
        "Send me a message and I will process it as "
        "an AI assistance request.\n\n"
        "Example:\n"
        "Write a professional email asking for a meeting."
    )

    await callback.message.edit_text(
        text,
        reply_markup=tools_menu()
    )

    await callback.answer()


# ============================================================
# SUMMARIZE BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "summarize")
async def summarize_callback(callback: types.CallbackQuery):

    text = (
        "📝 Summarize\n\n"
        "Send me the text you want summarized.\n\n"
        "Example:\n"
        "Paste an article, document or message here "
        "and I will create a concise summary."
    )

    await callback.message.edit_text(
        text,
        reply_markup=tools_menu()
    )

    await callback.answer()


# ============================================================
# IMPROVE TEXT BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "improve")
async def improve_callback(callback: types.CallbackQuery):

    text = (
        "✨ Improve Text\n\n"
        "Send me your text and tell me what you want "
        "to improve.\n\n"
        "For example:\n"
        "• Grammar\n"
        "• Clarity\n"
        "• Professional tone\n"
        "• Simpler wording"
    )

    await callback.message.edit_text(
        text,
        reply_markup=tools_menu()
    )

    await callback.answer()


# ============================================================
# TRANSLATE BUTTON
# ============================================================

@dp.callback_query(lambda c: c.data == "translate")
async def translate_callback(callback: types.CallbackQuery):

    text = (
        "🌍 Translate\n\n"
        "Send the text you want translated and include "
        "the target language.\n\n"
        "Example:\n"
        "Translate this to French: Hello, how are you?"
    )

    await callback.message.edit_text(
        text,
        reply_markup=tools_menu()
    )

    await callback.answer()


# ============================================================
# NORMAL TEXT MESSAGE
# ============================================================

@dp.message()
async def text_handler(message: types.Message):

    user_text = message.text

    if not user_text:
        await message.answer(
            "Please send a text message or use /start."
        )
        return

    # --------------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------------

    if not AI_API_KEY:

        await message.answer(
            "🤖 AI Tools\n\n"
            "I received your request.\n\n"
            "The AI provider is not configured yet. "
            "Add your AI provider API key as the "
            "AI_API_KEY Railway variable to enable "
            "real AI responses."
        )

        return

    # --------------------------------------------------------
    # AI PROVIDER INTEGRATION
    # --------------------------------------------------------
    #
    # Put your approved AI provider integration here.
    #
    # Keep the API key in Railway:
    #
    # AI_API_KEY=your_key
    #
    # Never put the key directly into this file.
    #

    await message.answer(
        "🤖 Your AI request was received.\n\n"
        "The AI provider connection can now be "
        "added to this bot."
    )


# ============================================================
# RAILWAY HEALTH CHECK
# ============================================================

async def health(request):

    return web.Response(
        text="AI Tools Bot is running",
        status=200
    )


async def start_web_server():

    app = web.Application()

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

    logger.info(
        f"Health server started on port {PORT}"
    )


# ============================================================
# MAIN
# ============================================================

async def main():

    logger.info("Starting AI Tools Bot...")

    # Start Railway health server
    await start_web_server()

    # Make sure no old webhook is active.
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    logger.info("Telegram webhook removed.")

    # Start polling
    logger.info("Starting Telegram polling...")

    await dp.start_polling(bot)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info(
            "AI Tools Bot stopped."
        )
