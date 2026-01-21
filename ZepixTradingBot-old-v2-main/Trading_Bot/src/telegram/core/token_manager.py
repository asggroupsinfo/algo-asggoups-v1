"""
Token Manager - Secure Token Management for 3-Bot Architecture
Version: 1.0.0
Date: 2026-01-20
"""

import os
import logging
from typing import Dict, NamedTuple, Optional, Any

logger = logging.getLogger(__name__)

class BotConfig(NamedTuple):
    token: str
    mode: str  # 'dedicated' or 'shared'

class TokenManager:
    """
    Manages Telegram tokens for the 3-bot system.
    Determines if system runs in Single-Bot (Shared) or Multi-Bot (Dedicated) mode.
    """
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize with raw config dictionary.
        
        Args:
            config_dict: Dictionary containing telegram_token, telegram_controller_token, etc.
        """
        self.raw_config = config_dict
        self.controller_config: Optional[BotConfig] = None
        self.notification_config: Optional[BotConfig] = None
        self.analytics_config: Optional[BotConfig] = None
        self.is_multi_bot_mode = False
        
        self._parse_tokens()
        
    def _parse_tokens(self):
        """Parse tokens and determine mode"""
        main_token = self.raw_config.get("telegram_token")
        ct_token = self.raw_config.get("telegram_controller_token")
        nt_token = self.raw_config.get("telegram_notification_token")
        an_token = self.raw_config.get("telegram_analytics_token")
        
        if not main_token and not (ct_token and nt_token and an_token):
             logger.error("No valid Telegram tokens found!")
             # Do not raise here, allow graceful degradation if possible, but log severe error
             return

        # Controller Logic
        if ct_token:
            self.controller_config = BotConfig(ct_token, "dedicated")
        elif main_token:
            self.controller_config = BotConfig(main_token, "shared")
            
        # Notification Logic
        if nt_token:
            self.notification_config = BotConfig(nt_token, "dedicated")
        elif main_token:
            self.notification_config = BotConfig(main_token, "shared")
            
        # Analytics Logic
        if an_token:
            self.analytics_config = BotConfig(an_token, "dedicated")
        elif main_token:
            self.analytics_config = BotConfig(main_token, "shared")
            
        # Determine Mode
        distinct_tokens = {
            t.token for t in [self.controller_config, self.notification_config, self.analytics_config]
            if t is not None
        }
        
        self.is_multi_bot_mode = len(distinct_tokens) > 1
        
        mode_str = "MULTI-BOT" if self.is_multi_bot_mode else "SINGLE-BOT"
        logger.info(f"[TokenManager] Initialized in {mode_str} mode. ({len(distinct_tokens)} unique tokens)")

    @property
    def mode(self) -> str:
        """Return current mode"""
        return "MULTI_BOT" if self.is_multi_bot_mode else "SINGLE_BOT"

    def get_token(self, bot_type: str) -> Optional[str]:
        """Get token by bot type (CONTROLLER, NOTIFICATION, ANALYTICS, MAIN)"""
        bot_type = bot_type.upper()
        if bot_type == "CONTROLLER":
            return self.get_controller_token()
        elif bot_type == "NOTIFICATION":
            return self.get_notification_token()
        elif bot_type == "ANALYTICS":
            return self.get_analytics_token()
        elif bot_type == "MAIN":
            # Return the main shared token
            return self.raw_config.get("telegram_token")
        return None

    def get_controller_token(self) -> Optional[str]:
        return self.controller_config.token if self.controller_config else None

    def get_notification_token(self) -> Optional[str]:
        return self.notification_config.token if self.notification_config else None
        
    def get_analytics_token(self) -> Optional[str]:
        return self.analytics_config.token if self.analytics_config else None
