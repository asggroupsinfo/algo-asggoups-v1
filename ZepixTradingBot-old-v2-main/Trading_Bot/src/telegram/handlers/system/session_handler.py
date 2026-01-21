"""
Session Handler - Trading Hours Management

Implements session control: London, New York, etc.

Version: 1.1.0 (Logic Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

import telegram as python_telegram_bot
from telegram import Update as TelegramUpdate
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class SessionHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "session"

    async def execute(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_session_menu'):
            await self.bot.handle_session_menu(TelegramUpdate, context)

    async def handle_london(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_london'):
            await self.bot.handle_london(TelegramUpdate, context)

    async def handle_newyork(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_newyork'):
            await self.bot.handle_newyork(TelegramUpdate, context)

    async def handle_tokyo(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_tokyo'):
            await self.bot.handle_tokyo(TelegramUpdate, context)



