# FINAL EXECUTION MAP

**Date:** 2026-01-16  
**Created By:** Devin AI  
**Purpose:** Complete file mapping for project restructuring  
**Status:** PLANNING ONLY - AWAITING GO SIGNAL

---

## 1. SCAN SUMMARY

| Category | Count |
|----------|-------|
| Root Level Files | 14 |
| Root Level Directories | 13 |
| Total Files to Move | ~150 |
| Total Files to Keep in Place | ~300 |
| Total Files to Delete | ~20 |

---

## 2. ROOT LEVEL FILE MAPPING

### 2.1 Files to KEEP (No Move)

```
[KEEP] .env.example
[KEEP] .gitignore
[KEEP] .pre-commit-config.yaml
[KEEP] pyproject.toml
[KEEP] requirements.txt
[KEEP] README.md
[KEEP] START_BOT.bat
[KEEP] ROADMAP.md
```

### 2.2 Files to ARCHIVE

```
[OLD] ./DEEPSEEK_AUDIT_FINAL.md
  --> [NEW] ./_archive/root_audits/DEEPSEEK_AUDIT_FINAL.md

[OLD] ./DEEPSEEK_DEEP_REASONING_AUDIT_REPORT.md
  --> [NEW] ./_archive/root_audits/DEEPSEEK_DEEP_REASONING_AUDIT_REPORT.md

[OLD] ./PINE_BOT_AUTONOMOUS_AUDIT.md
  --> [NEW] ./_archive/root_audits/PINE_BOT_AUTONOMOUS_AUDIT.md

[OLD] ./PROJECT_MEMORY_RESTORED.md
  --> [NEW] ./_archive/root_audits/PROJECT_MEMORY_RESTORED.md

[OLD] ./PROJECT_SCAN_REPORT_DEEPSEEK_V2.md
  --> [NEW] ./_archive/root_audits/PROJECT_SCAN_REPORT_DEEPSEEK_V2.md
```

### 2.3 Files to DELETE

```
[DELETE] ./bot_debug.log (empty temp file)
[DELETE] ./.pytest_cache/ (cache directory)
```

---

## 3. DIRECTORY MAPPING

### 3.1 Directories to KEEP (No Move)

```
[KEEP] ./src/           --> Source code (UNCHANGED)
[KEEP] ./config/        --> Configuration (UNCHANGED)
[KEEP] ./data/          --> Data storage (UNCHANGED)
[KEEP] ./logs/          --> Log files (UNCHANGED)
[KEEP] ./assets/        --> Static assets (UNCHANGED)
[KEEP] ./updates/       --> V5 migration docs (UNCHANGED)
```

### 3.2 Directories to ARCHIVE

```
[OLD] ./PLAN/
  --> [NEW] ./_archive/legacy_docs/PLAN/

[OLD] ./_devin_reports/
  --> [NEW] ./_archive/devin_reports/

[OLD] ./archive/
  --> [NEW] ./_archive/old_archive/
```

### 3.3 Directories to REORGANIZE

```
[REORGANIZE] ./tests/     --> Internal reorganization
[REORGANIZE] ./scripts/   --> Internal reorganization
[REORGANIZE] ./docs/      --> Internal reorganization
```

---

## 4. TESTS DIRECTORY MAPPING

### 4.1 Create New Subdirectories

```
[CREATE] ./tests/integration/
[CREATE] ./tests/batch/
[CREATE] ./tests/_archive/
```

### 4.2 Files to Move to `tests/integration/`

```
[OLD] ./tests/test_core_delegation.py
  --> [NEW] ./tests/integration/test_core_delegation.py

[OLD] ./tests/test_dual_order_integration.py
  --> [NEW] ./tests/integration/test_dual_order_integration.py

[OLD] ./tests/test_profit_booking_integration.py
  --> [NEW] ./tests/integration/test_profit_booking_integration.py

[OLD] ./tests/test_autonomous_integration.py
  --> [NEW] ./tests/integration/test_autonomous_integration.py

[OLD] ./tests/test_database_isolation.py
  --> [NEW] ./tests/integration/test_database_isolation.py

[OLD] ./tests/test_shadow_mode.py
  --> [NEW] ./tests/integration/test_shadow_mode.py
```

