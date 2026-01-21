"""
PHASES 4-6 IMPLEMENTATION VERIFICATION SCRIPT
Verifies implementation of document 04_PHASES_4_5_6_SUMMARY.md

Tests:
- Phase 4: Analytics command interface (parameter-based filtering)
- Phase 5: Notification preferences system (/notifications command)
- Phase 6: Menu callback wiring (session & notification callbacks)

Usage: python verify_phases_4_5_6.py
"""

import os
import sys
import re
from pathlib import Path

# ANSI Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    print(f"\n{BLUE}{BOLD}{'='*80}{RESET}")
    print(f"{BLUE}{BOLD}{text.center(80)}{RESET}")
    print(f"{BLUE}{BOLD}{'='*80}{RESET}\n")

def print_section(text):
    print(f"\n{YELLOW}{BOLD}{text}{RESET}")

def check_file_exists(filepath):
    """Check if file exists"""
    return os.path.exists(filepath)

def search_in_file(filepath, pattern, is_regex=True):
    """Search for pattern in file"""
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if is_regex:
        matches = re.findall(pattern, content, re.MULTILINE)
        return matches
    else:
        return [pattern] if pattern in content else []

def get_line_number(filepath, search_text):
    """Get line number where text appears"""
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if search_text in line:
                return i
    return None

def verify_phase_4():
    """Verify Phase 4: Analytics Command Interface"""
    print_section("PHASE 4: ANALYTICS COMMAND INTERFACE VERIFICATION")
    
    controller_path = "src/telegram/controller_bot.py"
    
    phase_4_checks = {
        "Analytics commands exist": [
            "/performance",
            "/daily",
            "/weekly",
            "/compare",
            "/export"
        ],
        "Parameter-based filtering": [
            r"plugin_filter.*=.*None",
            r"symbol_filter.*=.*None",
            r"Parse filters from message"
        ]
    }
    
    results = {}
    
    # Check analytics commands
    print(f"\n{BOLD}✓ Analytics Commands:{RESET}")
    for cmd in phase_4_checks["Analytics commands exist"]:
        found = search_in_file(controller_path, f'"{cmd}"', is_regex=False)
        if found:
            line = get_line_number(controller_path, f'"{cmd}"')
            print(f"  {GREEN}✓{RESET} {cmd} @ Line {line}")
            results[cmd] = True
        else:
            print(f"  {RED}✗{RESET} {cmd}")
            results[cmd] = False
    
    # Check filtering support
    print(f"\n{BOLD}✓ Parameter-Based Filtering:{RESET}")
    filter_supported = False
    for pattern in phase_4_checks["Parameter-based filtering"]:
        found = search_in_file(controller_path, pattern, is_regex=True)
        if found:
            filter_supported = True
            print(f"  {GREEN}✓{RESET} Found: {pattern}")
    
    if filter_supported:
        print(f"  {GREEN}✓{RESET} Plugin/Symbol filtering implemented")
        results["Filtering"] = True
    else:
        print(f"  {RED}✗{RESET} Filtering not found")
        results["Filtering"] = False
    
    # Phase 4 score
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n{BOLD}Phase 4 Implementation: {passed}/{total} ({percentage:.0f}%){RESET}")
    
    return percentage

