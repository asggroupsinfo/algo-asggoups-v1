"""
Database Reality Check Script
Check what's actually implemented vs what's documented in 10_DATABASE_SCHEMA.md
"""
import sqlite3
import os
from datetime import datetime

print("="*70)
print("DATABASE REALITY CHECK - 10_DATABASE_SCHEMA.md Implementation Status")
print("="*70)

db_path = 'data/trading_bot.db'

if not os.path.exists(db_path):
    print(f"\n❌ DATABASE NOT FOUND: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ==================== TABLES CHECK ====================
print("\n📊 TABLES CHECK")
print("-"*70)

# Expected tables from document
EXPECTED_TABLES = {
    'trades': 'Core trading records',
    'reentry_chains': 'Re-entry chain tracking',
    'sl_events': 'SL hit events',
    'tp_reentry_events': 'TP re-entry events',
    'reversal_exit_events': 'Reversal exit tracking',
    'profit_booking_chains': 'Profit booking chains',
    'profit_booking_orders': 'Profit booking orders',
    'profit_booking_events': 'Profit booking events',
    'trading_sessions': 'Trading session tracking',
    'system_state': 'System state key-value'
}

# Get actual tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
actual_tables = set([row[0] for row in cursor.fetchall()])

print(f"\nExpected Tables: {len(EXPECTED_TABLES)}")
print(f"Actual Tables: {len(actual_tables)}")

tables_status = []
for table_name, description in EXPECTED_TABLES.items():
    exists = table_name in actual_tables
    status = "✅" if exists else "❌"
    tables_status.append((table_name, description, exists))
    print(f"{status} {table_name:30s} - {description}")

missing_tables = [t for t, _, exists in tables_status if not exists]
extra_tables = actual_tables - set(EXPECTED_TABLES.keys())

if extra_tables:
    print(f"\n⚠️ Extra tables found (not in document):")
    for table in extra_tables:
        print(f"   - {table}")

# ==================== TRADES TABLE COLUMNS CHECK ====================
print("\n\n📋 TRADES TABLE COLUMNS CHECK")
print("-"*70)

EXPECTED_TRADES_COLUMNS = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'trade_id': 'TEXT UNIQUE',
    'symbol': 'TEXT NOT NULL',
    'direction': 'TEXT NOT NULL',
    'entry_price': 'REAL',
    'exit_price': 'REAL',
    'sl_price': 'REAL',
    'tp_price': 'REAL',
    'lot_size': 'REAL NOT NULL',
    'strategy': 'TEXT',
    'logic_type': 'TEXT',
    'pnl': 'REAL DEFAULT 0',
    'commission': 'REAL DEFAULT 0',
    'swap': 'REAL DEFAULT 0',
    'status': 'TEXT DEFAULT "open"',
    'open_time': 'DATETIME',
    'close_time': 'DATETIME',
    'comment': 'TEXT',
    'chain_id': 'TEXT',
    'chain_level': 'INTEGER DEFAULT 1',
    'is_re_entry': 'BOOLEAN DEFAULT FALSE',
    'order_type': 'TEXT',
    'profit_chain_id': 'TEXT',
    'profit_level': 'INTEGER DEFAULT 0',
    'session_id': 'TEXT',
    'sl_adjusted': 'INTEGER DEFAULT 0',
    'original_sl_distance': 'REAL DEFAULT 0.0',
    'base_lot_size': 'REAL DEFAULT 0.0',
    'final_lot_size': 'REAL DEFAULT 0.0',
    'base_sl_pips': 'REAL DEFAULT 0.0',
    'final_sl_pips': 'REAL DEFAULT 0.0',
    'lot_multiplier': 'REAL DEFAULT 1.0',
    'sl_multiplier': 'REAL DEFAULT 1.0'
}

if 'trades' in actual_tables:
    cursor.execute("PRAGMA table_info(trades)")
    actual_columns = {row[1]: row[2] for row in cursor.fetchall()}  # name: type
    
    print(f"\nExpected Columns: {len(EXPECTED_TRADES_COLUMNS)}")
    print(f"Actual Columns: {len(actual_columns)}")
    
    columns_status = []
    for col_name in EXPECTED_TRADES_COLUMNS.keys():
        exists = col_name in actual_columns
        status = "✅" if exists else "❌"
        columns_status.append((col_name, exists))
        if not exists:
            print(f"{status} {col_name}")
    
    missing_columns = [col for col, exists in columns_status if not exists]
    extra_columns = set(actual_columns.keys()) - set(EXPECTED_TRADES_COLUMNS.keys())
    
    if extra_columns:
        print(f"\n⚠️ Extra columns in trades table:")
        for col in extra_columns:
            print(f"   - {col}")
else:
    print("❌ trades table not found!")

# ==================== DATABASE METHODS CHECK ====================
print("\n\n🔧 DATABASE METHODS CHECK (from src/database.py)")
print("-"*70)

EXPECTED_METHODS = [
    'create_tables',
    'save_trade',
    'save_chain',
    'save_sl_event',
    'get_trade_history',
    'get_chain_statistics',
    'get_sl_recovery_stats',
    'get_tp_reentry_stats',
    'get_trades_by_date',
    'save_profit_chain',
    'get_active_profit_chains',
    'get_profit_chain_stats',
    'create_session',
    'close_session',
    'get_active_session',
    'get_session_details',
    'test_connection'
]

