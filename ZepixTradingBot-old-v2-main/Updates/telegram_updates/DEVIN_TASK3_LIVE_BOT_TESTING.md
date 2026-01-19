# DEVIN TASK 3: Live Telegram Bot Testing

## 🎯 OBJECTIVE
Test all 3 Telegram bots with live credentials to verify:
1. **Controller Bot** - All 105 commands work
2. **Notification Bot** - All 78 notification types route correctly
3. **Analytics Bot** - All analytics features work

---

## 📋 PRE-REQUISITES (Already Complete)
- ✅ Task 1: 105 command handlers wired in `controller_bot.py`
- ✅ Task 2: 78 notification types in `notification_router.py`
- ✅ 62/62 tests passing

---

## 🔑 TELEGRAM BOT CREDENTIALS

**From `config/config.json`:**

| Bot | Token | Chat ID |
|-----|-------|---------|
| Controller | `8598624206:AAGWD7y35HUkrSDvSCrFuTL-FZZx8bjqwwo` | 2139792302 |
| Notification | `8311364103:AAHArQ0kHnS8e_hLGdBMzf9u8bLGlUKK4vM` | 2139792302 |
| Analytics | `8513021073:AAHxk9Z9CxKpc2UKNVn1vhYUIGshDJ2L1Ys` | 2139792302 |

**Allowed User:** `2139792302`

---

## 📝 TASK 3 INSTRUCTIONS

### Step 1: Create Live Test Script
Create `tests/test_live_telegram_bots.py` with:

```python
"""
Live Telegram Bot Testing Script
Tests all 3 bots with real credentials
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telegram import Bot
from telegram.error import TelegramError

# Bot Credentials
CONTROLLER_TOKEN = "8598624206:AAGWD7y35HUkrSDvSCrFuTL-FZZx8bjqwwo"
NOTIFICATION_TOKEN = "8311364103:AAHArQ0kHnS8e_hLGdBMzf9u8bLGlUKK4vM"
ANALYTICS_TOKEN = "8513021073:AAHxk9Z9CxKpc2UKNVn1vhYUIGshDJ2L1Ys"
CHAT_ID = 2139792302


class LiveBotTester:
    def __init__(self):
        self.controller_bot = Bot(token=CONTROLLER_TOKEN)
        self.notification_bot = Bot(token=NOTIFICATION_TOKEN)
        self.analytics_bot = Bot(token=ANALYTICS_TOKEN)
        self.results = {"passed": 0, "failed": 0, "errors": []}
    
    async def test_bot_connection(self, bot: Bot, name: str) -> bool:
        """Test if bot can connect and get info"""
        try:
            info = await bot.get_me()
            print(f"✅ {name} connected: @{info.username}")
            self.results["passed"] += 1
            return True
        except TelegramError as e:
            print(f"❌ {name} connection failed: {e}")
            self.results["failed"] += 1
            self.results["errors"].append(f"{name}: {e}")
            return False
    
    async def test_send_message(self, bot: Bot, name: str, message: str) -> bool:
        """Test sending a message"""
        try:
            msg = await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode='HTML'
            )
            print(f"✅ {name} sent message (ID: {msg.message_id})")
            self.results["passed"] += 1
            return True
        except TelegramError as e:
            print(f"❌ {name} send failed: {e}")
            self.results["failed"] += 1
            self.results["errors"].append(f"{name} send: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all live bot tests"""
        print("\n" + "="*60)
        print("🚀 LIVE TELEGRAM BOT TESTING")
        print("="*60 + "\n")
        
        # Test 1: Bot Connections
        print("📡 Testing Bot Connections...")
        await self.test_bot_connection(self.controller_bot, "Controller Bot")
        await self.test_bot_connection(self.notification_bot, "Notification Bot")
        await self.test_bot_connection(self.analytics_bot, "Analytics Bot")
        
        # Test 2: Send Test Messages
        print("\n📤 Testing Message Sending...")
        await self.test_send_message(
            self.controller_bot, 
            "Controller Bot",
            "🤖 <b>CONTROLLER BOT TEST</b>\n\n✅ Live connection verified!\n📊 105 commands ready"
        )
        await asyncio.sleep(1)  # Rate limiting
        
        await self.test_send_message(
            self.notification_bot,
            "Notification Bot", 
            "🔔 <b>NOTIFICATION BOT TEST</b>\n\n✅ Live connection verified!\n📊 78 notification types ready"
        )
        await asyncio.sleep(1)
        
        await self.test_send_message(
            self.analytics_bot,
            "Analytics Bot",
            "📈 <b>ANALYTICS BOT TEST</b>\n\n✅ Live connection verified!\n📊 Analytics features ready"
        )
        
        # Print Results
        print("\n" + "="*60)
        print("📊 TEST RESULTS")
        print("="*60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results["errors"]:
            print("\n⚠️ Errors:")
            for error in self.results["errors"]:
                print(f"  - {error}")
        
        return self.results["failed"] == 0


async def main():
    tester = LiveBotTester()
    success = await tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

### Step 2: Run Live Tests
```bash
cd Trading_Bot
python tests/test_live_telegram_bots.py
```

### Step 3: Test Controller Bot Commands (Sample 10)
Test these commands via Telegram chat with Controller Bot:
1. `/start` - Main menu appears
2. `/status` - Bot status shows
3. `/help` - Help message appears
4. `/trading` - Trading menu shows
5. `/risk` - Risk menu shows
6. `/settings` - Settings menu shows
7. `/pause` - Bot pauses
8. `/resume` - Bot resumes
9. `/plugins` - Plugin menu shows
10. `/v6` - V6 control menu shows

### Step 4: Test Notification Routing
Create test script to send sample notifications:

```python
# tests/test_notification_routing.py
import asyncio
from src.telegram.notification_router import NotificationRouter, NotificationType