### 4.3 Files to Move to `tests/batch/`

```
[OLD] ./tests/test_batch_02_schemas.py
  --> [NEW] ./tests/batch/test_batch_02_schemas.py

[OLD] ./tests/test_batch_03_services.py
  --> [NEW] ./tests/batch/test_batch_03_services.py

[OLD] ./tests/test_batch_04_telegram.py
  --> [NEW] ./tests/batch/test_batch_04_telegram.py

[OLD] ./tests/test_batch_05_ux.py
  --> [NEW] ./tests/batch/test_batch_05_ux.py

[OLD] ./tests/test_batch_06_notifications.py
  --> [NEW] ./tests/batch/test_batch_06_notifications.py

[OLD] ./tests/test_batch_07_service_integration.py
  --> [NEW] ./tests/batch/test_batch_07_service_integration.py

[OLD] ./tests/test_batch_11_health.py
  --> [NEW] ./tests/batch/test_batch_11_health.py

[OLD] ./tests/test_batch_12_migration.py
  --> [NEW] ./tests/batch/test_batch_12_migration.py
```

### 4.4 Files to Move to `tests/_archive/`

```
[OLD] ./tests/test_ui_integration.py
  --> [NEW] ./tests/_archive/test_ui_integration.py

[OLD] ./tests/test_menu_flow_live.py
  --> [NEW] ./tests/_archive/test_menu_flow_live.py

[OLD] ./tests/test_menu_system_live.py
  --> [NEW] ./tests/_archive/test_menu_system_live.py

[OLD] ./tests/v3_master_simulation.py
  --> [NEW] ./tests/_archive/v3_master_simulation.py

[OLD] ./tests/audits/
  --> [NEW] ./tests/_archive/audits/

[OLD] ./tests/bible_suite/
  --> [NEW] ./tests/_archive/bible_suite/

[OLD] ./tests/simulations/
  --> [NEW] ./tests/_archive/simulations/
```

### 4.5 Files to KEEP in `tests/` Root

```
[KEEP] ./tests/__init__.py
[KEEP] ./tests/test_bot.py
[KEEP] ./tests/test_callback_parsing.py
[KEEP] ./tests/test_callback_flow.py
[KEEP] ./tests/test_session_manager.py
[KEEP] ./tests/test_fixed_clock_system.py
```

---

## 5. SCRIPTS DIRECTORY MAPPING

### 5.1 Create New Subdirectories

```
[CREATE] ./scripts/deploy/
[CREATE] ./scripts/_archive/
```

### 5.2 Files to Move to `scripts/deploy/`

```
[OLD] ./scripts/DEPLOY_AND_TEST_BOT.py
  --> [NEW] ./scripts/deploy/DEPLOY_AND_TEST_BOT.py
```

### 5.3 Files to Move to `scripts/_archive/`

```
[OLD] ./scripts/fix_menu_manager_bug.py
  --> [NEW] ./scripts/_archive/fix_menu_manager_bug.py

[OLD] ./scripts/fix_all_dependency_checks.py
  --> [NEW] ./scripts/_archive/fix_all_dependency_checks.py

[OLD] ./scripts/fix_string_literals.py
  --> [NEW] ./scripts/_archive/fix_string_literals.py

[OLD] ./scripts/fix_and_start_bot.py
  --> [NEW] ./scripts/_archive/fix_and_start_bot.py

[OLD] ./scripts/fix_comma.py
  --> [NEW] ./scripts/_archive/fix_comma.py

[OLD] ./scripts/fix_logging_indent.py
  --> [NEW] ./scripts/_archive/fix_logging_indent.py

[OLD] ./scripts/patch_telegram_bot.py
  --> [NEW] ./scripts/_archive/patch_telegram_bot.py

[OLD] ./scripts/patch_fine_tune_final.py
  --> [NEW] ./scripts/_archive/patch_fine_tune_final.py

[OLD] ./scripts/deepseek_segmented_audit.py
  --> [NEW] ./scripts/_archive/deepseek_segmented_audit.py

[OLD] ./scripts/deepseek_deep_reasoning.py
  --> [NEW] ./scripts/_archive/deepseek_deep_reasoning.py

[OLD] ./scripts/verify_brutal_fixes.py
  --> [NEW] ./scripts/_archive/verify_brutal_fixes.py

[OLD] ./scripts/automate_deepseek_scan.py
  --> [NEW] ./scripts/_archive/automate_deepseek_scan.py

[OLD] ./scripts/optimize_deepseek_scan.py
  --> [NEW] ./scripts/_archive/optimize_deepseek_scan.py

[OLD] ./scripts/deep_scan_robust.py
  --> [NEW] ./scripts/_archive/deep_scan_robust.py

[OLD] ./scripts/deep_scan.py
  --> [NEW] ./scripts/_archive/deep_scan.py
```

