# 🤖 DEVIN AUTONOMOUS BATCH IMPLEMENTATION PROMPT

## 📋 PROJECT: ZepixTradingBot Telegram V5 Upgrade
## 📍 LOCATION: `Updates/telegram_updates/`
## 🎯 GOAL: Complete implementation of ALL planning documents

---

## 🚨 GLOBAL NON-NEGOTIABLE RULES

```
❌ NEVER delete any existing file
❌ NEVER overwrite base logic without understanding
❌ NEVER create fresh project - work on EXISTING code
❌ NEVER skip testing before moving to next batch
✅ ALWAYS extend existing files
✅ ALWAYS push to GitLab after each batch
✅ ALWAYS test before marking batch complete
```

---

## 📦 BATCH DIVISION (5 Documents Per Batch)

### **BATCH 1: Foundation & Core Planning**
| # | Document | Purpose |
|---|----------|---------|
| 1 | `00_MASTER_PLAN.md` | Overall architecture vision |
| 2 | `01_COMPLETE_COMMAND_INVENTORY.md` | All commands that need to exist |
| 3 | `01_V6_NOTIFICATION_SYSTEM_PLAN.md` | V6 notification requirements |
| 4 | `02_NOTIFICATION_SYSTEMS_COMPLETE.md` | Complete notification specs |
| 5 | `02_V6_TIMEFRAME_MENU_PLAN.md` | V6 timeframe menu requirements |

### **BATCH 2: Menu & Priority Systems**
| # | Document | Purpose |
|---|----------|---------|
| 1 | `03_MENU_SYSTEMS_ARCHITECTURE.md` | Menu structure & callbacks |
| 2 | `03_PRIORITY_COMMAND_HANDLERS_PLAN.md` | Priority commands specs |
| 3 | `04_ANALYTICS_CAPABILITIES.md` | Analytics & reporting features |
| 4 | `04_PHASES_4_5_6_SUMMARY.md` | Phase implementation summary |
| 5 | `05_IMPLEMENTATION_ROADMAP.md` | Implementation sequence |

### **BATCH 3: Plugin Integration & V6 Features**
| # | Document | Purpose |
|---|----------|---------|
| 1 | `05_V5_PLUGIN_INTEGRATION.md` | Plugin system integration |
| 2 | `06_V6_PRICE_ACTION_TELEGRAM.md` | V6 Price Action features |
| 3 | `07_IMPROVEMENT_ROADMAP.md` | Future improvements |
| 4 | `08_TESTING_DOCUMENTATION.md` | Testing requirements |
| 5 | `09_ERROR_HANDLING_GUIDE.md` | Error handling specs |

### **BATCH 4: Database & Services**
| # | Document | Purpose |
|---|----------|---------|
| 1 | `10_DATABASE_SCHEMA.md` | Database structure |
| 2 | `11_SERVICEAPI_DOCUMENTATION.md` | Service & API specs |
| 3 | `12_VISUAL_CAPABILITIES_GUIDE.md` | Visual features |
| 4 | `COMPLETE_TELEGRAM_DOCUMENTATION_INDEX.md` | Documentation index |
| 5 | `DUAL_ORDER_REENTRY_QUICK_REFERENCE.md` | Dual order quick ref |

### **BATCH 5: Dual Order & Plugin Selection**
| # | Document | Purpose |
|---|----------|---------|
| 1 | `STATUS_DUAL_ORDER_REENTRY.md` | Dual order status |
| 2 | `TELEGRAM_V5_DUAL_ORDER_REENTRY_UPGRADE.md` | Dual order upgrade |
| 3 | `TELEGRAM_V5_PLUGIN_SELECTION_UPGRADE.md` | Plugin selection upgrade |
| 4 | `README.md` | Overview |
| 5 | Final Integration & Verification | - |

---

## 🔄 AUTONOMOUS BATCH CYCLE (REPEAT FOR EACH BATCH)

For each batch, follow this exact cycle:

### STEP 1: READ & ANALYZE (5 minutes per doc)
```
1. Read all 5 documents in the batch COMPLETELY
2. Extract ALL features, commands, menus, callbacks
3. Note dependencies on other batches
4. Identify what's already implemented vs missing
```

### STEP 2: CREATE BATCH IMPLEMENTATION PLAN
```
Create file: Updates/telegram_updates/batch_plans/BATCH_X_IMPLEMENTATION_PLAN.md

Contents:
- List of ALL features from 5 documents
- What's already implemented (check existing code)
- What's missing and needs to be created
- Files to create or modify
- Testing requirements
```

### STEP 3: IMPLEMENT
```
1. Create new files if needed
2. Extend existing files (DON'T overwrite)
3. Wire everything to main bot system
4. Add to menu_manager.py if creating menus
5. Add command handlers to controller_bot.py
```

### STEP 4: TEST
```
1. Run existing tests: pytest tests/ -v
2. Add new tests for new features
3. All tests must PASS before moving on
```

### STEP 5: COMMIT & PUSH
```
git add .
git commit -m "feat(telegram-v5): Batch X - [Brief description]"
git push gitlab main
```

### STEP 6: UPDATE PROGRESS
```
Update: Updates/telegram_updates/DEVIN_BATCH_PROGRESS.md
Mark batch as complete with summary
```

---

## 📊 PROGRESS TRACKING FILE

Create and maintain: `Updates/telegram_updates/DEVIN_BATCH_PROGRESS.md`

