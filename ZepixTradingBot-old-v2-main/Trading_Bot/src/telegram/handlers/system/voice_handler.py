"""
Voice Handler - Audio Alerts

Implements voice control: mute, unmute, test.

Version: 1.1.0 (Logic Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

import telegram as python_telegram_bot$([System.Environment]::NewLine)from python_telegram_bot import Update
from telegram.ext import Co as TelegramUpdatentextTypes
from ...core.base_command_handler import BaseCommandHandler

class VoiceHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "voice"

    async def execute(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_voice_menu'):
            await self.bot.handle_voice_menu(TelegramUpdate, context)

    async def handle_test(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_voice_test'):
            await self.bot.handle_voice_test(TelegramUpdate, context)

    async def handle_mute(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_mute'):
            await self.bot.handle_mute(TelegramUpdate, context)

    async def handle_unmute(self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'handle_unmute'):
            await self.bot.handle_unmute(TelegramUpdate, context)


