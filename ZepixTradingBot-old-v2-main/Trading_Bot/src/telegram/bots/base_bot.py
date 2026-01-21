"""
Base Independent Bot - Abstract Base Class for V6 Telegram Architecture
Version: 3.0.0
Date: 2026-01-20

Uses python-telegram-bot v20+ (Async)
"""

import logging
import asyncio
from typing import Optional, Dict, Any
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler

logger = logging.getLogger(__name__)

class BaseIndependentBot:
    """
    Abstract base class for independent Telegram bots (Controller, Notification, Analytics).
    Wraps python-telegram-bot Application instance.
    """
    
    def __init__(self, token: str, bot_type: str):
        """
        Initialize base bot.
        
        Args:
            token: Telegram bot token
            bot_type: Type of bot (Controller, Notification, Analytics)
        """
        if not token:
            raise ValueError(f"Token required for {bot_type}")
            
        self.token = token
        self.bot_type = bot_type
        self.app: Optional[Application] = None
        self.bot: Optional[Bot] = None
        self.is_active = False
        self._user_id = None  # Self bot ID
        
    async def initialize(self):
        """Initialize the Application and Bot instance"""
        try:
            logger.info(f"[{self.bot_type}] Initializing...")
            self.app = ApplicationBuilder().token(self.token).build()
            self.bot = self.app.bot
            
            await self.app.initialize()
            
            # Verify token and get bot details
            me = await self.bot.get_me()
            self._user_id = me.id
            self.is_active = True
            
            logger.info(f"[{self.bot_type}] Initialized as @{me.username} (ID: {me.id})")
            
            # Register common handlers
            self._register_handlers()
            
            # Start application
            await self.app.start()
            
        except Exception as e:
            logger.error(f"[{self.bot_type}] Initialization failed: {e}")
            self.is_active = False
            raise
            
    async def stop(self):
        """Stop the application"""
        if self.app and self.is_active:
            logger.info(f"[{self.bot_type}] Stopping...")
            await self.app.stop()
            await self.app.shutdown()
            self.is_active = False
            
    async def start_polling(self):
        """Start polling for updates"""
        if self.app and self.is_active:
            logger.info(f"[{self.bot_type}] Starting polling...")
            await self.app.updater.start_polling()
            
    def _register_handlers(self):
        """Register default handlers - Override in subclasses"""
        if self.app:
            self.app.add_handler(CommandHandler("ping", self._ping_handler))
            
    async def _ping_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Default ping handler"""
        await update.message.reply_text(f"🏓 Pong! I am the **{self.bot_type}**.")

    async def broadcast_message(self, chat_id: str, text: str, parse_mode: str = "HTML", **kwargs):
        """Send message (wrapper for consistency)"""
        if not self.is_active or not self.bot:
            logger.warning(f"[{self.bot_type}] Bot not active, cannot send message")
            return
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                **kwargs
            )
        except Exception as e:
            logger.error(f"[{self.bot_type}] Send Error: {e}")