async def test_notifications():
    router = NotificationRouter()
    
    # Test trade notifications
    test_cases = [
        (NotificationType.ENTRY, {"symbol": "XAUUSD", "type": "BUY", "price": 2650.50}),
        (NotificationType.TP_HIT, {"symbol": "XAUUSD", "profit": 150.00}),
        (NotificationType.SL_HIT, {"symbol": "EURUSD", "loss": -50.00}),
        (NotificationType.RECOVERY_SUCCESS, {"symbol": "GBPUSD", "recovered": 75.00}),
        (NotificationType.VOICE_TRADE_ENTRY, {"symbol": "USDJPY", "type": "SELL"}),
    ]
    
    for notification_type, data in test_cases:
        result = await router.route(notification_type, data)
        print(f"{'✅' if result else '❌'} {notification_type.value}: {result}")

if __name__ == "__main__":
    asyncio.run(test_notifications())
```

---

## 📊 EXPECTED RESULTS

### Bot Connections:
| Bot | Status | Username |
|-----|--------|----------|
| Controller | ✅ Connected | @ZepixControllerBot |
| Notification | ✅ Connected | @ZepixNotificationBot |
| Analytics | ✅ Connected | @ZepixAnalyticsBot |

### Test Messages:
| Bot | Message Sent | Message ID |
|-----|--------------|------------|
| Controller | ✅ | (auto-generated) |
| Notification | ✅ | (auto-generated) |
| Analytics | ✅ | (auto-generated) |

---

## 📝 DELIVERABLES

### 1. Create Test Files:
- [ ] `tests/test_live_telegram_bots.py`
- [ ] `tests/test_notification_routing.py`

### 2. Run Tests & Capture Output:
- [ ] All 3 bots connect successfully
- [ ] All 3 bots can send messages
- [ ] Sample commands work via Telegram

### 3. Update Test Report:
Update `FINAL_TEST_REPORT.md` with:
- Live bot test results
- Screenshot/log of test messages
- Any issues found

---

## ⚠️ IMPORTANT RULES

1. **DO NOT** modify bot tokens or credentials
2. **DO NOT** delete any existing files
3. **DO** use rate limiting (1 second between messages)
4. **DO** handle errors gracefully
5. **DO** commit all changes to GitLab

---

## 🔄 GIT WORKFLOW

```bash
git checkout -b devin/task3-live-bot-testing
# ... make changes ...
git add -A
git commit -m "feat(telegram): Add live bot testing scripts"
git push gitlab devin/task3-live-bot-testing
# Create MR to main
```

---

## ✅ SUCCESS CRITERIA

Task 3 is complete when:
1. ✅ All 3 bots connect successfully
2. ✅ All 3 bots can send test messages
3. ✅ Test scripts created and committed
4. ✅ MR merged to main branch
5. ✅ FINAL_TEST_REPORT.md updated

---

**Report back when Task 3 is complete with:**
- Test results (pass/fail counts)
- Bot usernames confirmed
- Any errors encountered
- MR link
