"""
Plugin Selection Menu Builder - V5 Plugin Selection System

Builds plugin selection screens with rich UI formatting.
Generates consistent selection interfaces across all commands.

Version: 1.0.0
Created: 2026-01-20
Part of: TELEGRAM_V5_PLUGIN_SELECTION_UPGRADE
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PluginSelectionMenuBuilder:
    """
    Builds plugin selection menus with consistent formatting.
    
    Features:
    - Rich HTML formatting
    - Consistent button layout
    - Command-specific descriptions
    - Visual indicators (emojis)
    - Cancel option
    """
    
    # Plugin display info
    PLUGIN_INFO = {
        'v3': {
            'emoji': '🔵',
            'name': 'V3 Combined Logic',
            'short': 'V3',
            'color': 'blue',
            'description': '3 strategies on 5M/15M/1H'
        },
        'v6': {
            'emoji': '🟢',
            'name': 'V6 Price Action',
            'short': 'V6',
            'color': 'green',
            'description': '4 timeframes (15M/30M/1H/4H)'
        },
        'both': {
            'emoji': '🔷',
            'name': 'Both Plugins',
            'short': 'Both',
            'color': 'purple',
            'description': 'Combined V3 + V6 data'
        }
    }
    
    # Command-specific descriptions
    COMMAND_DESCRIPTIONS = {
        '/status': 'View status for',
        '/pause': 'Pause trading for',
        '/resume': 'Resume trading for',
        '/positions': 'Show positions from',
        '/pnl': 'Show P&L for',
        '/setlot': 'Set lot size for',
        '/risktier': 'Configure risk tier for',
        '/chains': 'View re-entry chains for',
        '/autonomous': 'Toggle autonomous mode for',
        '/performance': 'View performance of',
        '/analytics': 'Show analytics for',
        '/daily': 'Daily report for',
        '/weekly': 'Weekly report for',
        '/monthly': 'Monthly report for',
        '/winrate': 'Win rate statistics for',
        '/drawdown': 'Drawdown analysis for',
        '/compare': 'Compare plugins',
    }
    
    @classmethod
    def build_selection_message(
        cls,
        command: str,
        include_description: bool = True,
        custom_text: str = None
    ) -> str:
        """
        Build plugin selection message text.
        
        Args:
            command: Command being executed (e.g., '/status')
            include_description: Include command description
            custom_text: Custom description override
        
        Returns:
            Formatted message text (HTML)
        """
        command_upper = command.upper()
        
        # Get description
        if custom_text:
            description = custom_text
        elif include_description and command in cls.COMMAND_DESCRIPTIONS:
            description = cls.COMMAND_DESCRIPTIONS[command]
        else:
            description = "Select plugin for"
        
        message = (
            f"🔌 <b>SELECT PLUGIN FOR {command_upper}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{description} which plugin?\n\n"
            f"<b>Available Plugins:</b>\n"
            f"🔵 <b>V3 Combined Logic</b>\n"
            f"   └─ 3 strategies on 5M/15M/1H\n\n"
            f"🟢 <b>V6 Price Action</b>\n"
            f"   └─ 4 timeframes (15M/30M/1H/4H)\n\n"
            f"🔷 <b>Both Plugins</b>\n"
            f"   └─ Combined data from V3 + V6\n\n"
            f"<i>Select one to continue...</i>"
        )
        
        return message
    
    @classmethod
    def build_selection_keyboard(
        cls,
        command: str,
        include_both: bool = True,
        include_cancel: bool = True
    ) -> Dict:
        """
        Build plugin selection keyboard.
        
        Args:
            command: Command for callback data
            include_both: Include "Both" option
            include_cancel: Include cancel button
        
        Returns:
            Telegram inline keyboard markup
        """
        # Remove leading slash from command
        cmd_clean = command[1:] if command.startswith('/') else command
        
        # Build button rows
        buttons = []
        
        # Row 1: V3 and V6
        row1 = [
            {
                'text': f"{cls.PLUGIN_INFO['v3']['emoji']} {cls.PLUGIN_INFO['v3']['name']}",
                'callback_data': f'plugin_select_v3_{cmd_clean}'
            },
            {
                'text': f"{cls.PLUGIN_INFO['v6']['emoji']} {cls.PLUGIN_INFO['v6']['name']}",
                'callback_data': f'plugin_select_v6_{cmd_clean}'
            }
        ]
        buttons.append(row1)
        
        # Row 2: Both (if enabled)
        if include_both:
            row2 = [
                {
                    'text': f"{cls.PLUGIN_INFO['both']['emoji']} {cls.PLUGIN_INFO['both']['name']}",
                    'callback_data': f'plugin_select_both_{cmd_clean}'
                }
            ]
            buttons.append(row2)
        
        # Row 3: Cancel (if enabled)
        if include_cancel:
            row3 = [
                {
                    'text': '❌ Cancel',
                    'callback_data': 'plugin_select_cancel'
                }
            ]
            buttons.append(row3)
        
        return {'inline_keyboard': buttons}
    
    @classmethod
    def build_full_selection_screen(
        cls,
        command: str,
        custom_text: str = None,
        include_both: bool = True
    ) -> tuple[str, Dict]:
        """
        Build complete selection screen (message + keyboard).
        
        Args:
            command: Command being executed
            custom_text: Custom message text
            include_both: Include "Both" option
        
        Returns:
            Tuple of (message_text, keyboard_markup)
        """
        message = cls.build_selection_message(command, custom_text=custom_text)
        keyboard = cls.build_selection_keyboard(command, include_both=include_both)
        
        return message, keyboard
    
    @classmethod
    def build_confirmation_message(
        cls,
        plugin: str,
        command: str
    ) -> str:
        """
        Build confirmation message after plugin selection.
        
        Args:
            plugin: Selected plugin ('v3', 'v6', 'both')
            command: Command being executed
        
        Returns:
            Confirmation message text (HTML)
        """
        if plugin not in cls.PLUGIN_INFO:
            plugin_name = plugin.upper()
            emoji = '🔌'
        else:
            info = cls.PLUGIN_INFO[plugin]
            plugin_name = info['name']
            emoji = info['emoji']
        
        message = (
            f"✅ <b>Plugin Selected</b>\n\n"
            f"{emoji} <b>{plugin_name}</b>\n\n"
            f"Executing {command.upper()}...\n"
            f"<i>Please wait...</i>"
        )
        
        return message
    
    @classmethod
    def build_cancel_message(cls) -> str:
        """
        Build cancellation message.
        
        Returns:
            Cancel message text (HTML)
        """
        return "❌ <b>Command Cancelled</b>\n\n<i>Plugin selection aborted.</i>"
    
    @classmethod
    def build_error_message(cls, error: str) -> str:
        """
        Build error message for selection failures.
        
        Args:
            error: Error description
        
        Returns:
            Error message text (HTML)
        """
        return (
            f"❌ <b>Selection Error</b>\n\n"
            f"{error}\n\n"
            f"<i>Please try again.</i>"
        )
    
    @classmethod
    def build_timeout_message(cls, command: str) -> str:
        """
        Build timeout message for expired selections.
        
        Args:
            command: Command that timed out
        
        Returns:
            Timeout message text (HTML)
        """
        return (
            f"⏱️ <b>Selection Timeout</b>\n\n"
            f"Plugin selection for {command.upper()} expired.\n\n"
            f"<i>Please send the command again.</i>"
        )
    
    @classmethod
    def build_quick_selection_buttons(
        cls,
        commands: List[str]
    ) -> Dict:
        """
        Build quick selection keyboard for multiple commands.
        
        Args:
            commands: List of commands to create buttons for
        
        Returns:
            Telegram inline keyboard
        """
        buttons = []
        for i in range(0, len(commands), 2):
            row = []
            for j in range(2):
                if i + j < len(commands):
                    cmd = commands[i + j]
                    row.append({
                        'text': cmd.upper(),
                        'callback_data': f'quick_cmd_{cmd[1:]}'
                    })
            if row:
                buttons.append(row)
        
        return {'inline_keyboard': buttons}
    
    @classmethod
    def get_plugin_display_name(cls, plugin: str, short: bool = False) -> str:
        """
        Get display name for plugin.
        
        Args:
            plugin: Plugin ID ('v3', 'v6', 'both')
            short: Use short name
        
        Returns:
            Display name with emoji
        """
        if plugin not in cls.PLUGIN_INFO:
            return plugin.upper()
        
        info = cls.PLUGIN_INFO[plugin]
        name = info['short'] if short else info['name']
        return f"{info['emoji']} {name}"
    
    @classmethod
    def format_plugin_status(
        cls,
        plugin: str,
        enabled: bool,
        details: str = None
    ) -> str:
        """
        Format plugin status line.
        
        Args:
            plugin: Plugin ID
            enabled: Whether plugin is enabled
            details: Additional details line
        
        Returns:
            Formatted status line
        """
        display = cls.get_plugin_display_name(plugin)
        status = "🟢 ENABLED" if enabled else "🔴 DISABLED"
        
        line = f"{display}: {status}"
        if details:
            line += f"\n   └─ {details}"
        
        return line


# Convenience functions

def show_plugin_selection(
    telegram_bot,
    command: str,
    chat_id: int,
    custom_text: str = None
) -> Optional[int]:
    """
    Show plugin selection screen (convenience function).
    
    Args:
        telegram_bot: TelegramBot instance
        command: Command being executed
        chat_id: Telegram chat ID
        custom_text: Custom message text
    
    Returns:
        Message ID if successful
    """
    message, keyboard = PluginSelectionMenuBuilder.build_full_selection_screen(
        command,
        custom_text=custom_text
    )
    
    try:
        return telegram_bot.send_message(
            message,
            chat_id=chat_id,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"[MenuBuilder] Failed to show selection: {e}")
        return None
