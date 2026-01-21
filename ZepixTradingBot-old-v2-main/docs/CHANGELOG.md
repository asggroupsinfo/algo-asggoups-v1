# 📜 CHANGELOG

## 2026-01-20: V6 Telegram Bot Independence Refactor
- **Summary**: Refactored the hybrid V5/Legacy bot into a clean V6 architecture with 3 independent bots.
- **Micro-features impacted**: Multi-bot initialization, Command routing, Risk management lot adjustments.
- **Files touched**: 
    - `src/telegram/core/multi_bot_manager.py`
    - `src/telegram/bots/controller_bot.py`
    - `src/managers/risk_manager.py`
    - `src/main.py`
- **Why**: Objective alignment with V6 clean architecture and fixing legacy dependencies.
- **Verification**: `verify_v6.py` passed. Menu handlers implemented in Controller bot.
- **Risk/rollback**: Deleting legacy `telegram_bot.py` (pending).
- **References**: MM-001 to MM-005, MM-007.
