# 📋 TASK LIST: TELEGRAM 3-BOT ARCHITECTURE REFACTOR

## 🎯 OBJECTIVE
Refactor the current broken/hybrid Telegram 3-Bot system into a clean, independent architecture where Controller, Notification, and Analytics bots operate autonomously without dependency on the legacy `telegram_bot.py` wrapper.

## 🔴 CRITICAL ISSUES TO FIX
1.  **Dual Implementation:** Legacy `telegram_bot.py` vs V5 `src/telegram/` bots running in parallel.
2.  **Legacy Dependency:** V5 bots are just wrappers delegating back to legacy code.
3.  **Command Routing Hell:** 6-layer deep routing causing latency and confusion.
4.  **Token Chaos:** Unclear configuration for 3 distinct bot tokens.
5.  **Polling Conflicts:** Race conditions and HTTP 409 errors.

## 🗓️ PHASE 1: BLUEPRINT & PREPARATION [CURRENT]
- [ ] **Analysis:** Confirm architecture conflicts (DONE)
- [ ] **Plan:** Define Clean Architecture Blueprint
- [ ] **Backup:** Secure current codebase before refactoring

## 🛠️ PHASE 2: CORE ARCHITECTURE [PENDING]
- [ ] **Config Update:** Define distinct tokens for Controller, Notification, Analytics.
- [ ] **Base Class:** Create strict `BaseIndependentBot` class.
- [ ] **Manager:** Rewrite `MultiTelegramManager` to manage 3 independent instances.

## 🤖 PHASE 3: BOT INDEPENDENCE [PENDING]
- [ ] **Controller Bot:** Move all command handling logic FROM legacy TO `controller_bot.py`.
- [ ] **Notification Bot:** Implement direct broadcast logic in `notification_bot.py`.
- [ ] **Analytics Bot:** Move reporting logic FROM legacy TO `analytics_bot.py`.

## 🗑️ PHASE 4: LEGACY REMOVAL [PENDING]
- [ ] **Disconnect:** Remove `legacy_bot` dependency from Manager.
- [ ] **Cleanup:** Delete `telegram_bot.py` (or archive it).
- [ ] **Verification:** Ensure no system calls legacy code.

## 🧪 PHASE 5: VERIFICATION [PENDING]
- [ ] **Unit Tests:** Test each bot independently.
- [ ] **Integration Test:** Run all 3 bots simultaneously.
- [ ] **Live Test:** Verify with actual Telegram tokens.

## 📉 STATUS DASHBOARD
- **Tasks Total:** 15
- **Tasks Done:** 1
- **Tasks In-Progress:** 0
- **Overall Status:** 🔴 NOT STARTED
