"""
Admin Error Notification System

Sends formatted error alerts to admin for critical issues.
Based on: Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from .error_codes import *
from .error_handlers import error_rate_limiter

logger = logging.getLogger(__name__)


class AdminErrorNotifier:
    """
    Sends error notifications to admin
    """
    
    def __init__(self, telegram_bot, admin_chat_id: Optional[int] = None):
        """
        Initialize admin notifier
        
        Args:
            telegram_bot: Telegram bot instance
            admin_chat_id: Admin chat ID for notifications
        """
        self.telegram_bot = telegram_bot
        self.admin_chat_id = admin_chat_id
        self.enabled = admin_chat_id is not None
        
        if self.enabled:
            logger.info(f"AdminErrorNotifier initialized for chat {admin_chat_id}")
        else:
            logger.warning("AdminErrorNotifier disabled - no admin_chat_id configured")
    
    async def notify_error(self, error_code: str, error_msg: str, severity: str, context: Dict = None):
        """
        Send error notification to admin
        
        Args:
            error_code: Error code (e.g., TG-001)
            error_msg: Error message
            severity: Error severity level
            context: Additional context dict
        """
        if not self.enabled:
            logger.debug(f"Admin notification skipped - not enabled: {error_code}")
            return
        
        # Check rate limit
        if not error_rate_limiter.should_notify(error_code):
            logger.debug(f"Admin notification rate limited: {error_code}")
            return
        
        try:
            # Format message
            emoji = SEVERITY_EMOJI.get(severity, "⚪")
            
            message = (
                f"🚨 <b>ADMIN ALERT</b> 🚨\n\n"
                f"{emoji} <b>Severity:</b> {severity}\n"
                f"<b>Code:</b> <code>{error_code}</code>\n"
                f"<b>Message:</b> {error_msg}\n"
                f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            # Add human-readable description
            if error_code in ERROR_MESSAGES:
                message += f"\n\n<b>Description:</b>\n{ERROR_MESSAGES[error_code]}"
            
            # Add context if provided
            if context:
                message += "\n\n<b>Context:</b>"
                for key, value in context.items():
                    message += f"\n• <code>{key}:</code> {value}"
            
            # Add recovery status
            if AUTO_RECOVERY_ENABLED.get(error_code, False):
                message += "\n\n✅ <i>Auto-recovery is enabled for this error</i>"
            else:
                message += "\n\n⚠️ <i>Manual intervention required</i>"
            
            # Send notification
            await self._send_to_admin(message)
            logger.info(f"Admin notification sent: {error_code}")
            
        except Exception as e:
            logger.error(f"Error sending admin notification: {e}")
    
    async def notify_recovery_success(self, error_code: str, message: str):
        """
        Notify admin of successful recovery
        
        Args:
            error_code: Error code that was recovered
            message: Recovery message
        """
        if not self.enabled:
            return
        
        try:
            notification = (
                f"✅ <b>RECOVERY SUCCESS</b>\n\n"
                f"<b>Code:</b> <code>{error_code}</code>\n"
                f"<b>Message:</b> {message}\n"
                f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            await self._send_to_admin(notification)
            logger.info(f"Recovery notification sent: {error_code}")
            
        except Exception as e:
            logger.error(f"Error sending recovery notification: {e}")
    
    async def notify_recovery_failure(self, error_code: str, message: str, attempts: int):
        """
        Notify admin of failed recovery
        
        Args:
            error_code: Error code that failed recovery
            message: Failure message
            attempts: Number of attempts made
        """
        if not self.enabled:
            return
        
        try:
            notification = (
                f"❌ <b>RECOVERY FAILED</b>\n\n"
                f"<b>Code:</b> <code>{error_code}</code>\n"
                f"<b>Message:</b> {message}\n"
                f"<b>Attempts:</b> {attempts}\n"
                f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"⚠️ <i>Manual intervention required</i>"
            )
            
            await self._send_to_admin(notification)
            logger.warning(f"Recovery failure notification sent: {error_code}")
            
        except Exception as e:
            logger.error(f"Error sending recovery failure notification: {e}")
    
    async def notify_critical_system_error(self, component: str, error_msg: str):
        """
        Notify admin of critical system error
        
        Args:
            component: System component (e.g., "MT5", "Database", "Telegram")
            error_msg: Error message
        """
        if not self.enabled:
            return
        
        try:
            notification = (
                f"🔴 <b>CRITICAL SYSTEM ERROR</b> 🔴\n\n"
                f"<b>Component:</b> {component}\n"
                f"<b>Error:</b> {error_msg}\n"
                f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"⚠️ <b>Immediate action required!</b>"
            )
            
            await self._send_to_admin(notification)
            logger.critical(f"Critical system error notification sent: {component}")
            
        except Exception as e:
            logger.error(f"Error sending critical notification: {e}")
    
    async def _send_to_admin(self, message: str):
        """
        Send message to admin chat
        
        Args:
            message: Message to send
        """
        try:
            if hasattr(self.telegram_bot, 'send_message'):
                await self.telegram_bot.send_message(
                    chat_id=self.admin_chat_id,
                    text=message,
                    parse_mode='HTML'
                )
            else:
                logger.warning("Telegram bot missing send_message method")
        except Exception as e:
            logger.error(f"Error sending to admin: {e}")


# Global instance (initialized in main)
admin_error_notifier = None


def initialize_admin_notifier(telegram_bot, admin_chat_id: Optional[int] = None):
    """
    Initialize global admin notifier
    
    Args:
        telegram_bot: Telegram bot instance
        admin_chat_id: Admin chat ID
    
    Returns:
        AdminErrorNotifier instance
    """
    global admin_error_notifier
    admin_error_notifier = AdminErrorNotifier(telegram_bot, admin_chat_id)
    return admin_error_notifier
