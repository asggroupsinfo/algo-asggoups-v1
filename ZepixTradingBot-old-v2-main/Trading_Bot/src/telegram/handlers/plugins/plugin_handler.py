"""
Plugin Handler - Strategy Management

Implements plugin control: enable, disable, config.

Version: 1.0.0
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class PluginHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "plugins"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_plugins'):
            await self.bot.handle_plugins(update, context)