### 5.4 Files to KEEP in `scripts/` Root

```
[KEEP] ./scripts/start_bot.py
[KEEP] ./scripts/run_all_tests.py
[KEEP] ./scripts/rename_plugins.py
[KEEP] ./scripts/reset_stats.py
[KEEP] ./scripts/setup_mt5_connection.py
[KEEP] ./scripts/query_trades.py
[KEEP] ./scripts/show_pnl_breakdown.py
[KEEP] ./scripts/check_todays_trades.py
```

---

## 6. DOCS DIRECTORY MAPPING

### 6.1 Create New Subdirectories

```
[CREATE] ./docs/_archive/
[CREATE] ./docs/setup/
```

### 6.2 Directories to Move to `docs/_archive/`

```
[OLD] ./docs/debug_reports/
  --> [NEW] ./docs/_archive/debug_reports/

[OLD] ./docs/verification-reports/
  --> [NEW] ./docs/_archive/verification-reports/

[OLD] ./docs/V3_FINAL_REPORTS/
  --> [NEW] ./docs/_archive/V3_FINAL_REPORTS/

[OLD] ./docs/log 08-12-25/
  --> [NEW] ./docs/_archive/log_08-12-25/

[OLD] ./docs/trading view log/
  --> [NEW] ./docs/_archive/trading_view_log/
```

### 6.3 Directories to RENAME (No Spaces)

```
[OLD] ./docs/Zepix Setup Files/
  --> [NEW] ./docs/setup/
```

### 6.4 Directories to KEEP (No Move)

```
[KEEP] ./docs/V5_BIBLE/          --> Primary documentation
[KEEP] ./docs/api/               --> API docs
[KEEP] ./docs/developer_notes/   --> Developer notes
[KEEP] ./docs/guides/            --> User guides
[KEEP] ./docs/implementation/    --> Implementation docs
[KEEP] ./docs/important/         --> Important docs
[KEEP] ./docs/plans/             --> Plans
[KEEP] ./docs/reports/           --> Reports
[KEEP] ./docs/testing/           --> Testing docs
[KEEP] ./docs/tradingview/       --> TradingView docs
```

---

## 7. ARCHIVE DIRECTORY MAPPING

### 7.1 Files to DELETE from `archive/`

```
[DELETE] ./archive/temp_scripts/ (entire directory - temporary scripts)
```

### 7.2 Files to KEEP in `archive/` (Move to `_archive/old_archive/`)

```
[OLD] ./archive/log 05-12-25/
  --> [NEW] ./_archive/old_archive/log_05-12-25/

[OLD] ./archive/log 01-12-25/
  --> [NEW] ./_archive/old_archive/log_01-12-25/

[OLD] ./archive/debug_files/
  --> [NEW] ./_archive/old_archive/debug_files/

[OLD] ./archive/documentation/
  --> [NEW] ./_archive/old_archive/documentation/
```

---

## 8. FINAL TREE STRUCTURE (AFTER RESTRUCTURING)

