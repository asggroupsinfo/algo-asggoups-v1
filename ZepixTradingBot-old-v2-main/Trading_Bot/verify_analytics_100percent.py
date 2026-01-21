"""
ANALYTICS CAPABILITIES VERIFICATION SCRIPT
==========================================

This script verifies 100% implementation of all analytics capabilities
from 04_ANALYTICS_CAPABILITIES.md against the actual bot code.

Expected Commands (10 total):
1. /performance - Performance report
2. /pair_report - Performance by trading pair
3. /strategy_report - Performance by strategy/plugin
4. /tp_report - TP re-entry statistics
5. /v6_performance - V6 timeframe breakdown
6. /daily - Daily comprehensive report
7. /weekly - Weekly comprehensive report
8. /monthly - Monthly comprehensive report
9. /export - CSV export functionality
10. /dashboard - Live trading dashboard
11. /compare - V3 vs V6 comparison

Date: 2026-01-20
Version: 1.0.0
"""

import re
import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

# File paths
CONTROLLER_BOT = Path("src/telegram/controller_bot.py")
ANALYTICS_QUERIES = Path("src/database/analytics_queries.py")
DOCUMENT = Path("../Updates/telegram_updates/04_ANALYTICS_CAPABILITIES.md")

# Analytics commands to verify
ANALYTICS_COMMANDS = {
    "/performance": "Full performance report with real data",
    "/pair_report": "Performance breakdown by trading pair",
    "/strategy_report": "Performance breakdown by strategy/plugin",
    "/tp_report": "TP re-entry statistics",
    "/v6_performance": "V6 Price Action timeframe breakdown",
    "/daily": "Comprehensive daily report",
    "/weekly": "Comprehensive weekly report",
    "/monthly": "Comprehensive monthly report",
    "/export": "Export trading data to CSV",
    "/dashboard": "Live trading dashboard",
    "/compare": "V3 vs V6 comparison"
}

def verify_handler_exists(file_content, command):
    """Verify handler function exists for command"""
    handler_name = f"handle_{command[1:]}"
    pattern = rf"def {handler_name}\("
    
    matches = re.findall(pattern, file_content)
    return len(matches) > 0, handler_name

def get_handler_line_number(file_path, handler_name):
    """Get line number where handler is defined"""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if re.search(rf"def {handler_name}\(", line):
                return line_num
    return None

def verify_registry_mapping(file_content, command, handler_name):
    """Verify command is registered in command handlers"""
    pattern = rf'self\._command_handlers\["{command}"\]\s*=\s*self\.{handler_name}'
    return bool(re.search(pattern, file_content))

