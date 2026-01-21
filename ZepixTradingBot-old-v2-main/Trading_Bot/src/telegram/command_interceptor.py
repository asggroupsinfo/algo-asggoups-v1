"""
Command Interceptor - V5 Plugin Selection System

Intercepts commands before execution to show plugin selection screen.
Routes commands to proper plugin context after user selection.

Version: 1.0.0
Created: 2026-01-20
Part of: TELEGRAM_V5_PLUGIN_SELECTION_UPGRADE
"""

import logging
from typing import Dict, Callable, Optional, List, Set
from .plugin_context_manager import PluginContextManager

logger = logging.getLogger(__name__)


class CommandInterceptor:
    """
    Intercepts all commands and shows plugin selection if needed.
    
    Flow:
    1. User sends command (e.g., /status)
    2. Interceptor checks if plugin selection needed
    3. If needed, shows selection screen
    4. User selects plugin (v3/v6/both)
    5. Context stored, command executed with plugin
    6. Context cleared after execution
    
    Features:
    - 95+ plugin-aware commands
    - Automatic selection screen generation
    - Context-aware command routing
    - System command bypass (no selection needed)
    """
    
    # Commands that ALWAYS need plugin selection
    PLUGIN_AWARE_COMMANDS: Set[str] = {
        # Trading Control
        '/pause', '/resume', '/status', '/trades', '/signal_status', '/simulation_mode',
        '/trade', '/buy', '/sell', '/close', '/closeall', '/positions', '/orders',
        '/history', '/equity', '/margin', '/balance', '/pnl', '/price', '/spread',
        '/symbols',
        
        # Performance & Analytics
        '/performance', '/stats', '/performance_report', '/pair_report', '/strategy_report',
        '/chains', '/analytics', '/daily', '/weekly', '/monthly', '/report', '/winrate',
        '/drawdown', '/tp_report', '/v6_performance', '/v6_status', '/compare',
        '/dashboard', '/export',
        
        # Risk Management
        '/risk', '/setlot', '/setsl', '/settp', '/dailylimit', '/maxloss', '/maxprofit',
        '/risktier', '/risk_tier', # handle spelling variations
        '/slsystem', '/trailsl', '/breakeven', '/protection',
        
        # Strategy Control
        '/strategy', '/logic1', '/logic2', '/logic3', '/v3', '/v6', '/signals', '/filters',
        '/logic1_config', '/logic2_config', '/logic3_config',
        '/v6_control', '/v6_1m_config', '/v6_5m_config', '/v6_15m_config', '/v6_1h_config',
        '/mode', '/multiplier',
        
        # Timeframe Control
        '/timeframe', '/trends',
        '/tf1m', '/tf5m',
        '/tf15m', '/tf15m_on', '/tf15m_off',
        '/tf30m', '/tf30m_on', '/tf30m_off',
        '/tf1h', '/tf1h_on', '/tf1h_off',
        '/tf4h', '/tf4h_on', '/tf4h_off',
        '/tf1d',
        
        # Re-entry System
        '/reentry', '/slhunt', '/tpcontinue', '/recovery', '/cooldown', '/autonomous',
        '/chainlimit', '/maxrecovery', '/reentry_enable', '/reentry_disable',
        '/reentry_config', '/reentry_status', '/reentry_history',
        
        # Profit Booking
        '/profit', '/booking', '/levels', '/partial', '/orderb', '/dualorder',
        '/pb_enable', '/pb_disable', '/pb_config', '/pb_chains', '/pb_history',
        '/pb_stats', '/pb_multiplier', '/pb_tier1', '/pb_tier2', '/pb_tier3',
        
        # Session Management
        '/session', '/london', '/newyork', '/tokyo', '/sydney', '/overlap',
        
        # Plugin Control
        '/plugins', '/enable', '/disable', '/upgrade', '/rollback', '/shadow', '/plugin',
        
        # Notification & System (that affects trading)
        '/notifications', '/mute', '/unmute',
    }
    
    # Commands that NEVER need plugin selection (system commands)
    SYSTEM_COMMANDS: Set[str] = {
        '/start', '/help', '/health', '/version', '/config',
        '/restart', '/shutdown', '/voice', '/voicetest'
    }
    
    def __init__(self, telegram_bot=None):
        """
        Initialize Command Interceptor.
        
        Args:
            telegram_bot: TelegramBot instance for sending messages
        """
        self.telegram_bot = telegram_bot
        self._pending_commands: Dict[int, str] = {}  # {chat_id: command}
        
        logger.info(
            f"[CommandInterceptor] Initialized with "
            f"{len(self.PLUGIN_AWARE_COMMANDS)} plugin-aware commands"
        )
    
    def intercept_command(
        self,
        command: str,
        chat_id: int,
        message: Dict = None
    ) -> bool:
        """
        Intercept command and check if plugin selection needed.
        
        Args:
            command: Command string (e.g., '/status')
            chat_id: Telegram chat ID
            message: Full message dict
        
        Returns:
            True if plugin selection shown (command paused)
            False if command can proceed (plugin already selected or not needed)
        """
        # Check if this is a system command (no selection needed)
        if command in self.SYSTEM_COMMANDS:
            logger.debug(f"[CommandInterceptor] System command, no selection: {command}")
            return False
        
        # Check if command needs plugin selection
        if command not in self.PLUGIN_AWARE_COMMANDS:
            logger.debug(f"[CommandInterceptor] Unknown/custom command, no selection: {command}")
            return False
        
        # Check if user already has active plugin context
        existing_context = PluginContextManager.get_plugin_context(chat_id)
        if existing_context:
            logger.debug(
                f"[CommandInterceptor] Plugin already selected ({existing_context}), "
                f"proceeding with {command}"
            )
            return False
        
        # Show plugin selection screen
        logger.info(f"[CommandInterceptor] Showing plugin selection for {command}")
        self._pending_commands[chat_id] = command
        self._show_plugin_selection(command, chat_id)
        return True  # Command paused, waiting for selection
    
    def _show_plugin_selection(self, command: str, chat_id: int):
        """
        Show plugin selection screen to user.
        
        Args:
            command: Command to execute after selection
            chat_id: Telegram chat ID
        """
        # Build message
        message = (
            f"🔌 <b>SELECT PLUGIN FOR {command.upper()}</b>\n\n"
            f"Choose which plugin to control:\n"
        )
        
        # Build keyboard
        keyboard = {
            'inline_keyboard': [
                [
                    {
                        'text': '🔵 V3 Combined Logic',
                        'callback_data': f'plugin_select_v3_{command[1:]}'  # Remove /
                    },
                    {
                        'text': '🟢 V6 Price Action',
                        'callback_data': f'plugin_select_v6_{command[1:]}'
                    }
                ],
                [
                    {
                        'text': '🔷 Both Plugins',
                        'callback_data': f'plugin_select_both_{command[1:]}'
                    }
                ],
                [
                    {
                        'text': '❌ Cancel',
                        'callback_data': 'plugin_select_cancel'
                    }
                ]
            ]
        }
        
        # Send selection screen
        if self.telegram_bot:
            try:
                self.telegram_bot.send_message(
                    message,
                    chat_id=chat_id,
                    reply_markup=keyboard
                )
                logger.debug(f"[CommandInterceptor] Sent selection screen for {command}")
            except Exception as e:
                logger.error(f"[CommandInterceptor] Failed to send selection screen: {e}")
    
    def handle_plugin_selection_callback(
        self,
        callback_data: str,
        chat_id: int,
        message_id: int = None
    ) -> Optional[Dict]:
        """
        Handle plugin selection callback from user.
        
        Callback format: plugin_select_v3_status
        
        Args:
            callback_data: Callback data from button
            chat_id: Telegram chat ID
            message_id: Message ID to edit (if available)
        
        Returns:
            Dict with command execution info or None if cancelled
        """
        # Parse callback data
        parts = callback_data.split('_')
        
        if len(parts) < 3:
            logger.error(f"[CommandInterceptor] Invalid callback format: {callback_data}")
            return None
        
        # Check for cancel
        if parts[2] == 'cancel':
            logger.info(f"[CommandInterceptor] User cancelled plugin selection")
            if self.telegram_bot and message_id:
                self.telegram_bot.edit_message_text(
                    "❌ Command cancelled",
                    chat_id=chat_id,
                    message_id=message_id
                )
            # Clear pending command
            if chat_id in self._pending_commands:
                del self._pending_commands[chat_id]
            return None
        
        # Extract plugin and command
        plugin = parts[2]  # 'v3', 'v6', 'both'
        command = '/' + '_'.join(parts[3:])  # Reconstruct command with /
        
        # Validate plugin
        if plugin not in ['v3', 'v6', 'both']:
            logger.error(f"[CommandInterceptor] Invalid plugin selection: {plugin}")
            return None
        
        # Store plugin context
        PluginContextManager.set_plugin_context(chat_id, plugin, command)
        
        # Edit message to show selection
        if self.telegram_bot and message_id:
            try:
                plugin_display = {
                    'v3': '🔵 V3 Combined Logic',
                    'v6': '🟢 V6 Price Action',
                    'both': '🔷 Both Plugins'
                }
                
                self.telegram_bot.edit_message_text(
                    f"✅ Plugin selected: {plugin_display.get(plugin, plugin.upper())}\n"
                    f"Executing {command}...",
                    chat_id=chat_id,
                    message_id=message_id
                )
            except Exception as e:
                logger.error(f"[CommandInterceptor] Failed to edit message: {e}")
        
        logger.info(
            f"[CommandInterceptor] Plugin {plugin} selected for {command} "
            f"by chat {chat_id}"
        )
        
        # Remove from pending
        if chat_id in self._pending_commands:
            del self._pending_commands[chat_id]
        
        # Return execution info
        return {
            'command': command,
            'plugin': plugin,
            'chat_id': chat_id
        }
    
    def is_command_plugin_aware(self, command: str) -> bool:
        """
        Check if command requires plugin selection.
        
        Args:
            command: Command string
        
        Returns:
            True if command needs plugin selection
        """
        return command in self.PLUGIN_AWARE_COMMANDS
    
    def get_pending_command(self, chat_id: int) -> Optional[str]:
        """
        Get pending command for user (waiting for plugin selection).
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            Command string or None
        """
        return self._pending_commands.get(chat_id)
    
    def clear_pending_command(self, chat_id: int) -> bool:
        """
        Clear pending command for user.
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            True if command was pending
        """
        if chat_id in self._pending_commands:
            del self._pending_commands[chat_id]
            return True
        return False
    
    def get_stats(self) -> Dict:
        """
        Get interceptor statistics.
        
        Returns:
            Dict with stats
        """
        return {
            'plugin_aware_commands': len(self.PLUGIN_AWARE_COMMANDS),
            'system_commands': len(self.SYSTEM_COMMANDS),
            'pending_selections': len(self._pending_commands),
            'context_stats': PluginContextManager.get_stats()
        }


# Convenience instance (singleton pattern)
_interceptor_instance: Optional[CommandInterceptor] = None


def get_interceptor(telegram_bot=None) -> CommandInterceptor:
    """Get or create CommandInterceptor instance."""
    global _interceptor_instance
    if _interceptor_instance is None:
        _interceptor_instance = CommandInterceptor(telegram_bot)
    return _interceptor_instance
