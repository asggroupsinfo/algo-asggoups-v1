#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
START BOT ON PORT 80 WITH FULL TESTING
Deploys Zepix Trading Bot with comprehensive verification
"""
import os
import sys
import time
import logging
import subprocess
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_deployment.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Deployment")


def print_banner(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def check_prerequisites():
    """Check if all prerequisites are met"""
    print_banner("CHECKING PREREQUISITES")
    
    checks = []
    
    # Python version
    python_version = sys.version_info
    checks.append(("Python 3.8+", python_version >= (3, 8)))
    print(f"  Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Dependencies
    try:
        import MetaTrader5
        checks.append(("MetaTrader5", True))
        print("  ✅ MetaTrader5 installed")
    except ImportError:
        checks.append(("MetaTrader5", False))
        print("  ❌ MetaTrader5 NOT installed")
    
    try:
        from telegram import Bot
        checks.append(("python-telegram-bot", True))
        print("  ✅ python-telegram-bot installed")
    except ImportError:
        checks.append(("python-telegram-bot", False))
        print("  ❌ python-telegram-bot NOT installed")
    
    try:
        import fastapi
        checks.append(("FastAPI", True))
        print("  ✅ FastAPI installed")
    except ImportError:
        checks.append(("FastAPI", False))
        print("  ❌ FastAPI NOT installed")
    
    # Configuration file
    config_exists = (project_root / "config" / "config.json").exists()
    checks.append(("Config file", config_exists))
    print(f"  {'✅' if config_exists else '❌'} Config file exists")
    
    all_ok = all(check[1] for check in checks)
    
    if not all_ok:
        print("\n  ⚠️  PREREQUISITES NOT MET!")
        print("  Please install missing dependencies:")
        print("    pip install -r requirements.txt")
        return False
    
    print("\n  ✅ ALL PREREQUISITES MET")
    return True


def run_production_tests():
    """Run production readiness tests"""
    print_banner("RUNNING PRODUCTION READINESS TESTS")
    
    try:
        # Run the production readiness test
        result = subprocess.run(
            [sys.executable, "tests/PRODUCTION_READINESS_TEST.py"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n  ✅ ALL PRODUCTION TESTS PASSED")
            return True
        else:
            print("\n  ⚠️  SOME TESTS FAILED")
            print("  Review errors above before proceeding")
            return False
            
    except Exception as e:
        print(f"  ❌ Error running tests: {e}")
        return False


def test_shadow_mode():
    """Test shadow mode is working"""
    print_banner("TESTING SHADOW MODE (SIMULATION)")
    
    try:
        from src.config import Config
        from src.core.shadow_mode_manager import ShadowModeManager
        
        config = Config()
        shadow_config = config.get("shadow_mode", {})
        shadow_manager = ShadowModeManager(shadow_config)
        
        print(f"  Current Mode: {shadow_manager.execution_mode.value}")
        print(f"  Plugins Execute: {shadow_manager.plugins_execute}")
        print(f"  Legacy Executes: {shadow_manager.legacy_executes}")
        
        if shadow_manager.plugins_execute or shadow_manager.legacy_executes:
            print("\n  ✅ Shadow Mode Active - Safe for testing")
            return True
        else:
            print("\n  ⚠️  No execution mode enabled")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing shadow mode: {e}")
        return False


def start_bot_on_port_80():
    """Start the bot on port 80"""
    print_banner("STARTING BOT ON PORT 80")
    
    try:
        # Check if port 80 is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 80))
        sock.close()
        
        if result == 0:
            print("  ⚠️  Port 80 is already in use!")
            print("  Please stop the existing service first")
            return False
        
        print("  ✅ Port 80 is available")
        
        # Start bot with FastAPI on port 80
        print("\n  Starting FastAPI server on port 80...")
        print("  Note: This may require administrator privileges on Windows")
        
        # Create startup command
        cmd = [
            sys.executable,
            "-m", "uvicorn",
            "src.main:app",
            "--host", "0.0.0.0",
            "--port", "80",
            "--reload"
        ]
        
        print(f"\n  Command: {' '.join(cmd)}")
        print("\n  Press Ctrl+C to stop the bot")
        print("  " + "=" * 76)
        
        # Start the bot
        process = subprocess.Popen(cmd, cwd=project_root)
        
        # Wait a bit to see if it starts
        time.sleep(3)
        
        if process.poll() is None:
            print("\n  ✅ BOT STARTED SUCCESSFULLY ON PORT 80")
            print("\n  API Endpoints:")
            print("    http://localhost:80/health")
            print("    http://localhost:80/status")
            print("    http://localhost:80/webhook (POST)")
            
            print("\n  Telegram Bot:")
            print("    Send /start to your bot to test")
            
            return process
        else:
            print("\n  ❌ BOT FAILED TO START")
            return None
            
    except Exception as e:
        print(f"  ❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_bot_running():
    """Test if bot is responding"""
    print_banner("TESTING BOT ENDPOINTS")
    
    import requests
    
    endpoints = [
        ("Health Check", "http://localhost:80/health"),
        ("Status", "http://localhost:80/status"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name}: OK")
                print(f"     Response: {response.json()}")
            else:
                print(f"  ⚠️  {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")


def main():
    print("\n" + "=" * 80)
    print("  ZEPIX TRADING BOT - PORT 80 DEPLOYMENT WITH TESTING")
    print("  Full Production Readiness Verification")
    print("=" * 80)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  Cannot proceed without prerequisites")
        return 1
    
    # Step 2: Run production tests
    print("\nProceed with production tests? (y/n): ", end='')
    if input().lower() != 'y':
        print("Deployment cancelled")
        return 0
    
    tests_passed = run_production_tests()
    
    if not tests_passed:
        print("\nTests failed. Proceed anyway? (y/n): ", end='')
        if input().lower() != 'y':
            print("Deployment cancelled")
            return 0
    
    # Step 3: Test shadow mode
    test_shadow_mode()
    
    # Step 4: Start bot
    print("\nStart bot on port 80? (y/n): ", end='')
    if input().lower() != 'y':
        print("Deployment cancelled")
        return 0
    
    bot_process = start_bot_on_port_80()
    
    if not bot_process:
        print("\n❌ DEPLOYMENT FAILED")
        return 1
    
    # Step 5: Wait and test
    time.sleep(5)
    test_bot_running()
    
    print("\n" + "=" * 80)
    print("  ✅ BOT IS RUNNING ON PORT 80")
    print("=" * 80)
    print("\n  Next Steps:")
    print("    1. Open Telegram and send /start to your bot")
    print("    2. Test menu navigation")
    print("    3. Send a test webhook alert")
    print("    4. Monitor logs in bot_deployment.log")
    print("    5. Press Ctrl+C here to stop the bot")
    
    try:
        # Keep script running
        bot_process.wait()
    except KeyboardInterrupt:
        print("\n\nStopping bot...")
        bot_process.terminate()
        time.sleep(2)
        if bot_process.poll() is None:
            bot_process.kill()
        print("Bot stopped")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