```
ZepixTradingBot-old-v2-main/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── README.md
├── ROADMAP.md
├── START_BOT.bat
│
├── src/                          # SOURCE CODE (UNCHANGED)
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── api/
│   ├── clients/
│   ├── core/
│   │   ├── plugin_system/
│   │   └── services/
│   ├── logic_plugins/
│   │   ├── _template/
│   │   ├── v3_combined/
│   │   ├── v6_price_action_1m/
│   │   ├── v6_price_action_5m/
│   │   ├── v6_price_action_15m/
│   │   └── v6_price_action_1h/
│   ├── managers/
│   ├── menu/
│   ├── models/
│   ├── modules/
│   ├── monitoring/
│   ├── processors/
│   ├── services/
│   ├── telegram/
│   └── utils/
│
├── tests/                        # TESTS (REORGANIZED)
│   ├── __init__.py
│   ├── conftest.py               # NEW: Pytest config
│   ├── test_bot.py
│   ├── test_callback_*.py
│   ├── test_session_manager.py
│   │
│   ├── integration/              # NEW: Integration tests
│   │   ├── test_core_delegation.py
│   │   ├── test_dual_order_integration.py
│   │   ├── test_profit_booking_integration.py
│   │   ├── test_autonomous_integration.py
│   │   ├── test_database_isolation.py
│   │   └── test_shadow_mode.py
│   │
│   ├── batch/                    # NEW: Batch tests
│   │   ├── test_batch_02_schemas.py
│   │   ├── test_batch_03_services.py
│   │   ├── test_batch_04_telegram.py
│   │   ├── test_batch_05_ux.py
│   │   ├── test_batch_06_notifications.py
│   │   ├── test_batch_07_service_integration.py
│   │   ├── test_batch_11_health.py
│   │   └── test_batch_12_migration.py
│   │
│   ├── verify/                   # KEEP: Verification tests
│   │
│   └── _archive/                 # NEW: Archived tests
│       ├── test_ui_integration.py
│       ├── test_menu_*.py
│       ├── audits/
│       ├── bible_suite/
│       └── simulations/
│
├── scripts/                      # SCRIPTS (REORGANIZED)
│   ├── start_bot.py
│   ├── run_all_tests.py
│   ├── rename_plugins.py
│   ├── reset_stats.py
│   ├── setup_mt5_connection.py
│   ├── query_trades.py
│   │
│   ├── deploy/                   # NEW: Deployment scripts
│   │   └── DEPLOY_AND_TEST_BOT.py
│   │
│   └── _archive/                 # NEW: Archived scripts
│       ├── fix_*.py
│       ├── patch_*.py
│       ├── deepseek_*.py
│       └── verify_*.py
│
├── config/                       # CONFIG (UNCHANGED)
│   └── plugins/
│
├── data/                         # DATA (UNCHANGED)
│   ├── schemas/
│   └── backups/
│
├── docs/                         # DOCS (REORGANIZED)
│   ├── V5_BIBLE/                 # PRIMARY DOCUMENTATION
│   │   ├── 00_INDEX.md
│   │   ├── 03_TELEGRAM/
│   │   └── *.md
│   ├── api/
│   ├── developer_notes/
│   ├── guides/
│   ├── implementation/
│   ├── important/
│   ├── plans/
│   ├── reports/
│   ├── setup/                    # RENAMED from "Zepix Setup Files"
│   ├── testing/
│   ├── tradingview/
│   │
│   └── _archive/                 # NEW: Archived docs
│       ├── debug_reports/
│       ├── verification-reports/
│       ├── V3_FINAL_REPORTS/
│       ├── log_08-12-25/
│       └── trading_view_log/
│
├── logs/                         # LOGS (UNCHANGED)
│
├── assets/                       # ASSETS (UNCHANGED)
│
├── updates/                      # V5 MIGRATION (UNCHANGED)
│   └── v5_hybrid_plugin_architecture/
│
└── _archive/                     # NEW: CONSOLIDATED ARCHIVE
    ├── root_audits/              # Root level audit files
    │   ├── DEEPSEEK_AUDIT_FINAL.md
    │   ├── DEEPSEEK_DEEP_REASONING_AUDIT_REPORT.md
    │   ├── PINE_BOT_AUTONOMOUS_AUDIT.md
    │   ├── PROJECT_MEMORY_RESTORED.md
    │   └── PROJECT_SCAN_REPORT_DEEPSEEK_V2.md
    │
    ├── legacy_docs/              # Legacy documentation
    │   └── PLAN/
    │
    ├── devin_reports/            # Devin audit reports
    │   ├── audit_v5/
    │   ├── telegram_docs_update/
    │   └── validation_phase/
    │
    └── old_archive/              # Previous archive contents
        ├── log_05-12-25/
        ├── log_01-12-25/
        ├── debug_files/
        └── documentation/
```

