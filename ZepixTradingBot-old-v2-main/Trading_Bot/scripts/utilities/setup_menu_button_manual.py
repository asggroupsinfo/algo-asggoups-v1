"""
MANUAL MENU BUTTON SETUP SCRIPT
Run this to manually setup menu button on Telegram
"""

import requests
import json
import sys

def setup_telegram_menu_button():
    """Manually setup Telegram menu button with all commands"""
    
    # Read token from config
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            token = config.get('telegram_token')
            if not token:
                print("❌ No Telegram token found in config")
                return False
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        print(f"ℹ️  Trying to read token from environment or alternate source...")
        # Try to import from bot's config
        try:
            import sys
            sys.path.insert(0, 'src')
            from config.config_manager import Config
            cfg = Config()
            token = cfg.get('telegram_token')
            if not token:
                print("❌ No token found")
                return False
        except Exception as e2:
            print(f"❌ Alternate config load failed: {e2}")
            return False
    
    base_url = f"https://api.telegram.org/bot{token}"
    
    # Complete command list (78 commands in 12 categories)
    commands = [
        # CATEGORY 1: MAIN CONTROLS
        {"command": "start", "description": "🚀 Start/Restart the bot"},
        {"command": "status", "description": "📊 Bot status & overview"},
        {"command": "dashboard", "description": "📱 Main dashboard"},
        {"command": "pause", "description": "⏸️ Pause all trading"},
        {"command": "resume", "description": "▶️ Resume trading"},
        {"command": "panic", "description": "🚨 Emergency close all positions"},
        
        # CATEGORY 2: PERFORMANCE & ANALYTICS
        {"command": "performance", "description": "💰 Performance report"},
        {"command": "performance_report", "description": "📈 Detailed performance"},
        {"command": "stats", "description": "📊 Trading statistics"},
        {"command": "trades", "description": "📋 View all trades"},
        {"command": "pair_report", "description": "📊 Symbol pair analysis"},
        {"command": "strategy_report", "description": "🎯 Strategy performance"},
        
        # CATEGORY 3: PLUGIN CONTROL
        {"command": "logic_control", "description": "⚙️ Plugin management"},
        {"command": "logic_status", "description": "📊 Plugin status"},
        {"command": "logic1_on", "description": "✅ Enable LOGIC1"},
        {"command": "logic1_off", "description": "❌ Disable LOGIC1"},
        {"command": "logic2_on", "description": "✅ Enable LOGIC2"},
        {"command": "logic2_off", "description": "❌ Disable LOGIC2"},
        {"command": "logic3_on", "description": "✅ Enable LOGIC3"},
        {"command": "logic3_off", "description": "❌ Disable LOGIC3"},
        {"command": "view_logic_settings", "description": "📋 View plugin settings"},
        
        # CATEGORY 4: TREND MANAGEMENT
        {"command": "set_trend", "description": "📈 Set trend manually"},
        {"command": "set_auto", "description": "🔄 Auto trend detection"},
        {"command": "show_trends", "description": "📊 Show all trends"},
        {"command": "trend_matrix", "description": "🎯 Trend matrix view"},
        {"command": "trend_mode", "description": "⚙️ Trend mode settings"},
        {"command": "reset_timeframe_default", "description": "🔄 Reset timeframe defaults"},
        
        # CATEGORY 5: RISK MANAGEMENT
        {"command": "lot_size_status", "description": "💰 Current lot size"},
        {"command": "set_lot_size", "description": "⚙️ Set lot size"},
        {"command": "view_risk_caps", "description": "🛡️ View risk limits"},
        {"command": "clear_loss_data", "description": "🗑️ Clear loss data"},
        {"command": "clear_daily_loss", "description": "🗑️ Clear daily loss"},
        
        # CATEGORY 6: SL/TP SYSTEM
        {"command": "tp_system", "description": "🎯 TP system status"},
        {"command": "tp_report", "description": "📊 TP performance report"},
        {"command": "sl_hunt", "description": "🎯 SL Hunt settings"},
        {"command": "sl_status", "description": "📊 SL system status"},
        {"command": "sl_system_change", "description": "⚙️ Change SL system"},
        {"command": "sl_system_on", "description": "✅ Enable SL system"},
        {"command": "view_sl_config", "description": "📋 View SL configuration"},
        {"command": "set_symbol_sl", "description": "⚙️ Set symbol-specific SL"},
        
        # CATEGORY 7: RE-ENTRY SYSTEM
        {"command": "exit_continuation", "description": "🔄 Exit continuation"},
        {"command": "reentry_config", "description": "⚙️ Re-entry configuration"},
        {"command": "set_monitor_interval", "description": "⏱️ Set monitor interval"},
        {"command": "set_sl_offset", "description": "📏 Set SL offset"},
        {"command": "set_cooldown", "description": "⏳ Set cooldown period"},
        {"command": "set_recovery_time", "description": "🔄 Set recovery time"},
        {"command": "set_max_levels", "description": "📊 Set max re-entry levels"},
        {"command": "set_sl_reduction", "description": "📉 Set SL reduction %"},
        {"command": "reset_reentry_config", "description": "🔄 Reset re-entry config"},
        
        # CATEGORY 8: PROFIT BOOKING SYSTEM
        {"command": "profit_stats", "description": "💰 Profit booking stats"},
        {"command": "toggle_profit_booking", "description": "🔄 Toggle profit booking"},
        {"command": "set_profit_targets", "description": "🎯 Set profit targets"},
        {"command": "profit_chains", "description": "⛓️ View profit chains"},
        {"command": "stop_profit_chain", "description": "⏸️ Stop profit chain"},
        {"command": "stop_all_profit_chains", "description": "⏹️ Stop all chains"},
        {"command": "close_profit_chain", "description": "❌ Close profit chain"},
        {"command": "set_chain_multipliers", "description": "📊 Set chain multipliers"},
        {"command": "set_sl_reductions", "description": "📉 Set SL reductions"},
        {"command": "profit_config", "description": "⚙️ Profit system config"},
        {"command": "chains", "description": "⛓️ Chain status"},
        
        # CATEGORY 9: PROFIT SL PROTECTION
        {"command": "profit_sl_status", "description": "📊 Profit SL status"},
        {"command": "profit_sl_mode", "description": "⚙️ Profit SL mode"},
        {"command": "enable_profit_sl", "description": "✅ Enable profit SL"},
        {"command": "disable_profit_sl", "description": "❌ Disable profit SL"},
        {"command": "set_sl1_1", "description": "📊 Set SL1.1 level"},
        {"command": "set_sl2_1", "description": "📊 Set SL2.1 level"},
        {"command": "set_profit_sl", "description": "⚙️ Configure profit SL"},
        {"command": "reset_profit_sl", "description": "🔄 Reset profit SL"},
        
        # CATEGORY 10: AUTONOMOUS/FINE-TUNE SYSTEM
        {"command": "fine_tune", "description": "🎛️ Fine-tune dashboard"},
        {"command": "autonomous_dashboard", "description": "🤖 Autonomous system"},
        {"command": "autonomous_status", "description": "📊 Autonomous status"},
        {"command": "profit_protection", "description": "🛡️ Profit protection"},
        {"command": "sl_reduction", "description": "📉 SL reduction system"},
        {"command": "recovery_windows", "description": "🔄 Recovery windows"},
        {"command": "shield", "description": "🛡️ Reverse shield v3.0"},
        
        # CATEGORY 11: SIMULATION & TESTING
        {"command": "simulation_mode", "description": "🎮 Simulation mode"},
        {"command": "signal_status", "description": "📡 Signal status"},
        
        # CATEGORY 12: HELP & INFO
        {"command": "help", "description": "🆘 Help & all commands"}
    ]
    
    print(f"\n🔧 Setting up menu button with {len(commands)} commands...")
    print(f"📡 Telegram API: {base_url[:50]}...")
    
    # Call Telegram API
    try:
        url = f"{base_url}/setMyCommands"
        payload = {"commands": commands}
        
        print(f"\n📤 Sending request to Telegram...")
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print(f"\n✅ SUCCESS! Menu button configured!")
                print(f"✅ Total commands: {len(commands)}")
                print(f"✅ Categories: 12")
                print(f"\n📱 Now open your Telegram bot:")
                print(f"   1. Look for (≡) button next to input field")
                print(f"   2. Click it to see all {len(commands)} commands")
                print(f"   3. Commands are organized in categories")
                return True
            else:
                print(f"\n❌ Telegram API returned error:")
                print(f"   {result}")
                return False
        else:
            print(f"\n❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timeout - Check internet connection")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("  TELEGRAM MENU BUTTON SETUP SCRIPT")
    print("="*70)
    
    success = setup_telegram_menu_button()
    
    if success:
        print("\n" + "="*70)
        print("  ✅ MENU BUTTON SETUP COMPLETE")
        print("="*70)
        print("\n📌 NEXT STEPS:")
        print("   1. Open your Telegram bot chat")
        print("   2. Look for (≡) menu button next to typing area")
        print("   3. Click (≡) to open command list")
        print("   4. You'll see all 78 commands organized!")
        print("\n⚠️  NOTE: Menu button is CLICK-TO-OPEN (not fixed)")
        print("   - It's a small (≡) icon, not always-visible buttons")
        print("   - Click it when you need commands")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("  ❌ SETUP FAILED")
        print("="*70)
        print("\n🔍 TROUBLESHOOTING:")
        print("   1. Check config/config.json has valid telegram_token")
        print("   2. Verify bot token with @BotFather")
        print("   3. Check internet connection")
        print("   4. Try running again")
        print("="*70 + "\n")
        sys.exit(1)
