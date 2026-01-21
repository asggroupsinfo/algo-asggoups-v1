"""
Base Telegram Bot - Lightweight base class for specialized bots

Provides basic send/receive functionality without command handlers.
Used by ControllerBot, NotificationBot, and AnalyticsBot.

Version: 1.0.0
Date: 2026-01-14
"""

import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseTelegramBot:
    """
    Lightweight base class for Telegram bots.
    Provides basic message sending without command handling.
    """
    
    def __init__(self, token: str, chat_id: str = None, bot_name: str = "BaseBot"):
        self.token = token
        self.chat_id = chat_id
        self.bot_name = bot_name
        self.base_url = f"https://api.telegram.org/bot{token}" if token else None
        self.session = requests.Session()
        self._is_active = bool(token)
        self._message_count = 0
        self._last_message_time = None
        
        if self._is_active:
            logger.info(f"[{self.bot_name}] Initialized with token")
        else:
            logger.warning(f"[{self.bot_name}] No token provided - bot inactive")
    
    @property
    def is_active(self) -> bool:
        """Check if bot has valid token"""
        return self._is_active
    
    def send_message(
        self,
        text: str,
        chat_id: str = None,
        parse_mode: str = "HTML",
        reply_markup: Dict = None,
        disable_notification: bool = False
    ) -> Optional[int]:
        """
        Send a message via Telegram API
        
        Args:
            text: Message text
            chat_id: Target chat ID (uses default if not provided)
            parse_mode: 'HTML', 'Markdown', or None
            reply_markup: Inline keyboard markup
            disable_notification: Send silently
        
        Returns:
            Message ID if successful, None otherwise
        """
        if not self._is_active:
            logger.warning(f"[{self.bot_name}] Cannot send - bot inactive")
            return None
        
        target_chat = chat_id or self.chat_id
        if not target_chat:
            logger.error(f"[{self.bot_name}] No chat_id provided")
            return None
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": target_chat,
                "text": text,
                "disable_notification": disable_notification
            }
            
            if parse_mode:
                payload["parse_mode"] = parse_mode
            
            if reply_markup:
                payload["reply_markup"] = reply_markup
            
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    self._message_count += 1
                    self._last_message_time = datetime.now()
                    return result.get("result", {}).get("message_id")
            
            if response.status_code == 400 and parse_mode:
                logger.warning(f"[{self.bot_name}] Parse mode error, retrying without formatting")
                payload.pop("parse_mode", None)
                retry_response = self.session.post(url, json=payload, timeout=10)
                if retry_response.status_code == 200:
                    result = retry_response.json()
                    if result.get("ok"):
                        self._message_count += 1
                        self._last_message_time = datetime.now()
                        return result.get("result", {}).get("message_id")
            
            logger.error(f"[{self.bot_name}] Send failed: {response.status_code} - {response.text[:200]}")
            return None
            
        except requests.exceptions.Timeout:
            logger.error(f"[{self.bot_name}] Request timeout")
            return None
        except Exception as e:
            logger.error(f"[{self.bot_name}] Send error: {e}")
            return None
    
    def edit_message(
        self,
        message_id: int,
        text: str,
        chat_id: str = None,
        parse_mode: str = "HTML",
        reply_markup: Dict = None
    ) -> bool:
        """
        Edit an existing message
        
        Args:
            message_id: ID of message to edit
            text: New message text
            chat_id: Target chat ID
            parse_mode: Formatting mode
            reply_markup: New inline keyboard
        
        Returns:
            True if successful
        """
        if not self._is_active:
            return False
        
        target_chat = chat_id or self.chat_id
        if not target_chat:
            return False
        
        try:
            url = f"{self.base_url}/editMessageText"
            payload = {
                "chat_id": target_chat,
                "message_id": message_id,
                "text": text
            }
            
            if parse_mode:
                payload["parse_mode"] = parse_mode
            
            if reply_markup:
                payload["reply_markup"] = reply_markup
            
            response = self.session.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"[{self.bot_name}] Edit error: {e}")
            return False
    
    def send_voice(
        self,
        voice_file_path: str,
        chat_id: str = None,
        caption: str = None
    ) -> bool:
        """
        Send a voice message
        
        Args:
            voice_file_path: Path to voice file
            chat_id: Target chat ID
            caption: Optional caption
        
        Returns:
            True if successful
        """
        if not self._is_active:
            return False
        
        target_chat = chat_id or self.chat_id
        if not target_chat:
            return False
        
        try:
            url = f"{self.base_url}/sendVoice"
            
            with open(voice_file_path, 'rb') as voice_file:
                files = {"voice": voice_file}
                data = {"chat_id": target_chat}
                
                if caption:
                    data["caption"] = caption
                
                response = self.session.post(url, data=data, files=files, timeout=30)
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"[{self.bot_name}] Voice send error: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics"""
        return {
            "bot_name": self.bot_name,
            "is_active": self._is_active,
            "message_count": self._message_count,
            "last_message_time": self._last_message_time.isoformat() if self._last_message_time else None
        }

    def start_simple_polling(self, welcome_message: str):
        """
        Start a simple background thread to poll for /start commands.
        This ensures Notification and Analytics bots respond to users.
        """
        import threading
        import time
        
        if not self._is_active:
            return

        def _poll():
            offset = 0
            logger.info(f"[{self.bot_name}] Starting simple polling for /start...")
            while True:
                try:
                    url = f"{self.base_url}/getUpdates"
                    params = {"offset": offset, "timeout": 30, "allowed_updates": ["message"]}
                    resp = self.session.get(url, params=params, timeout=35)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("ok"):
                            for result in data.get("result", []):
                                offset = result["update_id"] + 1
                                message = result.get("message", {})
                                text = message.get("text", "")
                                chat_id = message.get("chat", {}).get("id")
                                
                                if text == "/start" and chat_id:
                                    logger.info(f"[{self.bot_name}] Received /start from {chat_id}")
                                    self.send_message(welcome_message, chat_id=chat_id)
                                    
                except Exception as e:
                    logger.error(f"[{self.bot_name}] Polling error: {e}")
                    time.sleep(5)
                
                time.sleep(1)

        t = threading.Thread(target=_poll, daemon=True)
        t.start()
    
    # ========================================
    # ENHANCED UX METHODS (Phase 4)
    # ========================================
    
    def send_chat_action(self, action: str = "typing", chat_id: str = None) -> bool:
        """
        Send chat action (typing indicator, etc.)
        
        Args:
            action: Action type ('typing', 'upload_document', 'upload_photo', etc.)
            chat_id: Target chat ID
        
        Returns:
            True if successful
        """
        if not self._is_active:
            return False
        
        target_chat = chat_id or self.chat_id
        if not target_chat:
            return False
        
        try:
            url = f"{self.base_url}/sendChatAction"
            payload = {
                "chat_id": target_chat,
                "action": action
            }
            response = self.session.post(url, json=payload, timeout=5)
            return response.status_code == 200 and response.json().get("ok", False)
        except Exception as e:
            logger.debug(f"[{self.bot_name}] Chat action error: {e}")
            return False
    
    def send_message_with_keyboard(
        self,
        text: str,
        reply_markup: Dict = None,
        chat_id: str = None,
        parse_mode: str = "HTML"
    ) -> Optional[int]:
        """
        Send message with inline keyboard (wrapper for send_message)
        
        Args:
            text: Message text
            reply_markup: Inline keyboard markup
            chat_id: Target chat ID
            parse_mode: Formatting mode
        
        Returns:
            Message ID if successful
        """
        return self.send_message(text, chat_id, parse_mode, reply_markup)
    
    def set_my_commands(self, commands: list) -> bool:
        """
        Set bot command list (for autocomplete in Telegram)
        
        Args:
            commands: List of dicts with 'command' and 'description'
                Example: [{"command": "start", "description": "Start bot"}]
        
        Returns:
            True if successful
        """
        if not self._is_active:
            return False
        
        try:
            url = f"{self.base_url}/setMyCommands"
            payload = {"commands": commands}
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 200 and response.json().get("ok", False):
                logger.info(f"[{self.bot_name}] Updated command list ({len(commands)} commands)")
                return True
            
            logger.error(f"[{self.bot_name}] Command list update failed")
            return False
        except Exception as e:
            logger.error(f"[{self.bot_name}] Command list error: {e}")
            return False
    
    @staticmethod
    def create_reply_keyboard_markup(
        keyboard: list,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False
    ) -> Dict:
        """
        Create ReplyKeyboardMarkup for persistent keyboard
        
        Args:
            keyboard: List of button rows, each row is a list of button texts
                Example: [["📊 Status", "📈 Analytics"], ["⚙️ Settings"]]
            resize_keyboard: Auto-resize keyboard
            one_time_keyboard: Hide after use
            selective: Show only to specific users
        
        Returns:
            ReplyKeyboardMarkup dict
        
        Example:
            >>> keyboard = [["📊 Status", "📈 Analytics"], ["⚙️ Settings"]]
            >>> markup = BaseTelegramBot.create_reply_keyboard_markup(keyboard)
            >>> bot.send_message("Choose option:", reply_markup=markup)
        """
        return {
            "keyboard": keyboard,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard,
            "selective": selective
        }
    
    @staticmethod
    def remove_reply_keyboard() -> Dict:
        """
        Remove persistent keyboard
        
        Returns:
            ReplyKeyboardRemove dict
        """
        return {"remove_keyboard": True}

