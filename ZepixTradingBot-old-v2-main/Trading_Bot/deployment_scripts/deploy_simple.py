"""
Simple FastAPI deployment on port 80
Bypasses complex dependencies for quick deployment
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from src.config import Config

# Create FastAPI app
app = FastAPI(
    title="Zepix Trading Bot API",
    description="Advanced MT5 Trading Bot with Telegram Integration",
    version="2.0.0"
)

# Global config
config = None

@app.on_event("startup")
async def startup_event():
    """Initialize configuration on startup"""
    global config
    try:
        config = Config()
        print("✅ Configuration loaded successfully")
        print(f"   MT5 Account: {config.get('mt5_login')}")
        print(f"   MT5 Server: {config.get('mt5_server')}")
        print(f"   Symbols: {len(config.get('symbol_mapping', {}))}")
        
        # Check plugins
        plugin_system = config.get('plugin_system', {})
        print(f"   Plugin System: {plugin_system.get('enabled')}")
        
        # Check V3
        v3_integration = config.get('v3_integration', {})
        print(f"   V3 Integration: {v3_integration.get('enabled')}")
        
        # Check Telegram
        print(f"   Telegram Controller: {'✅' if config.get('telegram_controller_token') else '❌'}")
        print(f"   Telegram Notification: {'✅' if config.get('telegram_notification_token') else '❌'}")
        print(f"   Telegram Analytics: {'✅' if config.get('telegram_analytics_token') else '❌'}")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "name": "Zepix Trading Bot",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "v3_combined_logic": True,
            "v6_price_action": True,
            "telegram_3bot": True,
            "autonomous_reentry": True,
            "profit_booking_chains": True,
            "shadow_mode": True
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    if config is None:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "reason": "Configuration not loaded"}
        )
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "config_loaded": True,
        "mt5_account": config.get('mt5_login'),
        "symbol_count": len(config.get('symbol_mapping', {}))
    }

@app.get("/status")
async def status():
    """Detailed status endpoint"""
    if config is None:
        return JSONResponse(
            status_code=503,
            content={"error": "Configuration not loaded"}
        )
    
    # Get configuration details
    plugin_system = config.get('plugin_system', {})
    v3_integration = config.get('v3_integration', {})
    re_entry = config.get('re_entry_config', {})
    autonomous = re_entry.get('autonomous_config', {})
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "configuration": {
            "mt5_login": config.get('mt5_login'),
            "mt5_server": config.get('mt5_server'),
            "symbols": list(config.get('symbol_mapping', {}).keys())
        },
        "plugin_system": {
            "enabled": plugin_system.get('enabled'),
            "use_delegation": plugin_system.get('use_delegation')
        },
        "v3_integration": {
            "enabled": v3_integration.get('enabled'),
            "aggressive_reversal_signals": v3_integration.get('aggressive_reversal_signals', [])
        },
        "re_entry_system": {
            "sl_hunt_enabled": re_entry.get('sl_hunt_reentry_enabled'),
            "tp_reentry_enabled": re_entry.get('tp_reentry_enabled'),
            "autonomous_enabled": re_entry.get('autonomous_enabled'),
            "max_chain_levels": re_entry.get('max_chain_levels')
        },
        "telegram": {
            "controller_configured": bool(config.get('telegram_controller_token')),
            "notification_configured": bool(config.get('telegram_notification_token')),
            "analytics_configured": bool(config.get('telegram_analytics_token'))
        }
    }

@app.post("/webhook")
async def webhook(request: Request):
    """TradingView webhook endpoint"""
    try:
        data = await request.json()
        
        # Log the webhook
        print(f"📨 Webhook received: {data}")
        
        # In production, this would be processed by AlertProcessor
        return {
            "status": "received",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Alert queued for processing (simulation mode)"
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.get("/config")
async def get_config():
    """Get sanitized configuration"""
    if config is None:
        return JSONResponse(
            status_code=503,
            content={"error": "Configuration not loaded"}
        )
    
    # Return sanitized config (no passwords/tokens)
    return {
        "mt5_server": config.get('mt5_server'),
        "symbols": list(config.get('symbol_mapping', {}).keys()),
        "features": {
            "v3_enabled": config.get('v3_integration', {}).get('enabled'),
            "plugin_system_enabled": config.get('plugin_system', {}).get('enabled'),
            "shadow_mode": config.get('shadow_mode_enabled', True)
        }
    }

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STARTING ZEPIX TRADING BOT ON PORT 80")
    print("=" * 70)
    print("\nEndpoints:")
    print("  GET  /          - Root status")
    print("  GET  /health    - Health check")
    print("  GET  /status    - Detailed status")
    print("  GET  /config    - Configuration")
    print("  POST /webhook   - TradingView alerts")
    print("\n" + "=" * 70)
    
    # Start server on port 80
    # Note: On Windows, port 80 may require admin privileges
    # If port 80 fails, it will try port 8080
    try:
        uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
    except PermissionError:
        print("\n⚠️  Port 80 requires administrator privileges")
        print("Starting on port 8080 instead...\n")
        uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
