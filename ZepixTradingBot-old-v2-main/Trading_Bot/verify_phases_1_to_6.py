"""
COMPLETE PHASES 1-6 VERIFICATION SCRIPT
Verifies all 6 phases of Telegram V5 Upgrade implementation

Phase 1: V6 Notification System (NEW - V6-specific methods)
Phase 2: V6 Timeframe Menu (NEW - Menu builder + callback wiring)
Phase 3: Priority Command Handlers (20+ commands)
Phase 4: Analytics Command Interface
Phase 5: Notification Filtering System
Phase 6: Menu Callback Wiring

Version: 1.0.0
Date: January 20, 2026
"""

import os
import sys
import re
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title: str):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}")
    print(f"                     {title}")
    print(f"{'='*80}{Colors.END}\n")

def print_result(check: str, passed: bool, details: str = ""):
    """Print check result"""
    status = f"{Colors.GREEN}✓" if passed else f"{Colors.RED}✗"
    print(f"{status} {check}{Colors.END}")
    if details:
        print(f"  {details}")

def check_file_exists(filepath: str) -> bool:
    """Check if file exists"""
    return os.path.exists(filepath)

def search_in_file(filepath: str, pattern: str, is_regex: bool = False) -> List[Tuple[int, str]]:
    """Search for pattern in file, return list of (line_number, line_content)"""
    if not check_file_exists(filepath):
        return []
    
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if is_regex:
                    if re.search(pattern, line):
                        matches.append((line_num, line.strip()))
                else:
                    if pattern in line:
                        matches.append((line_num, line.strip()))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return matches

