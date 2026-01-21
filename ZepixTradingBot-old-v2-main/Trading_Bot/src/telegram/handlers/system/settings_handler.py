"""
Settings Handler - System Config

Implements general settings.

Version: 1.0.0
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class SettingsHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "settings"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'show_settings_menu'):
            await self.bot.show_settings_menu(update.effective_chat.id)
        elif hasattr(self.bot, 'handle_settings'):
            await self.bot.handle_settings(update, context)
