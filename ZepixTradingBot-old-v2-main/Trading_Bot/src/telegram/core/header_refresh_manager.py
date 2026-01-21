"""
Header Refresh Manager - Auto-Update Sticky Headers

Manages background refresh of sticky headers on active menus.

Version: 1.0.0
Created: 2026-01-21
Part of: TELEGRAM_V5_STICKY_HEADER
"""

import asyncio
import logging
from typing import Dict
from .sticky_header_builder import StickyHeaderBuilder

logger = logging.getLogger(__name__)

class HeaderRefreshManager:
    """Manages periodic updates of sticky headers"""

    def __init__(self, bot_instance, refresh_interval: int = 5):
        self.bot = bot_instance
        self.interval = refresh_interval
        self.active_messages: Dict[int, int] = {} # {chat_id: message_id}
        self.builder = StickyHeaderBuilder()
        self._running = False
        self._task = None

    def start(self):
        """Start refresh loop"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._refresh_loop())
            logger.info("[HeaderRefresh] Started background refresh loop")

    def stop(self):
        """Stop refresh loop"""
        self._running = False
        if self._task:
            self._task.cancel()

    def register_message(self, chat_id: int, message_id: int):
        """Register a message for auto-updates"""
        self.active_messages[chat_id] = message_id

    def unregister(self, chat_id: int):
        """Stop updating for a chat"""
        if chat_id in self.active_messages:
            del self.active_messages[chat_id]

    async def _refresh_loop(self):
        """Main loop"""
        while self._running:
            await asyncio.sleep(self.interval)

            # Create snapshot of active messages to avoid modification during iteration
            for chat_id, message_id in list(self.active_messages.items()):
                try:
                    # Logic to update header only
                    # Requires storing original body text or rebuilding complete menu?
                    # Menu rebuilding is safer.
                    # This requires knowing WHICH menu is active.
                    # For now, simplistic PnL update on header.

                    # NOTE: Updating entire message text just to change header
                    # requires holding state of the body content.
                    pass
                except Exception as e:
                    logger.warning(f"[HeaderRefresh] Update failed for {chat_id}: {e}")
                    self.unregister(chat_id)
