"""
Auto-Recovery System

Automatic recovery procedures for critical errors.
Based on: Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional, Callable

from .error_codes import *

logger = logging.getLogger(__name__)


class AutoRecoveryManager:
    """
    Manages automatic recovery procedures
    """
    
    def __init__(self, mt5_client=None, database=None, telegram_bot=None):
        """
        Initialize auto-recovery manager
        
        Args:
            mt5_client: MT5 client instance
            database: Database instance
            telegram_bot: Telegram bot instance
        """
        self.mt5_client = mt5_client
        self.database = database
        self.telegram_bot = telegram_bot
        self.running = False
        self.recovery_task = None
        self.admin_notifier = None
        
        self.mt5_reconnect_attempts = 0
        self.db_reconnect_attempts = 0
        self.tg_restart_attempts = 0
        
        logger.info("AutoRecoveryManager initialized")
    
    def set_admin_notifier(self, notifier):
        """Set admin notifier for error alerts"""
        self.admin_notifier = notifier
    
    async def start(self):
        """Start auto-recovery loop"""
        if self.running:
            logger.warning("Auto-recovery already running")
            return
        
        self.running = True
        self.recovery_task = asyncio.create_task(self._recovery_loop())
        logger.info("✅ Auto-recovery system started")
    
    async def stop(self):
        """Stop auto-recovery loop"""
        self.running = False
        if self.recovery_task:
            self.recovery_task.cancel()
            try:
                await self.recovery_task
            except asyncio.CancelledError:
                pass
        logger.info("Auto-recovery system stopped")
    
    async def _recovery_loop(self):
        """Main recovery loop - checks every 60 seconds"""
        while self.running:
            try:
                # Check MT5 connection
                await self._check_mt5_connection()
                
                # Check database connection
                await self._check_database_connection()
                
                # Check Telegram health
                await self._check_telegram_health()
                
                # Wait 60 seconds
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in recovery loop: {e}")
                await asyncio.sleep(60)
    
    async def _check_mt5_connection(self):
        """Check and recover MT5 connection (MT-001)"""
        if not self.mt5_client:
            return
        
        try:
            is_connected = await self._safe_check_mt5()
            
            if not is_connected:
                logger.warning(f"{MT_001_CONNECTION_FAILED}: MT5 disconnected, attempting recovery")
                success = await self.recover_mt5_connection()
                
                if success:
                    self.mt5_reconnect_attempts = 0
                    logger.info("✅ MT5 connection recovered")
                else:
                    self.mt5_reconnect_attempts += 1
                    logger.error(f"❌ MT5 recovery failed (attempt {self.mt5_reconnect_attempts}/{MAX_MT5_RECONNECT_ATTEMPTS})")
                    
                    # Notify admin after max attempts
                    if self.mt5_reconnect_attempts >= MAX_MT5_RECONNECT_ATTEMPTS:
                        if self.admin_notifier:
                            await self.admin_notifier.notify_error(
                                MT_001_CONNECTION_FAILED,
                                f"MT5 connection failed after {MAX_MT5_RECONNECT_ATTEMPTS} attempts",
                                SEVERITY_CRITICAL,
                                {'attempts': self.mt5_reconnect_attempts}
                            )
        
        except Exception as e:
            logger.error(f"Error checking MT5 connection: {e}")
    
    async def _safe_check_mt5(self) -> bool:
        """Safely check MT5 connection"""
        try:
            if hasattr(self.mt5_client, 'is_connected'):
                if asyncio.iscoroutinefunction(self.mt5_client.is_connected):
                    return await self.mt5_client.is_connected()
                else:
                    return self.mt5_client.is_connected()
            elif hasattr(self.mt5_client, 'connected'):
                return self.mt5_client.connected
            else:
                return False
        except Exception:
            return False
    
    async def recover_mt5_connection(self) -> bool:
        """
        Attempt to recover MT5 connection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.mt5_client:
                return False
            
            # Disconnect first
            if hasattr(self.mt5_client, 'disconnect'):
                try:
                    if asyncio.iscoroutinefunction(self.mt5_client.disconnect):
                        await self.mt5_client.disconnect()
                    else:
                        self.mt5_client.disconnect()
                except Exception as e:
                    logger.debug(f"Disconnect error (expected): {e}")
            
            # Wait before reconnect
            await asyncio.sleep(2)
            
            # Reconnect
            if hasattr(self.mt5_client, 'connect'):
                if asyncio.iscoroutinefunction(self.mt5_client.connect):
                    result = await self.mt5_client.connect()
                else:
                    result = self.mt5_client.connect()
                return bool(result)
            elif hasattr(self.mt5_client, 'initialize'):
                if asyncio.iscoroutinefunction(self.mt5_client.initialize):
                    result = await self.mt5_client.initialize()
                else:
                    result = self.mt5_client.initialize()
                return bool(result)
            
            return False
            
        except Exception as e:
            logger.error(f"MT5 recovery error: {e}")
            return False
    
    async def _check_database_connection(self):
        """Check and recover database connection (DB-001)"""
        if not self.database:
            return
        
        try:
            is_connected = await self._safe_check_database()
            
            if not is_connected:
                logger.warning(f"{DB_001_CONNECTION_ERROR}: Database disconnected, attempting recovery")
                success = await self.recover_database_connection()
                
                if success:
                    self.db_reconnect_attempts = 0
                    logger.info("✅ Database connection recovered")
                else:
                    self.db_reconnect_attempts += 1
                    logger.error(f"❌ Database recovery failed (attempt {self.db_reconnect_attempts})")
                    
                    # Notify admin after 3 attempts
                    if self.db_reconnect_attempts >= 3:
                        if self.admin_notifier:
                            await self.admin_notifier.notify_error(
                                DB_001_CONNECTION_ERROR,
                                f"Database connection failed after {self.db_reconnect_attempts} attempts",
                                SEVERITY_CRITICAL,
                                {'attempts': self.db_reconnect_attempts}
                            )
        
        except Exception as e:
            logger.error(f"Error checking database connection: {e}")
    
    async def _safe_check_database(self) -> bool:
        """Safely check database connection"""
        try:
            if hasattr(self.database, 'test_connection'):
                if asyncio.iscoroutinefunction(self.database.test_connection):
                    return await self.database.test_connection()
                else:
                    return self.database.test_connection()
            elif hasattr(self.database, 'is_connected'):
                if asyncio.iscoroutinefunction(self.database.is_connected):
                    return await self.database.is_connected()
                else:
                    return self.database.is_connected()
            else:
                # Try simple query
                if hasattr(self.database, 'execute'):
                    result = self.database.execute("SELECT 1")
                    return result is not None
                return False
        except Exception:
            return False
    
    async def recover_database_connection(self) -> bool:
        """
        Attempt to recover database connection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.database:
                return False
            
            # Close existing connection
            if hasattr(self.database, 'close'):
                try:
                    if asyncio.iscoroutinefunction(self.database.close):
                        await self.database.close()
                    else:
                        self.database.close()
                except Exception as e:
                    logger.debug(f"Close error (expected): {e}")
            
            # Wait before reconnect
            await asyncio.sleep(1)
            
            # Reconnect
            if hasattr(self.database, 'connect'):
                if asyncio.iscoroutinefunction(self.database.connect):
                    result = await self.database.connect()
                else:
                    result = self.database.connect()
                return bool(result)
            elif hasattr(self.database, 'initialize'):
                if asyncio.iscoroutinefunction(self.database.initialize):
                    result = await self.database.initialize()
                else:
                    result = self.database.initialize()
                return bool(result)
            
            return False
            
        except Exception as e:
            logger.error(f"Database recovery error: {e}")
            return False
    
    async def _check_telegram_health(self):
        """Check Telegram bot health (TG-001)"""
        if not self.telegram_bot:
            return
        
        try:
            is_healthy = await self._safe_check_telegram()
            
            if not is_healthy:
                logger.warning(f"{TG_001_HTTP_409}: Telegram unhealthy, attempting recovery")
                success = await self.recover_telegram()
                
                if success:
                    self.tg_restart_attempts = 0
                    logger.info("✅ Telegram connection recovered")
                else:
                    self.tg_restart_attempts += 1
                    logger.error(f"❌ Telegram recovery failed (attempt {self.tg_restart_attempts})")
        
        except Exception as e:
            logger.error(f"Error checking Telegram health: {e}")
    
    async def _safe_check_telegram(self) -> bool:
        """Safely check Telegram health"""
        try:
            if hasattr(self.telegram_bot, 'is_healthy'):
                if asyncio.iscoroutinefunction(self.telegram_bot.is_healthy):
                    return await self.telegram_bot.is_healthy()
                else:
                    return self.telegram_bot.is_healthy()
            elif hasattr(self.telegram_bot, 'running'):
                return self.telegram_bot.running
            else:
                # Try getMe() call
                if hasattr(self.telegram_bot, 'get_me'):
                    me = await self.telegram_bot.get_me()
                    return me is not None
                return True  # Assume healthy if no check available
        except Exception:
            return False
    
    async def recover_telegram(self) -> bool:
        """
        Attempt to recover Telegram connection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.telegram_bot:
                return False
            
            # Stop polling
            if hasattr(self.telegram_bot, 'stop_polling'):
                try:
                    if asyncio.iscoroutinefunction(self.telegram_bot.stop_polling):
                        await self.telegram_bot.stop_polling()
                    else:
                        self.telegram_bot.stop_polling()
                except Exception as e:
                    logger.debug(f"Stop polling error (expected): {e}")
            
            # Wait before restart
            await asyncio.sleep(3)
            
            # Restart polling
            if hasattr(self.telegram_bot, 'start_polling'):
                if asyncio.iscoroutinefunction(self.telegram_bot.start_polling):
                    await self.telegram_bot.start_polling()
                else:
                    self.telegram_bot.start_polling()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Telegram recovery error: {e}")
            return False


# Global instance (initialized in main)
auto_recovery_manager = None


def initialize_auto_recovery(mt5_client=None, database=None, telegram_bot=None):
    """
    Initialize global auto-recovery manager
    
    Args:
        mt5_client: MT5 client instance
        database: Database instance
        telegram_bot: Telegram bot instance
    
    Returns:
        AutoRecoveryManager instance
    """
    global auto_recovery_manager
    auto_recovery_manager = AutoRecoveryManager(mt5_client, database, telegram_bot)
    return auto_recovery_manager