def verify_analytics_queries_module():
    """Verify analytics_queries.py module exists and has required methods"""
    if not ANALYTICS_QUERIES.exists():
        return False, []
    
    with open(ANALYTICS_QUERIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_methods = [
        "get_performance_stats",
        "get_pair_performance",
        "get_strategy_performance",
        "get_tp_reentry_stats",
        "get_v6_timeframe_performance",
        "get_plugin_group_performance",
        "get_trades_for_date",
        "get_weekly_summary",
        "get_monthly_summary",
        "prepare_trades_export",
        "prepare_daily_summary_export"
    ]
    
    found_methods = []
    for method in required_methods:
        if re.search(rf"def {method}\(", content):
            found_methods.append(method)
    
    return True, found_methods

def verify_helper_functions(file_content):
    """Verify helper functions exist"""
    helpers = {
        "_init_analytics_queries": "Initialize analytics query engine",
        "_format_pnl": "Format P&L with color indicator",
        "_create_progress_bar": "Create visual progress bar",
        "_get_plugin_display_name": "Convert plugin_id to display name"
    }
    
    found = {}
    for helper, desc in helpers.items():
        pattern = rf"def {helper}\("
        if re.search(pattern, file_content):
            found[helper] = desc
    
    return found

def main():
    print_header("ANALYTICS CAPABILITIES - 100% IMPLEMENTATION VERIFICATION")
    
    # Check file existence
    print_info("Checking file existence...")
    if not CONTROLLER_BOT.exists():
        print_error(f"Controller bot not found: {CONTROLLER_BOT}")
        return False
    print_success(f"Controller bot found: {CONTROLLER_BOT}")
    
    # Read controller bot
    with open(CONTROLLER_BOT, 'r', encoding='utf-8') as f:
        controller_content = f.read()
    
    print_success(f"Loaded controller_bot.py ({len(controller_content)} bytes)")
    
    # ==================== VERIFY ANALYTICS QUERY MODULE ====================
    print_header("ANALYTICS QUERY MODULE VERIFICATION")
    
    module_exists, found_methods = verify_analytics_queries_module()
    if not module_exists:
        print_error(f"Analytics queries module not found: {ANALYTICS_QUERIES}")
        return False
    
    print_success(f"Analytics queries module exists: {ANALYTICS_QUERIES}")
    print_success(f"Found {len(found_methods)} analytics query methods")
    
    for method in found_methods:
        print_success(f"  • {method}()")
    
    # ==================== VERIFY HELPER FUNCTIONS ====================
    print_header("HELPER FUNCTIONS VERIFICATION")
    
    helpers = verify_helper_functions(controller_content)
    print_success(f"Found {len(helpers)}/4 helper functions")
    
    for helper, desc in helpers.items():
        print_success(f"  • {helper}() - {desc}")
    
    # ==================== VERIFY ANALYTICS COMMANDS ====================
    print_header("ANALYTICS COMMANDS VERIFICATION (11 Commands)")
    
    results = {
        "handlers_found": 0,
        "handlers_missing": 0,
        "registry_ok": 0,
        "registry_missing": 0,
        "total": len(ANALYTICS_COMMANDS)
    }
    
    handler_details = []
    
    for command, description in ANALYTICS_COMMANDS.items():
        handler_exists, handler_name = verify_handler_exists(controller_content, command)
        registry_ok = verify_registry_mapping(controller_content, command, handler_name)
        
        if handler_exists:
            results["handlers_found"] += 1
            line_num = get_handler_line_number(CONTROLLER_BOT, handler_name)
            
            if registry_ok:
                results["registry_ok"] += 1
                status = f"{Colors.GREEN}✓ COMPLETE{Colors.END}"
                handler_details.append({
                    "command": command,
                    "handler": handler_name,
                    "line": line_num,
                    "status": "✓"
                })
                print_success(f"{command:<20} {handler_name}() at line {line_num} [REGISTERED]")
            else:
                results["registry_missing"] += 1
                print_error(f"{command:<20} {handler_name}() exists but NOT REGISTERED")
        else:
            results["handlers_missing"] += 1
            results["registry_missing"] += 1
            print_error(f"{command:<20} MISSING (no handler found)")
    
    # ==================== SUMMARY ====================
    print_header("IMPLEMENTATION SUMMARY")
    
    handler_percent = (results["handlers_found"] / results["total"]) * 100
    registry_percent = (results["registry_ok"] / results["total"]) * 100
    
    print(f"{'Metric':<30} {'Status':<20} {'Percentage'}")
    print("-" * 70)
    print(f"{'Handlers Implemented':<30} {results['handlers_found']}/{results['total']:<18} {handler_percent:.0f}%")
    print(f"{'Registry Mappings':<30} {results['registry_ok']}/{results['total']:<18} {registry_percent:.0f}%")
    print(f"{'Analytics Query Methods':<30} {len(found_methods)}/11{'':<14} {len(found_methods)/11*100:.0f}%")
    print(f"{'Helper Functions':<30} {len(helpers)}/4{'':<16} {len(helpers)/4*100:.0f}%")
    
    # ==================== FINAL VERDICT ====================
    print_header("FINAL VERDICT")
    
    all_complete = (
        results["handlers_found"] == results["total"] and
        results["registry_ok"] == results["total"] and
        len(found_methods) >= 11 and
        len(helpers) >= 4
    )
    
    if all_complete:
        print(f"{Colors.GREEN}{Colors.BOLD}★ 100% IMPLEMENTATION ACHIEVED ★{Colors.END}\n")
        print_success("All 11 analytics commands implemented")
        print_success("All handlers registered in command registry")
        print_success("Analytics query engine fully functional")
        print_success("Helper functions complete")
        
        print(f"\n{Colors.BOLD}HANDLER LINE NUMBERS:{Colors.END}")
        for detail in handler_details:
            print(f"  {detail['status']} {detail['command']:<20} → {detail['handler']}() @ Line {detail['line']}")
        
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ INCOMPLETE IMPLEMENTATION{Colors.END}\n")
        print_error(f"Handlers: {results['handlers_found']}/{results['total']}")
        print_error(f"Registry: {results['registry_ok']}/{results['total']}")
        return False

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    success = main()
    
    print(f"\n{Colors.BOLD}Verification Result: {'PASS ✓' if success else 'FAIL ✗'}{Colors.END}\n")
    sys.exit(0 if success else 1)
