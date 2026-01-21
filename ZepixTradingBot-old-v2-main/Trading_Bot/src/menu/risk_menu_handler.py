"""
Risk Menu Handler - Risk Management Controls

Manages risk settings and limits via Telegram menu.

Features:
- Daily loss limits
- Max open trades
- Max risk per trade
- Emergency stop controls
- Risk tier presets

Version: 1.0.0
Date: 2026-01-20
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RiskMenuHandler:
    """
    Handles risk management menu for Telegram bot.
    
    Provides:
    - Daily loss limit configuration
    - Max trades limit
    - Risk per trade settings
    - Emergency stop functionality
    """
    
    def __init__(self, telegram_bot):
        """
        Initialize RiskMenuHandler.
        
        Args:
            telegram_bot: The Telegram bot instance
        """
        self.bot = telegram_bot
        self._logger = logger
    
    def _get_risk_config(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        try:
            if hasattr(self.bot, 'config'):
                return self.bot.config.get("risk_management", {})
            return {}
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error getting risk config: {e}")
            return {}
    
    def _format_currency(self, amount: float) -> str:
        """Format currency amount"""
        return f"${amount:.2f}"
    
    def show_risk_menu(self, user_id: int, message_id: int = None):
        """
        Show main risk management menu.
        
        Args:
            user_id: Telegram user ID
            message_id: Message ID to edit (optional)
        """
        risk_config = self._get_risk_config()
        
        # Get current settings
        daily_loss_limit = risk_config.get("daily_loss_limit", 100.0)
        max_trades = risk_config.get("max_open_trades", 5)
        risk_per_trade = risk_config.get("risk_per_trade_percent", 2.0)
        emergency_stop_enabled = risk_config.get("emergency_stop_enabled", False)
        
        # Get current stats
        daily_loss = self._get_daily_loss()
        open_trades_count = self._get_open_trades_count()
        
        # Calculate limits
        loss_pct = (abs(daily_loss) / daily_loss_limit * 100) if daily_loss_limit > 0 else 0
        trades_pct = (open_trades_count / max_trades * 100) if max_trades > 0 else 0
        
        text = f"""🛡️ <b>RISK MANAGEMENT</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>📊 Current Status:</b>

💰 <b>Daily Loss Limit:</b> {self._format_currency(daily_loss_limit)}
  • Today's Loss: {self._format_currency(daily_loss)}
  • Usage: {loss_pct:.1f}% [{self._create_progress_bar(loss_pct)}]

📈 <b>Max Open Trades:</b> {max_trades}
  • Currently Open: {open_trades_count}
  • Usage: {trades_pct:.1f}% [{self._create_progress_bar(trades_pct)}]

💎 <b>Risk Per Trade:</b> {risk_per_trade:.1f}%

⚠️ <b>Emergency Stop:</b> {'🟢 ENABLED' if emergency_stop_enabled else '🔴 DISABLED'}