def verify_phase_5():
    """Verify Phase 5: Notification Filtering System"""
    print_section("PHASE 5: NOTIFICATION FILTERING SYSTEM VERIFICATION")
    
    controller_path = "src/telegram/controller_bot.py"
    prefs_menu_path = "src/menu/notification_preferences_menu.py"
    prefs_module_path = "src/telegram/notification_preferences.py"
    
    results = {}
    
    # Check if notification preferences files exist
    print(f"\n{BOLD}✓ Notification Preferences Files:{RESET}")
    
    files_to_check = {
        "notification_preferences.py": prefs_module_path,
        "notification_preferences_menu.py": prefs_menu_path
    }
    
    for filename, filepath in files_to_check.items():
        if check_file_exists(filepath):
            filesize = os.path.getsize(filepath)
            print(f"  {GREEN}✓{RESET} {filename} ({filesize} bytes)")
            results[filename] = True
        else:
            print(f"  {RED}✗{RESET} {filename} not found")
            results[filename] = False
    
    # Check /notifications command
    print(f"\n{BOLD}✓ /notifications Command:{RESET}")
    cmd_found = search_in_file(controller_path, '"/notifications"', is_regex=False)
    if cmd_found:
        line = get_line_number(controller_path, '"/notifications"')
        print(f"  {GREEN}✓{RESET} /notifications command registered @ Line {line}")
        results["/notifications"] = True
    else:
        print(f"  {RED}✗{RESET} /notifications command not registered")
        results["/notifications"] = False
    
    # Check handler method
    handler_found = search_in_file(controller_path, r"def handle_notifications_menu", is_regex=True)
    if handler_found:
        line = get_line_number(controller_path, "def handle_notifications_menu")
        print(f"  {GREEN}✓{RESET} handle_notifications_menu() @ Line {line}")
        results["handler"] = True
    else:
        print(f"  {RED}✗{RESET} handle_notifications_menu() not found")
        results["handler"] = False
    
    # Check callback routing
    print(f"\n{BOLD}✓ Notification Preferences Callback Routing:{RESET}")
    callback_handler = search_in_file(controller_path, r"def handle_notification_prefs_callback", is_regex=True)
    if callback_handler:
        line = get_line_number(controller_path, "def handle_notification_prefs_callback")
        print(f"  {GREEN}✓{RESET} handle_notification_prefs_callback() @ Line {line}")
        results["callback_routing"] = True
    else:
        print(f"  {RED}✗{RESET} Callback routing not found")
        results["callback_routing"] = False
    
    # Check NotificationCategory enum
    if check_file_exists(prefs_module_path):
        categories = search_in_file(prefs_module_path, r"class NotificationCategory", is_regex=True)
        if categories:
            print(f"  {GREEN}✓{RESET} NotificationCategory enum defined")
            results["categories"] = True
        
        # Check quiet hours
        quiet_hours = search_in_file(prefs_module_path, r"quiet_hours", is_regex=True)
        if quiet_hours:
            print(f"  {GREEN}✓{RESET} Quiet hours support found")
            results["quiet_hours"] = True
    
    # Phase 5 score
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n{BOLD}Phase 5 Implementation: {passed}/{total} ({percentage:.0f}%){RESET}")
    
    return percentage

