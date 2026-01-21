# 🧠 PRODUCT MIND MAP - ZEPIX V6
Root: Refactor Trading Engine for V6 Telegram independent architecture.

*   **MM-001: Configuration [DONE]**
    *   Purpose: Define 3 distinct tokens for bots.
    *   Acceptance: Tokens loaded from config. [PASS]
    *   Verification: `TokenManager` tests.

*   **MM-002: Base Architecture [DONE]**
    *   Purpose: Common base for independent bots.
    *   Acceptance: `BaseIndependentBot` exists. [PASS]
    *   Verification: Inheritance check.

*   **MM-003: Multi-Bot Management [DONE]**
    *   Purpose: Orchestrate 3 bots.
    *   Acceptance: `MultiBotManager` initializes 3 roles. [PASS]
    *   Verification: Multi-instance logs.

*   **MM-004: Controller Bot Independence [IN-PROGRESS]**
    *   Purpose: Remove legacy dependency for command handling.
    *   Acceptance: `ControllerBot` handles `/start` and callbacks directly. [PASS]
    *   Verification: Menu navigation working.

*   **MM-005: Notification Bot Independence [DONE]**
    *   Purpose: Direct broadcasts.
    *   Acceptance: `NotificationBot` has `send_alert`. [PASS]
    *   Verification: Alert logs.

*   **MM-006: Legacy Removal [NOT-DONE]**
    *   Purpose: Delete `src/clients/telegram_bot.py`.
    *   Acceptance: System runs without legacy file. [FAIL]
    *   Verification: Deletion + live run.

*   **MM-007: Risk Manager V6 Integration [DONE]**
    *   Purpose: Smart Lot Adjustments in Dual Orders.
    *   Acceptance: `pip_value_std` NameError fixed. [PASS]
    *   Verification: `verify_v6.py` script.