# Check if methods exist in database.py
import inspect
try:
    from src.database import TradeDatabase
    db_class = TradeDatabase
    actual_methods = [method for method in dir(db_class) if not method.startswith('_')]
    
    print(f"\nExpected Methods: {len(EXPECTED_METHODS)}")
    print(f"Actual Methods: {len([m for m in actual_methods if m in EXPECTED_METHODS])}")
    
    methods_status = []
    for method_name in EXPECTED_METHODS:
        exists = method_name in actual_methods
        status = "✅" if exists else "❌"
        methods_status.append((method_name, exists))
        if not exists:
            print(f"{status} {method_name}")
    
    missing_methods = [m for m, exists in methods_status if not exists]
    
except Exception as e:
    print(f"❌ Error checking methods: {e}")

# ==================== DATA STATISTICS ====================
print("\n\n📈 DATABASE DATA STATISTICS")
print("-"*70)

for table_name in EXPECTED_TABLES.keys():
    if table_name in actual_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"{table_name:30s}: {count:6d} records")

# ==================== WAL MODE CHECK ====================
print("\n\n⚙️ DATABASE CONFIGURATION")
print("-"*70)

cursor.execute("PRAGMA journal_mode")
journal_mode = cursor.fetchone()[0]
print(f"Journal Mode: {journal_mode}")

cursor.execute("PRAGMA foreign_keys")
fk_enabled = cursor.fetchone()[0]
print(f"Foreign Keys: {'Enabled' if fk_enabled else 'Disabled'}")

# ==================== ANALYTICS QUERIES CHECK ====================
print("\n\n📊 ANALYTICS QUERIES TEST")
print("-"*70)

# Test daily performance query
try:
    cursor.execute("""
        SELECT 
            DATE(close_time) as trade_date,
            COUNT(*) as total_trades,
            SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
            ROUND(SUM(pnl), 2) as total_pnl
        FROM trades
        WHERE status = 'closed'
            AND close_time >= datetime('now', '-7 days')
        GROUP BY DATE(close_time)
    """)
    results = cursor.fetchall()
    print(f"✅ Daily Performance Query: {len(results)} days of data")
except Exception as e:
    print(f"❌ Daily Performance Query Failed: {e}")

# Test plugin performance query
try:
    cursor.execute("""
        SELECT 
            logic_type as plugin,
            COUNT(*) as trades,
            ROUND(SUM(pnl), 2) as total_pnl
        FROM trades
        WHERE status = 'closed'
            AND logic_type IS NOT NULL
        GROUP BY logic_type
    """)
    results = cursor.fetchall()
    print(f"✅ Plugin Performance Query: {len(results)} plugins found")
except Exception as e:
    print(f"❌ Plugin Performance Query Failed: {e}")

# Test re-entry chain stats
try:
    cursor.execute("""
        SELECT 
            COUNT(*) as total_chains,
            AVG(max_level_reached) as avg_levels,
            SUM(total_profit) as total_profit
        FROM reentry_chains
    """)
    result = cursor.fetchone()
    if result:
        print(f"✅ Re-entry Chain Stats: {result[0]} chains, Avg Level: {result[1] if result[1] else 0:.2f}")
except Exception as e:
    print(f"❌ Re-entry Chain Stats Failed: {e}")

# ==================== SUMMARY ====================
print("\n\n" + "="*70)
print("SUMMARY")
print("="*70)

tables_implemented = len([t for t, _, exists in tables_status if exists])
columns_implemented = len([c for c, exists in columns_status if exists]) if 'trades' in actual_tables else 0
methods_implemented = len([m for m, exists in methods_status if exists])

tables_percent = (tables_implemented / len(EXPECTED_TABLES)) * 100
columns_percent = (columns_implemented / len(EXPECTED_TRADES_COLUMNS)) * 100 if 'trades' in actual_tables else 0
methods_percent = (methods_implemented / len(EXPECTED_METHODS)) * 100

print(f"\n📊 Implementation Status:")
print(f"   Tables:  {tables_implemented}/{len(EXPECTED_TABLES)} ({tables_percent:.1f}%)")
print(f"   Columns: {columns_implemented}/{len(EXPECTED_TRADES_COLUMNS)} ({columns_percent:.1f}%)")
print(f"   Methods: {methods_implemented}/{len(EXPECTED_METHODS)} ({methods_percent:.1f}%)")

overall_percent = (tables_percent + columns_percent + methods_percent) / 3
print(f"\n🎯 Overall Implementation: {overall_percent:.1f}%")

if missing_tables:
    print(f"\n❌ Missing Tables ({len(missing_tables)}):")
    for table in missing_tables:
        print(f"   - {table}")

if 'trades' in actual_tables and missing_columns:
    print(f"\n❌ Missing Columns in trades table ({len(missing_columns)}):")
    for col in missing_columns[:10]:  # Show first 10
        print(f"   - {col}")

if missing_methods:
    print(f"\n❌ Missing Methods ({len(missing_methods)}):")
    for method in missing_methods:
        print(f"   - {method}")

if overall_percent >= 95:
    print(f"\n✅ DATABASE IS {overall_percent:.1f}% IMPLEMENTED - EXCELLENT!")
elif overall_percent >= 80:
    print(f"\n⚠️ DATABASE IS {overall_percent:.1f}% IMPLEMENTED - GOOD, MINOR GAPS")
else:
    print(f"\n❌ DATABASE IS {overall_percent:.1f}% IMPLEMENTED - SIGNIFICANT GAPS!")

print("\n" + "="*70)
conn.close()
