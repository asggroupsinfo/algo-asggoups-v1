"""
Message Router - Intelligent Message Routing for V6 Architecture
Version: 3.0.0
Date: 2026-01-20

Routes messages to the appropriate specialized bot.
"""

import logging
import asyncio
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class MessageRouter:
    """
    Routes messages to specific bots based on intent.
    - Commands -> Controller Bot
    - Alerts -> Notification Bot
    - Reports -> Analytics Bot
    """
    
    def __init__(self, controller_bot, notification_bot, analytics_bot):
        self.controller = controller_bot
        self.notification = notification_bot
        self.analytics = analytics_bot
        
    async def route_command_response(self, chat_id: str, text: str):
        """Send response via Controller"""
        if self.controller and self.controller.is_active:
            await self.controller.broadcast_message(chat_id, text)
        else:
            logger.warning("Controller bot inactive, cannot send response")

    async def route_alert(self, message: str, chat_id: str = None):
        """Route trade alert to Notification Bot"""
        if self.notification and self.notification.is_active:
            await self.notification.send_alert(message, chat_id)
        elif self.controller and self.controller.is_active:
            # Fallback to controller if notification bot is down
            await self.controller.broadcast_message(chat_id, f"🔔 {message}")
            
    async def route_report(self, message: str, chat_id: str):
        """Route report to Analytics Bot"""
        if self.analytics and self.analytics.is_active:
            await self.analytics.broadcast_message(chat_id, message)
        elif self.controller and self.controller.is_active:
            # Fallback
            await self.controller.broadcast_message(chat_id, message)