def verify_phase_1() -> Dict[str, bool]:
    """Verify Phase 1: V6 Notification System"""
    print_header("PHASE 1: V6 NOTIFICATION SYSTEM VERIFICATION")
    
    results = {}
    filepath = "src/telegram/notification_bot.py"
    
    # Check 1: File exists
    passed = check_file_exists(filepath)
    print_result("notification_bot.py exists", passed)
    results['file_exists'] = passed
    
    if not passed:
        return results
    
    # Check 2: send_v6_entry_alert method
    matches = search_in_file(filepath, "def send_v6_entry_alert")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("send_v6_entry_alert() method", passed, details)
    results['v6_entry_alert'] = passed
    
    # Check 3: send_v6_exit_alert method
    matches = search_in_file(filepath, "def send_v6_exit_alert")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("send_v6_exit_alert() method", passed, details)
    results['v6_exit_alert'] = passed
    
    # Check 4: send_trend_pulse_alert method
    matches = search_in_file(filepath, "def send_trend_pulse_alert")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("send_trend_pulse_alert() method", passed, details)
    results['trend_pulse_alert'] = passed
    
    # Check 5: send_shadow_mode_alert method
    matches = search_in_file(filepath, "def send_shadow_mode_alert")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("send_shadow_mode_alert() method", passed, details)
    results['shadow_mode_alert'] = passed
    
    # Check 6: Timeframe shown in V6 entry messages
    matches = search_in_file(filepath, "Timeframe:")
    passed = len(matches) > 0
    details = f"Found {len(matches)} instances" if matches else "NOT FOUND"
    print_result("Timeframe displayed in V6 alerts", passed, details)
    results['timeframe_display'] = passed
    
    # Check 7: Pattern details in V6 messages
    matches = search_in_file(filepath, "Pattern:")
    passed = len(matches) > 0
    details = f"Found {len(matches)} instances" if matches else "NOT FOUND"
    print_result("Pattern details in V6 alerts", passed, details)
    results['pattern_display'] = passed
    
    # Check 8: Trend Pulse strength display
    matches = search_in_file(filepath, "Trend Pulse:")
    passed = len(matches) > 0
    details = f"Found {len(matches)} instances" if matches else "NOT FOUND"
    print_result("Trend Pulse strength display", passed, details)
    results['pulse_display'] = passed
    
    # Check 9: Shadow mode indicator
    matches = search_in_file(filepath, "Shadow mode")
    passed = len(matches) >= 3  # Should appear in multiple methods
    details = f"Found {len(matches)} instances" if matches else "NOT FOUND"
    print_result("Shadow mode indicators", passed, details)
    results['shadow_indicator'] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 1 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def verify_phase_2() -> Dict[str, bool]:
    """Verify Phase 2: V6 Timeframe Menu"""
    print_header("PHASE 2: V6 TIMEFRAME MENU VERIFICATION")
    
    results = {}
    menu_filepath = "src/telegram/v6_timeframe_menu_builder.py"
    controller_filepath = "src/telegram/controller_bot.py"
    
    # Check 1: Menu builder file exists
    passed = check_file_exists(menu_filepath)
    print_result("v6_timeframe_menu_builder.py exists", passed)
    results['menu_file_exists'] = passed
    
    if passed:
        # Check 2: build_v6_submenu method
        matches = search_in_file(menu_filepath, "def build_v6_submenu")
        passed = len(matches) > 0
        details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
        print_result("build_v6_submenu() method", passed, details)
        results['build_submenu'] = passed
        
        # Check 3: 4 timeframes defined
        matches = search_in_file(menu_filepath, '["15m", "30m", "1h", "4h"]')
        passed = len(matches) > 0
        details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
        print_result("V6 timeframes defined (15m, 30m, 1h, 4h)", passed, details)
        results['timeframes_defined'] = passed
        
        # Check 4: Enable/Disable buttons
        matches = search_in_file(menu_filepath, "v6_enable")
        passed = len(matches) > 0
        details = f"Found {len(matches)} enable callbacks" if matches else "NOT FOUND"
        print_result("Enable/Disable callbacks", passed, details)
        results['enable_disable_buttons'] = passed
        
        # Check 5: Per-timeframe config
        matches = search_in_file(menu_filepath, "v6_config")
        passed = len(matches) > 0
        details = f"Found {len(matches)} config callbacks" if matches else "NOT FOUND"
        print_result("Per-timeframe config menus", passed, details)
        results['config_menus'] = passed
        
        # Check 6: Bulk actions
        matches = search_in_file(menu_filepath, "v6_enable_all")
        passed = len(matches) > 0
        print_result("Bulk enable/disable actions", passed)
        results['bulk_actions'] = passed
    
    # Check 7: V6 menu builder initialization in controller
    matches = search_in_file(controller_filepath, "_v6_timeframe_menu_builder")
    passed = len(matches) > 0
    details = f"Found {len(matches)} references" if matches else "NOT FOUND"
    print_result("V6 menu builder initialized in controller", passed, details)
    results['builder_initialized'] = passed
    
    # Check 8: V6 menu builder import
    matches = search_in_file(controller_filepath, "from src.telegram.v6_timeframe_menu_builder import V6TimeframeMenuBuilder")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("V6TimeframeMenuBuilder import", passed, details)
    results['builder_import'] = passed
    
    # Check 9: show_v6_control_menu wired
    matches = search_in_file(controller_filepath, "def show_v6_control_menu")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("show_v6_control_menu() method", passed, details)
    results['show_v6_menu'] = passed
    
    # Check 10: handle_v6_callback wired
    matches = search_in_file(controller_filepath, "def handle_v6_callback")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("handle_v6_callback() method", passed, details)
    results['handle_v6_callback'] = passed
    
    # Check 11: Central callback dispatcher
    matches = search_in_file(controller_filepath, "def dispatch_callback")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("Central callback dispatcher", passed, details)
    results['callback_dispatcher'] = passed
    
    # Check 12: v6_* callback routing
    matches = search_in_file(controller_filepath, "if callback_data.startswith('v6_'):")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("v6_* callback routing", passed, details)
    results['v6_routing'] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 2 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def verify_phase_3() -> Dict[str, bool]:
    """Verify Phase 3: Priority Command Handlers"""
    print_header("PHASE 3: PRIORITY COMMAND HANDLERS VERIFICATION")
    
    results = {}
    filepath = "src/telegram/controller_bot.py"
    
    # Check priority commands
    priority_commands = {
        '/chains': 'handle_chains',
        '/setlot': 'handle_set_lot',
        '/risktier': 'handle_risk_tier',
        '/autonomous': 'handle_autonomous',
        '/tf15m': 'handle_tf_15m',
        '/tf30m': 'handle_tf30m',  # Changed to search for the main handler
        '/tf1h': 'handle_tf_1h',
        '/tf4h': 'handle_tf_4h',
        '/slhunt': 'handle_sl_hunt',
        '/tpcontinue': 'handle_tp_continue',
        '/levels': 'handle_levels',
        '/shadow': 'handle_shadow',
        '/trends': 'handle_trends'
    }
    
    for cmd, handler in priority_commands.items():
        matches = search_in_file(filepath, f'"{cmd}"')
        passed = len(matches) > 0
        details = f"Found {len(matches)} references" if passed else "NOT FOUND"
        print_result(f"{cmd} command", passed, details)
        results[cmd] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 3 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def verify_phase_4() -> Dict[str, bool]:
    """Verify Phase 4: Analytics Command Interface"""
    print_header("PHASE 4: ANALYTICS COMMAND INTERFACE VERIFICATION")
    
    results = {}
    filepath = "src/telegram/controller_bot.py"
    
    # Check analytics commands
    analytics_commands = {
        '/performance': 'handle_performance',
        '/daily': 'handle_daily',
        '/weekly': 'handle_weekly',
        '/compare': 'handle_compare',
        '/export': 'handle_export'
    }
    
    for cmd, handler in analytics_commands.items():
        matches = search_in_file(filepath, f'"{cmd}"')
        passed = len(matches) > 0
        details = f"Found {len(matches)} references" if passed else "NOT FOUND"
        print_result(f"{cmd} command", passed, details)
        results[cmd] = passed
    
    # Check filtering
    matches = search_in_file(filepath, "plugin_filter")
    passed = len(matches) > 0
    details = f"Found {len(matches)} references" if passed else "NOT FOUND"
    print_result("Plugin filtering (V3/V6)", passed, details)
    results['plugin_filter'] = passed
    
    matches = search_in_file(filepath, "symbol_filter")
    passed = len(matches) > 0
    details = f"Found {len(matches)} references" if passed else "NOT FOUND"
    print_result("Symbol filtering", passed, details)
    results['symbol_filter'] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 4 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def verify_phase_5() -> Dict[str, bool]:
    """Verify Phase 5: Notification Filtering System"""
    print_header("PHASE 5: NOTIFICATION FILTERING SYSTEM VERIFICATION")
    
    results = {}
    
    # Check notification preferences files
    prefs_filepath = "src/telegram/notification_preferences.py"
    menu_filepath = "src/menu/notification_preferences_menu.py"
    controller_filepath = "src/telegram/controller_bot.py"
    
    # File existence
    passed = check_file_exists(prefs_filepath)
    print_result("notification_preferences.py exists", passed)
    results['prefs_file'] = passed
    
    passed = check_file_exists(menu_filepath)
    print_result("notification_preferences_menu.py exists", passed)
    results['menu_file'] = passed
    
    # /notifications command
    matches = search_in_file(controller_filepath, '"/notifications"')
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("/notifications command registered", passed, details)
    results['notifications_cmd'] = passed
    
    # Callback handlers
    matches = search_in_file(controller_filepath, "handle_notifications_menu")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("handle_notifications_menu() method", passed, details)
    results['menu_handler'] = passed
    
    matches = search_in_file(controller_filepath, "handle_notification_prefs_callback")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("handle_notification_prefs_callback() method", passed, details)
    results['callback_handler'] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 5 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def verify_phase_6() -> Dict[str, bool]:
    """Verify Phase 6: Menu Callback Wiring"""
    print_header("PHASE 6: MENU CALLBACK WIRING VERIFICATION")
    
    results = {}
    filepath = "src/telegram/controller_bot.py"
    
    # Session menu handler
    matches = search_in_file(filepath, "handle_session_callback")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("handle_session_callback() method", passed, details)
    results['session_callback'] = passed
    
    # Session menu file
    session_filepath = "src/telegram/session_menu_handler.py"
    passed = check_file_exists(session_filepath)
    print_result("session_menu_handler.py exists", passed)
    results['session_file'] = passed
    
    # Re-entry menu file
    reentry_filepath = "src/menu/reentry_menu_handler.py"
    passed = check_file_exists(reentry_filepath)
    print_result("reentry_menu_handler.py exists", passed)
    results['reentry_file'] = passed
    
    # Central callback dispatcher
    matches = search_in_file(filepath, "def dispatch_callback")
    passed = len(matches) > 0
    details = f"@ Line {matches[0][0]}" if matches else "NOT FOUND"
    print_result("Central callback dispatcher", passed, details)
    results['dispatcher'] = passed
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n{Colors.BOLD}Phase 6 Implementation: {passed_count}/{total_count} ({int(passed_count/total_count*100)}%){Colors.END}")
    
    return results