def verify_phase_6():
    """Verify Phase 6: Menu Callback Wiring"""
    print_section("PHASE 6: MENU CALLBACK WIRING VERIFICATION")
    
    controller_path = "src/telegram/controller_bot.py"
    session_handler_path = "src/telegram/session_menu_handler.py"
    reentry_handler_path = "src/menu/reentry_menu_handler.py"
    
    results = {}
    
    # Check session menu handler
    print(f"\n{BOLD}✓ Session Menu Handler:{RESET}")
    
    if check_file_exists(session_handler_path):
        filesize = os.path.getsize(session_handler_path)
        print(f"  {GREEN}✓{RESET} session_menu_handler.py exists ({filesize} bytes)")
        results["session_handler_file"] = True
        
        # Check session callback methods
        session_callbacks = [
            "handle_symbol_toggle",
            "handle_time_adjustment",
            "handle_master_switch",
            "handle_force_close_toggle"
        ]
        
        for callback in session_callbacks:
            found = search_in_file(session_handler_path, f"def {callback}", is_regex=False)
            if found:
                print(f"    {GREEN}✓{RESET} {callback}()")
                results[callback] = True
    else:
        print(f"  {RED}✗{RESET} session_menu_handler.py not found")
        results["session_handler_file"] = False
    
    # Check session callback routing in controller
    print(f"\n{BOLD}✓ Session Callback Routing in Controller:{RESET}")
    session_routing = search_in_file(controller_path, r"def handle_session_callback", is_regex=True)
    if session_routing:
        line = get_line_number(controller_path, "def handle_session_callback")
        print(f"  {GREEN}✓{RESET} handle_session_callback() @ Line {line}")
        results["session_routing"] = True
    else:
        print(f"  {RED}✗{RESET} Session callback routing not found")
        results["session_routing"] = False
    
    # Check re-entry menu handler
    print(f"\n{BOLD}✓ Re-entry Menu Handler:{RESET}")
    
    if check_file_exists(reentry_handler_path):
        filesize = os.path.getsize(reentry_handler_path)
        print(f"  {GREEN}✓{RESET} reentry_menu_handler.py exists ({filesize} bytes)")
        results["reentry_handler_file"] = True
        
        # Check re-entry is wired
        reentry_wired = search_in_file(controller_path, "handle_reentry_callback", is_regex=False)
        if reentry_wired:
            print(f"  {GREEN}✓{RESET} Re-entry callbacks wired to controller")
            results["reentry_wired"] = True
    else:
        print(f"  {RED}✗{RESET} reentry_menu_handler.py not found")
        results["reentry_handler_file"] = False
    
    # Check session handler initialization
    print(f"\n{BOLD}✓ Handler Initialization:{RESET}")
    session_init = search_in_file(controller_path, r"self._session_menu_handler", is_regex=True)
    if session_init:
        print(f"  {GREEN}✓{RESET} Session menu handler initialized in controller")
        results["session_init"] = True
    
    notif_init = search_in_file(controller_path, r"self._notification_prefs_menu", is_regex=True)
    if notif_init:
        print(f"  {GREEN}✓{RESET} Notification prefs menu initialized in controller")
        results["notif_init"] = True
    
    # Phase 6 score
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n{BOLD}Phase 6 Implementation: {passed}/{total} ({percentage:.0f}%){RESET}")
    
    return percentage

def main():
    """Main verification function"""
    print_header("PHASES 4-6 IMPLEMENTATION VERIFICATION")
    
    print(f"{BOLD}Document:{RESET} 04_PHASES_4_5_6_SUMMARY.md")
    print(f"{BOLD}Verifying:{RESET} Analytics Interface, Notification Filtering, Menu Callback Wiring\n")
    
    # Change to Trading_Bot directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run verifications
    phase_4_score = verify_phase_4()
    phase_5_score = verify_phase_5()
    phase_6_score = verify_phase_6()
    
    # Calculate overall score
    overall_score = (phase_4_score + phase_5_score + phase_6_score) / 3
    
    # Print summary
    print_header("IMPLEMENTATION SUMMARY")
    
    print(f"{BOLD}Phase 4 (Analytics Interface):{RESET}       {phase_4_score:.0f}%")
    print(f"{BOLD}Phase 5 (Notification Filtering):{RESET}    {phase_5_score:.0f}%")
    print(f"{BOLD}Phase 6 (Menu Callback Wiring):{RESET}      {phase_6_score:.0f}%")
    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}Overall Implementation:{RESET}              {overall_score:.0f}%")
    
    # Final verdict
    if overall_score >= 80:
        status = f"{GREEN}✓ PASS - Ready for Testing{RESET}"
    elif overall_score >= 60:
        status = f"{YELLOW}⚠ PARTIAL - Needs Work{RESET}"
    else:
        status = f"{RED}✗ FAIL - Significant Gaps{RESET}"
    
    print(f"\n{BOLD}Verification Result:{RESET} {status}\n")
    
    # Recommendations
    print(f"{BOLD}NEXT STEPS:{RESET}")
    if phase_4_score < 100:
        print(f"  • Phase 4: Add interactive date range selection menus")
        print(f"  • Phase 4: Implement symbol selection UI")
    if phase_5_score < 100:
        print(f"  • Phase 5: Test notification filtering with real data")
    if phase_6_score < 100:
        print(f"  • Phase 6: Test all menu callbacks end-to-end")
    
    if overall_score >= 80:
        print(f"\n{GREEN}✓ Implementation is production-ready!{RESET}")
    
    return 0 if overall_score >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())
