"""
Error Handler Utilities

Centralized error handling functions for the trading bot.
Based on: Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from collections import defaultdict

from .error_codes import *

logger = logging.getLogger(__name__)


class SignalDeduplicator:
    """
    Prevent duplicate signal processing (TE-003)
    """
    
    def __init__(self, ttl_seconds: int = 60):
        """
        Initialize deduplicator
        
        Args:
            ttl_seconds: Time-to-live for signals in cache
        """
        self.recent_signals = {}
        self.ttl = ttl_seconds
        logger.info(f"SignalDeduplicator initialized with {ttl_seconds}s TTL")
    
    def is_duplicate(self, signal: dict) -> bool:
        """
        Check if signal is duplicate
        
        Args:
            signal: Signal dictionary
        
        Returns:
            True if duplicate, False otherwise
        """
        try:
            # Create unique key
            key = f"{signal.get('symbol')}_{signal.get('direction')}_{signal.get('entry')}"
            
            # Check cache
            if key in self.recent_signals:
                last_time = self.recent_signals[key]
                age = (datetime.now() - last_time).seconds
                
                if age < self.ttl:
                    logger.info(f"{TE_003_DUPLICATE}: Blocked duplicate signal - {key} (age: {age}s)")
                    return True
            
            # Store signal
            self.recent_signals[key] = datetime.now()
            self._cleanup_old_signals()
            return False
            
        except Exception as e:
            logger.error(f"Error checking duplicate signal: {e}")
            return False
    
    def _cleanup_old_signals(self):
        """Remove expired signals from cache"""
        try:
            cutoff = datetime.now() - timedelta(seconds=self.ttl * 2)
            self.recent_signals = {
                k: v for k, v in self.recent_signals.items()
                if v > cutoff
            }
        except Exception as e:
            logger.error(f"Error cleaning up signal cache: {e}")


class NotificationQueue:
    """
    Notification queue with overflow handling (NF-001)
    """
    
    def __init__(self, max_size: int = MAX_NOTIFICATION_QUEUE_SIZE):
        """
        Initialize queue
        
        Args:
            max_size: Maximum queue size
        """
        self.queue = []
        self.max_size = max_size
        logger.info(f"NotificationQueue initialized with max size {max_size}")
    
    async def enqueue(self, notification: dict):
        """
        Add notification with overflow handling
        
        Args:
            notification: Notification data
        """
        try:
            if len(self.queue) >= self.max_size:
                logger.warning(f"{NF_001_QUEUE_FULL}: Queue at capacity, dropping oldest 10%")
                drop_count = max(1, self.max_size // 10)
                self.queue = self.queue[drop_count:]
            
            self.queue.append(notification)
            
        except Exception as e:
            logger.error(f"Error enqueueing notification: {e}")
    
    async def dequeue(self) -> Optional[dict]:
        """
        Remove and return oldest notification
        
        Returns:
            Notification dict or None if empty
        """
        try:
            if self.queue:
                return self.queue.pop(0)
            return None
        except Exception as e:
            logger.error(f"Error dequeuing notification: {e}")
            return None
    
    def size(self) -> int:
        """Get current queue size"""
        return len(self.queue)
    
    def is_full(self) -> bool:
        """Check if queue is at capacity"""
        return len(self.queue) >= self.max_size


def validate_signal(signal: dict) -> Tuple[bool, str]:
    """
    Validate incoming signal (TE-001)
    
    Args:
        signal: Signal dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        errors = []
        
        # Check required fields
        for field in REQUIRED_SIGNAL_FIELDS:
            if field not in signal or signal[field] is None:
                errors.append(f"Missing {field}")
        
        # Validate direction
        direction = signal.get('direction', '').upper()
        if direction not in ['BUY', 'SELL']:
            errors.append(f"Invalid direction: {direction}")
        
        # Validate entry price
        entry = signal.get('entry')
        if entry is not None:
            try:
                entry_float = float(entry)
                if entry_float <= 0:
                    errors.append(f"Invalid entry price: {entry}")
            except (ValueError, TypeError):
                errors.append(f"Entry price not numeric: {entry}")
        
        if errors:
            error_msg = ", ".join(errors)
            logger.warning(f"{TE_001_INVALID_SIGNAL}: {error_msg}")
            return False, error_msg
        
        return True, ""
        
    except Exception as e:
        logger.error(f"Error validating signal: {e}")
        return False, str(e)