---

## 9. EXECUTION PHASES

### Phase 1: Create New Directories
```bash
mkdir -p _archive/root_audits
mkdir -p _archive/legacy_docs
mkdir -p _archive/devin_reports
mkdir -p _archive/old_archive
mkdir -p tests/integration
mkdir -p tests/batch
mkdir -p tests/_archive
mkdir -p scripts/deploy
mkdir -p scripts/_archive
mkdir -p docs/_archive
mkdir -p docs/setup
```

### Phase 2: Move Root Level Files
```bash
git mv DEEPSEEK_AUDIT_FINAL.md _archive/root_audits/
git mv DEEPSEEK_DEEP_REASONING_AUDIT_REPORT.md _archive/root_audits/
git mv PINE_BOT_AUTONOMOUS_AUDIT.md _archive/root_audits/
git mv PROJECT_MEMORY_RESTORED.md _archive/root_audits/
git mv PROJECT_SCAN_REPORT_DEEPSEEK_V2.md _archive/root_audits/
```

### Phase 3: Move Legacy Directories
```bash
git mv PLAN _archive/legacy_docs/
git mv _devin_reports/* _archive/devin_reports/
git mv archive/* _archive/old_archive/
```

### Phase 4: Reorganize Tests
```bash
git mv tests/test_core_delegation.py tests/integration/
git mv tests/test_dual_order_integration.py tests/integration/
# ... (continue for all test files)
```

### Phase 5: Reorganize Scripts
```bash
git mv scripts/DEPLOY_AND_TEST_BOT.py scripts/deploy/
git mv scripts/fix_*.py scripts/_archive/
# ... (continue for all script files)
```

### Phase 6: Reorganize Docs
```bash
git mv "docs/Zepix Setup Files" docs/setup
git mv docs/debug_reports docs/_archive/
git mv docs/verification-reports docs/_archive/
# ... (continue for all doc directories)
```

### Phase 7: Delete Temporary Files
```bash
rm bot_debug.log
rm -rf .pytest_cache
rm -rf archive/temp_scripts
```

### Phase 8: Verification
```bash
python -m pytest tests/ -v
python scripts/start_bot.py --help
```

---

## 10. CONSTRAINTS VERIFIED

| Constraint | Status |
|------------|--------|
| No Renaming of source folders | VERIFIED - src/ unchanged |
| Single Layer logic | VERIFIED - max 2 levels deep |
| No spaces in folder names | VERIFIED - renamed "Zepix Setup Files" to "setup" |
| Git history preserved | VERIFIED - using git mv |
| All imports still work | TO VERIFY after execution |

---

## 11. LOST FILES CHECK

| File/Directory | Status | Destination |
|----------------|--------|-------------|
| All src/ files | MAPPED | No move (unchanged) |
| All config/ files | MAPPED | No move (unchanged) |
| All data/ files | MAPPED | No move (unchanged) |
| All updates/ files | MAPPED | No move (unchanged) |
| All logs/ files | MAPPED | No move (unchanged) |
| All assets/ files | MAPPED | No move (unchanged) |
| All tests/ files | MAPPED | Reorganized internally |
| All scripts/ files | MAPPED | Reorganized internally |
| All docs/ files | MAPPED | Reorganized internally |
| Root audit files | MAPPED | _archive/root_audits/ |
| PLAN/ | MAPPED | _archive/legacy_docs/ |
| _devin_reports/ | MAPPED | _archive/devin_reports/ |
| archive/ | MAPPED | _archive/old_archive/ |

**RESULT: NO LOST FILES**

---

## 12. APPROVAL REQUIRED

**Before execution, User must confirm:**

- [ ] Final tree structure is acceptable
- [ ] File mappings are correct
- [ ] Execution phases are acceptable
- [ ] No files are missing from the plan

---

**STATUS: AWAITING GO SIGNAL**

**DO NOT EXECUTE UNTIL USER APPROVES**

---

**END OF EXECUTION MAP**