```markdown
# Devin Batch Implementation Progress

## Overall Status: X/5 Batches Complete

### Batch 1: Foundation & Core Planning
- [ ] Documents Read
- [ ] Plan Created
- [ ] Implementation Done
- [ ] Tests Passing
- [ ] Pushed to GitLab
- Files Created/Modified: 
- Features Implemented:

### Batch 2: Menu & Priority Systems
- [ ] Documents Read
- [ ] Plan Created
- [ ] Implementation Done
- [ ] Tests Passing
- [ ] Pushed to GitLab
- Files Created/Modified:
- Features Implemented:

### Batch 3: Plugin Integration & V6 Features
- [ ] Documents Read
- [ ] Plan Created
- [ ] Implementation Done
- [ ] Tests Passing
- [ ] Pushed to GitLab
- Files Created/Modified:
- Features Implemented:

### Batch 4: Database & Services
- [ ] Documents Read
- [ ] Plan Created
- [ ] Implementation Done
- [ ] Tests Passing
- [ ] Pushed to GitLab
- Files Created/Modified:
- Features Implemented:

### Batch 5: Dual Order & Plugin Selection
- [ ] Documents Read
- [ ] Plan Created
- [ ] Implementation Done
- [ ] Tests Passing
- [ ] Pushed to GitLab
- Files Created/Modified:
- Features Implemented:

## Final Verification
- [ ] All commands working
- [ ] All notifications working
- [ ] All menus working
- [ ] All tests passing
- [ ] Bot running successfully
```

---

## 🎯 WHAT DEVIN MUST VERIFY AFTER ALL BATCHES

### Commands Must Work:
```
/start, /help, /status, /position, /stats
/daily, /weekly, /monthly, /compare
/setlot, /risktier, /chains, /autonomous
/v6_status, /tf15m_on, /tf30m_on, /tf1h_on, /tf4h_on
/plugin_select, /dual_order, /reentry, /export
```

### Notifications Must Send:
```
- Entry alerts (regular + V6 timeframes)
- Exit alerts with P&L
- Error notifications
- Daily summaries
- Trend pulse alerts
```

### Menus Must Open:
```
- Main Menu → All submenus accessible
- V6 Control Menu → Timeframe toggles work
- Analytics Menu → Shows real data
- Dual Order Menu → Config saves correctly
- Plugin Selection Menu → Plugins enable/disable
- Notification Preferences Menu → Filters work
```

### Tests Must Pass:
```
pytest tests/ -v
Target: >80% coverage
All existing tests + new tests for new features
```

---

## 🚀 START COMMAND FOR DEVIN

```
BEGIN BATCH 1:

1. Read these 5 documents completely:
   - Updates/telegram_updates/00_MASTER_PLAN.md
   - Updates/telegram_updates/01_COMPLETE_COMMAND_INVENTORY.md
   - Updates/telegram_updates/01_V6_NOTIFICATION_SYSTEM_PLAN.md
   - Updates/telegram_updates/02_NOTIFICATION_SYSTEMS_COMPLETE.md
   - Updates/telegram_updates/02_V6_TIMEFRAME_MENU_PLAN.md

2. Create: Updates/telegram_updates/batch_plans/BATCH_1_IMPLEMENTATION_PLAN.md
   - List ALL features mentioned in these docs
   - Check what's already implemented in existing code
   - List what's missing

3. Implement missing features

4. Test everything

5. Push to GitLab

6. Create/Update: Updates/telegram_updates/DEVIN_BATCH_PROGRESS.md

7. Move to Batch 2 and repeat
```

---

## ⚠️ CRITICAL REMINDERS

1. **DON'T RUSH** - Read documents thoroughly before implementing
2. **DON'T SKIP TESTS** - Every batch must have passing tests
3. **DON'T BREAK EXISTING CODE** - Extend, don't overwrite
4. **TRACK PROGRESS** - Update progress file after each batch
5. **PUSH OFTEN** - Commit after each batch completion
6. **VERIFY INTEGRATION** - Features must wire to main bot

---

## 📁 EXPECTED DIRECTORY STRUCTURE AFTER ALL BATCHES

```
Trading_Bot/
├── src/
│   ├── telegram/
│   │   ├── controller_bot.py (extended with new commands)
│   │   ├── notification_bot.py (V6 notification methods)
│   │   ├── v6_command_handlers.py (V6 commands)
│   │   ├── notification_router.py (V6 events)
│   │   └── notification_preferences.py (filtering system)
│   └── menu/
│       ├── menu_manager.py (all menus registered)
│       ├── v6_control_menu_handler.py
│       ├── analytics_menu_handler.py
│       ├── dual_order_menu_handler.py
│       ├── plugin_selection_menu.py
│       └── notification_preferences_menu.py
├── config/
│   ├── notification_preferences.json
│   └── v6_settings.json
├── tests/
│   └── test_telegram_v5_upgrade.py (comprehensive tests)
└── Updates/telegram_updates/
    ├── batch_plans/
    │   ├── BATCH_1_IMPLEMENTATION_PLAN.md
    │   ├── BATCH_2_IMPLEMENTATION_PLAN.md
    │   ├── BATCH_3_IMPLEMENTATION_PLAN.md
    │   ├── BATCH_4_IMPLEMENTATION_PLAN.md
    │   └── BATCH_5_IMPLEMENTATION_PLAN.md
    └── DEVIN_BATCH_PROGRESS.md
```

---

## 🏁 SUCCESS CRITERIA

All batches complete when:
- ✅ All 25 documents fully implemented
- ✅ All commands respond correctly
- ✅ All notifications send properly
- ✅ All menus work with callbacks
- ✅ All tests pass (>80% coverage)
- ✅ Bot runs without errors
- ✅ GitLab has all code pushed
- ✅ Progress file shows 5/5 batches complete