def format_error_notification(error_code: str, error_msg: str, context: Dict = None) -> str:
    """
    Format error for user notification
    
    Args:
        error_code: Error code (e.g., TG-001)
        error_msg: Error message
        context: Additional context dict
    
    Returns:
        Formatted message string
    """
    try:
        severity = ERROR_SEVERITY.get(error_code, SEVERITY_INFO)
        emoji = SEVERITY_EMOJI.get(severity, "⚪")
        
        message = (
            f"{emoji} <b>ERROR ALERT</b>\n\n"
            f"<b>Code:</b> <code>{error_code}</code>\n"
            f"<b>Severity:</b> {severity}\n"
            f"<b>Message:</b> {error_msg}\n"
            f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Add context if provided
        if context:
            message += "\n\n<b>Details:</b>\n"
            for key, value in context.items():
                message += f"• {key}: {value}\n"
        
        # Add auto-recovery info
        if AUTO_RECOVERY_ENABLED.get(error_code, False):
            message += "\n✅ Auto-recovery will be attempted"
        else:
            message += "\n⚠️ Manual intervention required"
        
        return message
        
    except Exception as e:
        logger.error(f"Error formatting error notification: {e}")
        return f"Error: {error_code} - {error_msg}"


def get_mt5_error_description(error_code: int) -> str:
    """
    Get human-readable description for MT5 error code
    
    Args:
        error_code: MT5 error code
    
    Returns:
        Error description string
    """
    return MT5_ERROR_CODES.get(error_code, f"Unknown MT5 error {error_code}")


def should_auto_recover(error_code: str) -> bool:
    """
    Check if error should attempt auto-recovery
    
    Args:
        error_code: Error code
    
    Returns:
        True if auto-recovery enabled
    """
    return AUTO_RECOVERY_ENABLED.get(error_code, False)


class ErrorRateLimiter:
    """
    Prevent error notification spam
    """
    
    def __init__(self, max_per_minute: int = 5):
        """
        Initialize rate limiter
        
        Args:
            max_per_minute: Max errors per code per minute
        """
        self.max_per_minute = max_per_minute
        self.error_timestamps = defaultdict(list)
        logger.info(f"ErrorRateLimiter initialized with {max_per_minute}/min limit")
    
    def should_notify(self, error_code: str) -> bool:
        """
        Check if error should be notified based on rate limit
        
        Args:
            error_code: Error code
        
        Returns:
            True if should notify
        """
        try:
            now = datetime.now()
            cutoff = now - timedelta(minutes=1)
            
            # Clean old timestamps
            self.error_timestamps[error_code] = [
                ts for ts in self.error_timestamps[error_code]
                if ts > cutoff
            ]
            
            # Check rate
            if len(self.error_timestamps[error_code]) >= self.max_per_minute:
                logger.debug(f"Rate limit reached for {error_code}")
                return False
            
            # Record timestamp
            self.error_timestamps[error_code].append(now)
            return True
            
        except Exception as e:
            logger.error(f"Error in rate limiter: {e}")
            return True  # Fail open
    
    def reset(self, error_code: str = None):
        """
        Reset rate limiter
        
        Args:
            error_code: Specific code to reset, or None for all
        """
        if error_code:
            self.error_timestamps[error_code] = []
        else:
            self.error_timestamps.clear()


# Global instances
signal_deduplicator = SignalDeduplicator(ttl_seconds=60)
error_rate_limiter = ErrorRateLimiter(max_per_minute=5)


def split_long_message(message: str, max_length: int = MAX_MESSAGE_LENGTH) -> list:
    """
    Split long message into chunks (TG-005)
    
    Args:
        message: Message text
        max_length: Maximum length per chunk
    
    Returns:
        List of message chunks
    """
    try:
        if len(message) <= max_length:
            return [message]
        
        chunks = []
        current_chunk = ""
        
        # Split by lines to preserve formatting
        lines = message.split('\n')
        
        for line in lines:
            # If single line is too long, split it
            if len(line) > max_length:
                # If we have content in current chunk, save it
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                # Split the long line
                for i in range(0, len(line), max_length):
                    chunks.append(line[i:i+max_length])
            
            # Check if adding line exceeds limit
            elif len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                if current_chunk:
                    current_chunk += "\n" + line
                else:
                    current_chunk = line
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        logger.info(f"{TG_005_MESSAGE_TOO_LONG}: Split message into {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"Error splitting message: {e}")
        return [message[:max_length]]


def truncate_callback_data(callback_data: str, max_length: int = MAX_CALLBACK_DATA_LENGTH) -> str:
    """
    Truncate callback data to Telegram limit
    
    Args:
        callback_data: Callback data string
        max_length: Maximum length
    
    Returns:
        Truncated string
    """
    if len(callback_data) <= max_length:
        return callback_data
    
    logger.warning(f"{MN_002_BUILD_ERROR}: Callback data truncated from {len(callback_data)} to {max_length}")
    return callback_data[:max_length]


def truncate_button_text(text: str, max_length: int = MAX_BUTTON_TEXT_LENGTH) -> str:
    """
    Truncate button text to Telegram limit
    
    Args:
        text: Button text
        max_length: Maximum length
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    logger.debug(f"Button text truncated from {len(text)} to {max_length}")
    return text[:max_length-3] + "..."


class RiskLimitChecker:
    """
    Check risk limits to prevent excessive losses (TE-002)
    """
    
    def __init__(self, daily_loss_limit: float = 500.0, lifetime_loss_limit: float = 5000.0):
        """
        Initialize risk limit checker
        
        Args:
            daily_loss_limit: Maximum daily loss allowed (USD)
            lifetime_loss_limit: Maximum lifetime loss allowed (USD)
        """
        self.daily_loss_limit = daily_loss_limit
        self.lifetime_loss_limit = lifetime_loss_limit
        self.daily_pnl = 0.0
        self.lifetime_pnl = 0.0
        self.trade_count_today = 0
        logger.info(f"RiskLimitChecker initialized: Daily limit ${daily_loss_limit}, Lifetime limit ${lifetime_loss_limit}")
    
    def check_risk_limits(self) -> Tuple[bool, str]:
        """
        Check if risk limits are exceeded
        
        Returns:
            Tuple of (can_trade, reason)
        """
        try:
            # Check daily loss limit
            if self.daily_pnl <= -self.daily_loss_limit:
                logger.warning(f"{TE_002_RISK_LIMIT_EXCEEDED}: Daily loss limit reached (${self.daily_pnl:.2f})")
                return False, f"Daily loss limit exceeded (${abs(self.daily_pnl):.2f} / ${self.daily_loss_limit})"
            
            # Check lifetime loss limit
            if self.lifetime_pnl <= -self.lifetime_loss_limit:
                logger.critical(f"{TE_002_RISK_LIMIT_EXCEEDED}: Lifetime loss limit reached (${self.lifetime_pnl:.2f})")
                return False, f"Lifetime loss limit exceeded (${abs(self.lifetime_pnl):.2f} / ${self.lifetime_loss_limit})"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error checking risk limits: {e}")
            return True, ""  # Fail open
    
    def update_pnl(self, trade_pnl: float):
        """
        Update P&L tracking
        
        Args:
            trade_pnl: Trade profit/loss
        """
        try:
            self.daily_pnl += trade_pnl
            self.lifetime_pnl += trade_pnl
            self.trade_count_today += 1
            logger.debug(f"P&L updated: Daily ${self.daily_pnl:.2f}, Lifetime ${self.lifetime_pnl:.2f}")
        except Exception as e:
            logger.error(f"Error updating P&L: {e}")
    
    def reset_daily(self):
        """Reset daily counters (call at start of day)"""
        self.daily_pnl = 0.0
        self.trade_count_today = 0
        logger.info("Daily risk limits reset")
    
    def get_status(self) -> Dict:
        """Get current risk status"""
        return {
            'daily_pnl': self.daily_pnl,
            'daily_limit': self.daily_loss_limit,
            'daily_remaining': self.daily_loss_limit + self.daily_pnl,
            'lifetime_pnl': self.lifetime_pnl,
            'lifetime_limit': self.lifetime_loss_limit,
            'lifetime_remaining': self.lifetime_loss_limit + self.lifetime_pnl,
            'trades_today': self.trade_count_today
        }


# Global instance
risk_limit_checker = RiskLimitChecker()
