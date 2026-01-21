"""
Analytics Handler - Performance & Reporting

Implements all analytics commands: daily, weekly, compare, export.

Version: 1.1.0 (Logic Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

import telegram as python_telegram_bot
from telegram import Update as TelegramUpdate
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class AnalyticsHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "analytics"

    async def execute(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_analytics_menu'):
            await self.bot.handle_analytics_menu(TelegramUpdate, context)

    async def handle_daily(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_daily'):
            await self.bot.handle_daily(TelegramUpdate, context)

    async def handle_weekly(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_weekly'):
            await self.bot.handle_weekly(TelegramUpdate, context)

    async def handle_compare(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_compare'):
            await self.bot.handle_compare(TelegramUpdate, context)

    async def handle_export(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_export'):
            await self.bot.handle_export(TelegramUpdate, context)