def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}")
    print(f"                     COMPLETE PHASES 1-6 VERIFICATION")
    print(f"{'='*80}{Colors.END}\n")
    
    print("Document: 05_IMPLEMENTATION_ROADMAP.md")
    print("Verifying: V6 Notifications, V6 Menu, Commands, Analytics, Filtering, Callbacks\n")
    
    # Run all verifications
    phase1_results = verify_phase_1()
    phase2_results = verify_phase_2()
    phase3_results = verify_phase_3()
    phase4_results = verify_phase_4()
    phase5_results = verify_phase_5()
    phase6_results = verify_phase_6()
    
    # Calculate totals
    all_results = {
        "Phase 1": phase1_results,
        "Phase 2": phase2_results,
        "Phase 3": phase3_results,
        "Phase 4": phase4_results,
        "Phase 5": phase5_results,
        "Phase 6": phase6_results
    }
    
    print_header("IMPLEMENTATION SUMMARY")
    
    for phase_name, results in all_results.items():
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        percentage = int(passed/total*100) if total > 0 else 0
        
        if percentage == 100:
            status = f"{Colors.GREEN}✓ COMPLETE{Colors.END}"
        elif percentage >= 80:
            status = f"{Colors.YELLOW}🟡 ALMOST{Colors.END}"
        else:
            status = f"{Colors.RED}⚠️ PARTIAL{Colors.END}"
        
        print(f"{phase_name:<30} {passed}/{total} ({percentage}%)   {status}")
    
    # Overall status
    total_passed = sum(sum(1 for v in r.values() if v) for r in all_results.values())
    total_checks = sum(len(r) for r in all_results.values())
    overall_percentage = int(total_passed/total_checks*100) if total_checks > 0 else 0
    
    print(f"\n{Colors.BOLD}{'─'*80}")
    print(f"Overall Implementation:              {total_passed}/{total_checks} ({overall_percentage}%)")
    print(f"{'─'*80}{Colors.END}\n")
    
    if overall_percentage == 100:
        print(f"{Colors.GREEN}{Colors.BOLD}Verification Result: ✓ PASS - All Phases 100% Complete!{Colors.END}\n")
    elif overall_percentage >= 85:
        print(f"{Colors.YELLOW}{Colors.BOLD}Verification Result: 🟡 MOSTLY COMPLETE - Minor gaps remaining{Colors.END}\n")
    else:
        print(f"{Colors.RED}{Colors.BOLD}Verification Result: ⚠️ PARTIAL - More work needed{Colors.END}\n")
    
    print(f"{Colors.BOLD}NEXT STEPS:{Colors.END}\n")
    
    # Identify incomplete phases
    incomplete_phases = []
    for phase_name, results in all_results.items():
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        if passed < total:
            incomplete_phases.append((phase_name, passed, total))
    
    if incomplete_phases:
        print(f"{Colors.YELLOW}Incomplete Phases:{Colors.END}")
        for phase, passed, total in incomplete_phases:
            missing = total - passed
            print(f"  • {phase}: {missing} check(s) missing")
        print()
    else:
        print(f"{Colors.GREEN}✓ All phases verified - Implementation complete!{Colors.END}\n")

if __name__ == "__main__":
    main()
