"""
FastAPI Application Entry Point for Zepix Trading Bot
Runs on port 80 with full integration
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

# Import bot components
from src.config import Config
from src.clients.mt5_client import MT5Client
from src.managers.risk_manager import RiskManager
from src.core.trading_engine import TradingEngine
from src.processors.alert_processor import AlertProcessor
from src.managers.session_manager import SessionManager
from src.database import TradeDatabase
from src.telegram.core.multi_bot_manager import MultiBotManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_api.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("API")

# Create FastAPI app
app = FastAPI(
    title="Zepix Trading Bot API",
    description="Automated Trading Bot with V3/V6 Logic, Re-entry, Profit Chains, Telegram Integration",
    version="2.0.0"
)

# Global bot components
config = None
mt5_client = None
trading_engine = None
telegram_manager = None


@app.on_event("startup")
async def startup_event():
    """Initialize bot components on startup"""
    global config, mt5_client, trading_engine, telegram_manager
    
    logger.info("=" * 60)
    logger.info("🚀 STARTING ZEPIX TRADING BOT API")
    logger.info("=" * 60)
    
    try:
        # 1. Load Configuration
        logger.info("Loading configuration...")
        config = Config()
        logger.info("✅ Configuration loaded")
        
        # 2. Initialize MT5 Client
        logger.info("Initializing MT5 client...")
        mt5_client = MT5Client(config)
        
        if mt5_client.initialize():
            logger.info("✅ MT5 connection established")
        else:
            logger.warning("⚠️  MT5 connection failed - running in restricted mode")
        
        # 3. Initialize Database & Session Manager
        logger.info("Initializing database...")
        db = TradeDatabase()
        session_manager = SessionManager(config, db, mt5_client)
        logger.info("✅ Database initialized")
        
        # 4. Initialize Risk Manager
        logger.info("Initializing risk manager...")
        risk_manager = RiskManager(config)
        risk_manager.set_mt5_client(mt5_client)
        logger.info("✅ Risk manager initialized")
        
        # 5. Initialize Telegram Manager
        logger.info("Initializing Telegram system...")
        telegram_manager = MultiBotManager(config.config)
        logger.info("✅ Telegram manager initialized")
        
        # 6. Initialize Alert Processor
        logger.info("Initializing alert processor...")
        alert_processor = AlertProcessor(config, telegram_bot=telegram_manager)
        logger.info("✅ Alert processor initialized")
        
        # 7. Initialize Trading Engine
        logger.info("Initializing trading engine...")
        trading_engine = TradingEngine(
            config, 
            risk_manager, 
            mt5_client, 
            telegram_manager, 
            alert_processor
        )
        logger.info("✅ Trading engine initialized")
        
        # 8. Wire Dependencies
        logger.info("Wiring dependencies...")
        telegram_manager.set_dependencies(trading_engine)
        logger.info("✅ Dependencies wired")
        
        # 9. Initialize Trading Engine
        logger.info("Starting trading engine...")
        await trading_engine.initialize()
        logger.info("✅ Trading engine started")
        
        # 10. Start Telegram Bots
        logger.info("Starting Telegram bots...")
        await telegram_manager.start()
        logger.info("✅ Telegram bots started")
        
        logger.info("=" * 60)
        logger.info("✅ BOT API READY")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down bot...")
    
    if mt5_client:
        mt5_client.shutdown()
    
    logger.info("Bot shutdown complete")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Zepix Trading Bot",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "V3 Combined Logic",
            "V6 Price Action (1m, 5m, 15m, 1h)",
            "SL Hunt Re-entry",
            "TP Re-entry",
            "Profit Booking Chains",
            "Dual Order System",
            "Multi-bot Telegram Integration",
            "Shadow Mode Testing"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    mt5_connected = mt5_client.is_connected() if mt5_client else False
    
    return {
        "status": "healthy",
        "mt5_connected": mt5_connected,
        "trading_engine": trading_engine is not None,
        "telegram": telegram_manager is not None
    }


@app.get("/status")
async def status():
    """Detailed status endpoint"""
    if not trading_engine:
        return {"status": "initializing"}
    
    # Get account info
    account_info = {}
    if mt5_client and mt5_client.is_connected():
        account_info = {
            "balance": mt5_client.get_account_balance(),
            "equity": mt5_client.get_account_equity(),
            "margin_free": mt5_client.get_account_free_margin(),
            "margin_level": mt5_client.get_account_margin_level()
        }
    
    # Get plugin status
    plugin_status = {}
    if hasattr(trading_engine, 'plugin_registry'):
        for plugin_id, plugin in trading_engine.plugin_registry.get_all_plugins().items():
            plugin_status[plugin_id] = {
                "enabled": plugin.enabled,
                "shadow_mode": plugin.shadow_mode,
                "name": plugin.plugin_name
            }
    
    return {
        "status": "running",
        "account": account_info,
        "plugins": plugin_status,
        "telegram_bots": {
            "controller": telegram_manager.controller_bot is not None,
            "notification": telegram_manager.notification_bot is not None,
            "analytics": telegram_manager.analytics_bot is not None
        }
    }


@app.post("/webhook")
async def webhook(request: Request):
    """
    Webhook endpoint for TradingView alerts
    
    Receives alerts and routes them to appropriate plugins
    """
    try:
        # Get raw alert
        raw_alert = await request.json()
        
        logger.info(f"📨 Webhook received: {raw_alert.get('type', 'unknown')}")
        
        if not trading_engine:
            return JSONResponse(
                status_code=503,
                content={"status": "error", "message": "Trading engine not initialized"}
            )
        
        # Process alert through trading engine
        result = await trading_engine.process_alert(raw_alert)
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "result": result}
        )
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.get("/config")
async def get_config():
    """Get current configuration (sensitive data masked)"""
    if not config:
        return {"status": "not initialized"}
    
    # Return safe config
    safe_config = {
        "symbols": list(config.get("symbol_mapping", {}).keys()),
        "v3_enabled": config.get("v3_integration", {}).get("enabled", False),
        "plugin_system_enabled": config.get("plugin_system", {}).get("enabled", False),
        "plugins": {}
    }
    
    # Add plugin status
    plugins = config.get("plugins", {})
    for plugin_name, plugin_config in plugins.items():
        if plugin_name != "_template":
            safe_config["plugins"][plugin_name] = {
                "enabled": plugin_config.get("enabled", False),
                "shadow_mode": plugin_config.get("shadow_mode", False)
            }
    
    return safe_config


def main():
    """Run the API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Zepix Trading Bot API")
    parser.add_argument("--port", type=int, default=80, help="Port to run on (default: 80)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    logger.info(f"Starting API server on {args.host}:{args.port}")
    
    if args.port == 80:
        logger.warning("Running on port 80 may require administrator privileges!")
    
    uvicorn.run(
        "src.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
