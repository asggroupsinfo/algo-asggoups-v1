# 🛠️ IMPLEMENTATION PLAN: TELEGRAM 3-BOT CLEAN ARCHITECTURE

## 🎯 OBJECTIVE
Refactor the Telegram 3-Bot system to be **fully independent, asynchronous, and clean**, removing the dependency on legacy code while ensuring zero downtime during migration.

## 🏗️ ARCHITECTURE BLUEPRINT

### 1. New Class Hierarchy
```
BaseIndependentBot (Abstract)
├── ControllerBot (Commands, Admin)
├── NotificationBot (Broadcasts, Alerts)
└── AnalyticsBot (Reports, Stats)
```

### 2. File Structure Changes
```
src/telegram/
├── bots/                   <-- NEW FOLDER
│   ├── base_bot.py
│   ├── controller_bot.py
│   ├── notification_bot.py
│   └── analytics_bot.py
├── core/                   <-- NEW FOLDER
│   ├── multi_bot_manager.py (Rewritten)
│   ├── token_manager.py     (New)
│   └── message_router.py    (Simplified)
└── utils/                  <-- NEW FOLDER
    ├── keyboards.py
    └── formatters.py
```

## 📅 EXECUTION STEPS

### PHASE 1: FOUNDATION (Safe Setup)
1.  **Create New Directory Structure:** Set up `src/telegram/bots`, `core`, `utils`.
2.  **Implement `BaseIndependentBot`:** Create the abstract base class with common polling/sending logic using `python-telegram-bot` (async).
3.  **Implement `TokenManager`:** Create a secure token loader that strictly enforces 3 distinct tokens or explicit single-mode.

### PHASE 2: INDEPENDENT BOT LOGIC
4.  **Rewrite `ControllerBot`:** 
    - Move command logic from `telegram_bot.py` (legacy) to `src/telegram/bots/controller_bot.py`.
    - Implement `handle_start`, `handle_help`, `handle_status` natively.
5.  **Rewrite `NotificationBot`:**
    - Create dedicated `broadcast()` method.
    - Implement `send_alert()` queue system.
6.  **Rewrite `AnalyticsBot`:**
    - Implement `generate_report()` logic.

### PHASE 3: MANAGER ORCHESTRATION
7.  **Rewrite `MultiTelegramManager`:**
    - Remove `set_legacy_bot`.
    - Initialize the 3 new bot classes.
    - Implement true async start/stop.

### PHASE 4: CLEANUP & SWITCHOVER
8.  **Update `TradingEngine`:** Point it to new `MultiTelegramManager`.
9.  **Archive Legacy:** Rename `telegram_bot.py` to `telegram_bot.py.bak`.
10. **Verify:** Run full test suite.

## 🛡️ RISK MITIGATION
- **Parallel Run:** We will create the new structure alongside the old one. logic will be switched over only when verified.
- **Token Check:** The system will validate tokens on startup to prevent "Single Bot Mode" accidents.
- **Rollback:** Keep `telegram_bot.py` until final sign-off.

## ✅ DEFINITION OF DONE
- [ ] 3 Distinct Bot instances running.
- [ ] Controller handles /start, /help, /status without legacy.
- [ ] Notification Bot sends test alert.
- [ ] Analytics Bot sends test report.
- [ ] Legacy `telegram_bot.py` is NOT loaded.
- [ ] 0 Errors in logs.
