"""Test Telegram bot integration and multi-bot architecture"""
import sys
sys.path.insert(0, '.')

from src.config import Config
from telegram import Bot
import asyncio

def test_telegram_bots():
    """Test all three Telegram bots (sync version for v13)"""
    config = Config()
    
    # Get tokens
    controller_token = config.get('telegram_controller_token')
    notification_token = config.get('telegram_notification_token')
    analytics_token = config.get('telegram_analytics_token')
    chat_id = config.get('telegram_chat_id')
    
    print("=" * 60)
    print("TELEGRAM 3-BOT ARCHITECTURE TEST")
    print("=" * 60)
    
    bots = {
        'Controller Bot': controller_token,
        'Notification Bot': notification_token,
        'Analytics Bot': analytics_token
    }
    
    results = []
    for bot_name, token in bots.items():
        if not token:
            print(f"\n❌ {bot_name}: No token configured")
            results.append(False)
            continue
            
        try:
            bot = Bot(token=token)
            bot_info = bot.get_me()
            print(f"\n✅ {bot_name}: Connected")
            print(f"   Username: @{bot_info.username}")
            print(f"   Bot ID: {bot_info.id}")
            print(f"   Name: {bot_info.first_name}")
            results.append(True)
        except Exception as e:
            print(f"\n❌ {bot_name}: Connection failed")
            print(f"   Error: {str(e)}")
            results.append(False)
    
    # Test sending a test message
    print("\n" + "=" * 60)
    print("TESTING MESSAGE SENDING")
    print("=" * 60)
    
    try:
        test_bot = Bot(token=notification_token)
        test_bot.send_message(
            chat_id=chat_id,
            text="🤖 *Zepix Trading Bot - Integration Test*\n\n"
                 "✅ Controller Bot: Active\n"
                 "✅ Notification Bot: Active\n"
                 "✅ Analytics Bot: Active\n\n"
                 "🎯 Bot is ready for production testing!",
            parse_mode='Markdown'
        )
        print(f"✅ Test message sent to chat_id: {chat_id}")
    except Exception as e:
        print(f"❌ Failed to send test message: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {sum(results)}/3 bots connected successfully")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = test_telegram_bots()
    sys.exit(0 if success else 1)