━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        keyboard = [
            [
                {"text": f"💰 Daily Limit ({self._format_currency(daily_loss_limit)})", 
                 "callback_data": "risk_daily_limit"},
                {"text": f"📈 Max Trades ({max_trades})", 
                 "callback_data": "risk_max_trades"}
            ],
            [
                {"text": f"💎 Risk/Trade ({risk_per_trade:.1f}%)", 
                 "callback_data": "risk_per_trade"},
                {"text": "🎚️ Risk Tiers", 
                 "callback_data": "risk_tiers"}
            ],
            [
                {"text": f"⚠️ E-Stop: {'🟢 ON' if emergency_stop_enabled else '🔴 OFF'}", 
                 "callback_data": "risk_toggle_estop"}
            ],
            [
                {"text": "📊 Risk Report", "callback_data": "risk_report"},
                {"text": "🔄 Reset Limits", "callback_data": "risk_reset"}
            ],
            [
                {"text": "🔙 Back", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(user_id, text, reply_markup, message_id)
    
    def _create_progress_bar(self, percentage: float, width: int = 10) -> str:
        """Create visual progress bar"""
        filled = int((percentage / 100) * width)
        filled = min(filled, width)  # Cap at width
        empty = width - filled
        return "█" * filled + "░" * empty
    
    def _get_daily_loss(self) -> float:
        """Get today's loss amount"""
        try:
            if hasattr(self.bot, 'trading_engine') and self.bot.trading_engine:
                db = getattr(self.bot.trading_engine, 'database', None)
                if db and hasattr(db, 'get_daily_pnl'):
                    from datetime import datetime
                    today = datetime.now().strftime("%Y-%m-%d")
                    pnl = db.get_daily_pnl(today)
                    return abs(pnl) if pnl < 0 else 0.0
            return 0.0
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error getting daily loss: {e}")
            return 0.0
    
    def _get_open_trades_count(self) -> int:
        """Get count of open trades"""
        try:
            if hasattr(self.bot, 'trading_engine') and self.bot.trading_engine:
                if hasattr(self.bot.trading_engine, 'get_open_trades_count'):
                    return self.bot.trading_engine.get_open_trades_count()
            return 0
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error getting open trades: {e}")
            return 0
    
    def show_daily_limit_menu(self, user_id: int, message_id: int = None):
        """Show daily loss limit configuration menu"""
        text = """💰 <b>DAILY LOSS LIMIT</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Select daily loss limit:
"""
        
        presets = [50, 100, 150, 200, 300, 500]
        
        keyboard = []
        row = []
        for i, preset in enumerate(presets):
            row.append({
                "text": f"${preset}", 
                "callback_data": f"risk_set_daily_{preset}"
            })
            if (i + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([
            {"text": "✏️ Custom", "callback_data": "risk_daily_custom"},
            {"text": "🔙 Back", "callback_data": "menu_risk"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(user_id, text, reply_markup, message_id)
    
    def show_max_trades_menu(self, user_id: int, message_id: int = None):
        """Show max open trades configuration menu"""
        text = """📈 <b>MAX OPEN TRADES</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Select maximum open trades:
"""
        
        presets = [1, 2, 3, 5, 8, 10]
        
        keyboard = []
        row = []
        for i, preset in enumerate(presets):
            row.append({
                "text": str(preset), 
                "callback_data": f"risk_set_max_trades_{preset}"
            })
            if (i + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([
            {"text": "🔙 Back", "callback_data": "menu_risk"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(user_id, text, reply_markup, message_id)
    
    def show_risk_per_trade_menu(self, user_id: int, message_id: int = None):
        """Show risk per trade percentage menu"""
        text = """💎 <b>RISK PER TRADE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Select risk percentage per trade:
"""
        
        presets = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0]
        
        keyboard = []
        row = []
        for i, preset in enumerate(presets):
            row.append({
                "text": f"{preset:.1f}%", 
                "callback_data": f"risk_set_per_trade_{preset}"
            })
            if (i + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([
            {"text": "🔙 Back", "callback_data": "menu_risk"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(user_id, text, reply_markup, message_id)
    
    def show_risk_tiers_menu(self, user_id: int, message_id: int = None):
        """Show risk tier presets"""
        text = """🎚️ <b>RISK TIER PRESETS</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Select a risk management tier:
"""
        
        tiers = [
            {"name": "🟢 Conservative", "daily": 50, "trades": 3, "risk": 1.0},
            {"name": "🟡 Moderate", "daily": 100, "trades": 5, "risk": 2.0},
            {"name": "🟠 Aggressive", "daily": 200, "trades": 8, "risk": 3.0},
            {"name": "🔴 Ultra Aggressive", "daily": 500, "trades": 10, "risk": 5.0}
        ]
        
        keyboard = []
        for i, tier in enumerate(tiers):
            text += f"\n{tier['name']}\n"
            text += f"  • Daily: ${tier['daily']} | Trades: {tier['trades']} | Risk: {tier['risk']}%\n"
            
            keyboard.append([{
                "text": tier['name'],
                "callback_data": f"risk_tier_{i}"
            }])
        
        keyboard.append([
            {"text": "🔙 Back", "callback_data": "menu_risk"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(user_id, text, reply_markup, message_id)
    
    def handle_callback(self, user_id: int, message_id: int, callback_data: str) -> bool:
        """
        Handle risk menu callbacks.
        
        Args:
            user_id: Telegram user ID
            message_id: Message ID
            callback_data: Callback data string
        
        Returns:
            True if handled, False otherwise
        """
        if callback_data == "menu_risk":
            self.show_risk_menu(user_id, message_id)
            return True
        
        elif callback_data == "risk_daily_limit":
            self.show_daily_limit_menu(user_id, message_id)
            return True
        
        elif callback_data == "risk_max_trades":
            self.show_max_trades_menu(user_id, message_id)
            return True
        
        elif callback_data == "risk_per_trade":
            self.show_risk_per_trade_menu(user_id, message_id)
            return True
        
        elif callback_data == "risk_tiers":
            self.show_risk_tiers_menu(user_id, message_id)
            return True
        
        elif callback_data.startswith("risk_set_daily_"):
            amount = float(callback_data.replace("risk_set_daily_", ""))
            self._update_daily_limit(amount)
            self.show_risk_menu(user_id, message_id)
            return True
        
        elif callback_data.startswith("risk_set_max_trades_"):
            count = int(callback_data.replace("risk_set_max_trades_", ""))
            self._update_max_trades(count)
            self.show_risk_menu(user_id, message_id)
            return True
        
        elif callback_data.startswith("risk_set_per_trade_"):
            risk = float(callback_data.replace("risk_set_per_trade_", ""))
            self._update_risk_per_trade(risk)
            self.show_risk_menu(user_id, message_id)
            return True
        
        elif callback_data.startswith("risk_tier_"):
            tier_idx = int(callback_data.replace("risk_tier_", ""))
            self._apply_risk_tier(tier_idx)
            self.show_risk_menu(user_id, message_id)
            return True
        
        elif callback_data == "risk_toggle_estop":
            self._toggle_emergency_stop()
            self.show_risk_menu(user_id, message_id)
            return True
        
        return False
    
    def _update_daily_limit(self, amount: float):
        """Update daily loss limit"""
        try:
            if hasattr(self.bot, 'config'):
                if "risk_management" not in self.bot.config:
                    self.bot.config["risk_management"] = {}
                self.bot.config["risk_management"]["daily_loss_limit"] = amount
                self._logger.info(f"[RiskMenu] Daily loss limit updated to ${amount}")
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error updating daily limit: {e}")
    
    def _update_max_trades(self, count: int):
        """Update max open trades"""
        try:
            if hasattr(self.bot, 'config'):
                if "risk_management" not in self.bot.config:
                    self.bot.config["risk_management"] = {}
                self.bot.config["risk_management"]["max_open_trades"] = count
                self._logger.info(f"[RiskMenu] Max trades updated to {count}")
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error updating max trades: {e}")
    
    def _update_risk_per_trade(self, risk: float):
        """Update risk per trade percentage"""
        try:
            if hasattr(self.bot, 'config'):
                if "risk_management" not in self.bot.config:
                    self.bot.config["risk_management"] = {}
                self.bot.config["risk_management"]["risk_per_trade_percent"] = risk
                self._logger.info(f"[RiskMenu] Risk per trade updated to {risk}%")
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error updating risk per trade: {e}")
    
    def _apply_risk_tier(self, tier_idx: int):
        """Apply risk tier preset"""
        tiers = [
            {"daily": 50, "trades": 3, "risk": 1.0},
            {"daily": 100, "trades": 5, "risk": 2.0},
            {"daily": 200, "trades": 8, "risk": 3.0},
            {"daily": 500, "trades": 10, "risk": 5.0}
        ]
        
        if 0 <= tier_idx < len(tiers):
            tier = tiers[tier_idx]
            self._update_daily_limit(tier["daily"])
            self._update_max_trades(tier["trades"])
            self._update_risk_per_trade(tier["risk"])
            self._logger.info(f"[RiskMenu] Applied risk tier {tier_idx}")
    
    def _toggle_emergency_stop(self):
        """Toggle emergency stop"""
        try:
            if hasattr(self.bot, 'config'):
                if "risk_management" not in self.bot.config:
                    self.bot.config["risk_management"] = {}
                current = self.bot.config["risk_management"].get("emergency_stop_enabled", False)
                self.bot.config["risk_management"]["emergency_stop_enabled"] = not current
                self._logger.info(f"[RiskMenu] Emergency stop toggled to {not current}")
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error toggling emergency stop: {e}")
    
    def _send_message(self, user_id: int, text: str, reply_markup: Dict = None, message_id: int = None):
        """Send or edit message"""
        try:
            if message_id and hasattr(self.bot, 'edit_message'):
                self.bot.edit_message(text, message_id, reply_markup, parse_mode="HTML")
            elif hasattr(self.bot, 'send_message_with_keyboard') and reply_markup:
                self.bot.send_message_with_keyboard(text, reply_markup, parse_mode="HTML")
            elif hasattr(self.bot, 'send_message'):
                self.bot.send_message(text, parse_mode="HTML")
            else:
                self._logger.warning("[RiskMenu] No send method available")
        except Exception as e:
            self._logger.error(f"[RiskMenu] Error sending message: {e}")
