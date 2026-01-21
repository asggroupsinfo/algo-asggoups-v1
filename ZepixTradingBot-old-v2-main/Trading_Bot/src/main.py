import os
import sys
import time
import logging
import signal
import threading
import asyncio

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.clients.mt5_client import MT5Client
from src.managers.risk_manager import RiskManager
from src.core.trading_engine import TradingEngine
# from src.clients.telegram_bot import TelegramBot # REMOVED
from src.processors.alert_processor import AlertProcessor
from src.managers.session_manager import SessionManager
from src.database import TradeDatabase

# ============================================================================
# ERROR HANDLING SYSTEM - DOCUMENT 09 IMPLEMENTATION
# ============================================================================
from src.utils.logging_config import setup_error_logging
from src.utils.auto_recovery import initialize_auto_recovery
from src.utils.admin_notifier import initialize_admin_notifier

# Setup enhanced error logging (3-tier: console + bot.log + errors.log)
setup_error_logging()

# Setup Logging to file and console (original logging kept for compatibility)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot_startup.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Main")

running_event = threading.Event()
running_event.set()

def handle_exit(signum, frame):
    print("\nShutdown signal received...")
    running_event.clear()

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def main():
    logger.info("-" * 50)
    logger.info("🚀 STARTING ZEPIX TRADING BOT V2.0")
    logger.info("-" * 50)
    
    try:
        # 1. Config
        logger.info("Loading Configuration...")
        config = Config()
        
        # 2. MT5 Client
        logger.info("Initializing MT5 Client...")
        mt5_client = MT5Client(config)
        
        if mt5_client.initialize():
            logger.info("✅ MT5 Connection Successful")
        else:
            logger.warning("⚠️ MT5 Connection Failed! Bot running in restricted mode.")

        # 3. Database & Session Manager (Dependency Injection)
        logger.info("Initializing Database & Session Manager...")
        db = TradeDatabase()
        session_manager = SessionManager(config, db, mt5_client)

        # 4. Risk Manager
        logger.info("Initializing Risk Manager...")
        risk_manager = RiskManager(config)
        risk_manager.set_mt5_client(mt5_client)
        
        # 5. Telegram System (NEW V6 SINGLE SOURCE OF TRUTH)
        # Replaces old TelegramBot wrapper with MultiBotManager
        logger.info("Initializing V6 Telegram System...")
        # from src.clients.telegram_bot import TelegramBot # REMOVED
        from src.telegram.core.multi_bot_manager import MultiBotManager
        
        # Use config for token management
        telegram_manager = MultiBotManager(config.config)
        # INJECT SESSION MANAGER (Critical fix for circular dependency)
        # telegram_bot.session_manager = session_manager
        # NOTE: SessionManager is already instantiated above. 
        # For now, if other components need it, they should import it directly 
        # or it should be managed by a core ServiceLocator if needed.
        # Ideally, Telegram shouldn't own SessionManager.
        
        # 6. Alert Processor (Updated to use new Manager)
        logger.info("Initializing Alert Processor...")
        # Alert processor needs an interface to send messages. 
        # We pass the telegram_manager which exposes send_message/alert methods based on routing.
        alert_processor = AlertProcessor(config, telegram_bot=telegram_manager) 
        
        # 7. Trading Engine (The Brain)
        logger.info("Initializing Trading Engine...")
        trading_engine = TradingEngine(config, risk_manager, mt5_client, telegram_manager, alert_processor)
        
        # 8. Wire Dependencies (Inverse Injection)
        logger.info("Wiring Dependencies...")
        telegram_manager.set_dependencies(trading_engine)
        
        # 9. Start Systems (Async Init)
        logger.info("Starting Subsystems...")
        
        # Run async initialization
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # ================================================================
            # ERROR HANDLING SYSTEM INITIALIZATION
            # ================================================================
            logger.info("Initializing Error Handling System...")
            
            # Initialize auto-recovery manager
            auto_recovery = initialize_auto_recovery(
                mt5_client=mt5_client,
                database=db,
                telegram_bot=telegram_manager
            )
            
            # Initialize admin notifier (get admin chat ID from config)
            admin_chat_id = config.config.get('telegram', {}).get('admin_chat_id')
            if admin_chat_id:
                admin_notifier = initialize_admin_notifier(
                    telegram_bot=telegram_manager,
                    admin_chat_id=admin_chat_id
                )
                auto_recovery.set_admin_notifier(admin_notifier)
                logger.info(f"✅ Admin notifications enabled for chat {admin_chat_id}")
            else:
                logger.warning("⚠️ Admin chat ID not configured - admin notifications disabled")
            
            # Start auto-recovery loop
            loop.run_until_complete(auto_recovery.start())
            logger.info("✅ Error handling system initialized")
            # ================================================================
            
            # Initialize Trading Engine
            loop.run_until_complete(trading_engine.initialize())
            
            # Start V6 Telegram Bots
            logger.info("Starting V6 Telegram Bots...")
            loop.run_until_complete(telegram_manager.start())
            
        except Exception as e:
            logger.error(f"Startup Init Error: {e}")
        
        # 10. Keep Alive (Replaces old threading polling)
        logger.info("✅ V6 BOT ARCHITECTURE ACTIVE. Waiting for signals...")
        
        logger.info("✅ BOT STARTUP COMPLETE. Waiting for commands.")
        
        # 11. Main Loop
        while running_event.is_set():
            time.sleep(1)
            
    except Exception as e:
        logger.critical(f"🔥 FATAL ERROR DURING STARTUP: {e}", exc_info=True)
        # Keep window open for debugging if needed (remove in prod)
        # time.sleep(10)
    finally:
        logger.info("Bot Shutdown.")

if __name__ == "__main__":
    main()
