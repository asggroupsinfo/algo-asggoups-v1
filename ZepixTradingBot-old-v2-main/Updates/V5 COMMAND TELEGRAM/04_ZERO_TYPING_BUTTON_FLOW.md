# TELEGRAM BOT - ZERO-TYPING BUTTON FLOW SYSTEM
**Version:** V5.0  
**Created:** January 21, 2026  
**Purpose:** Complete button-based interaction flows (no manual typing)

---

## 🎯 PHILOSOPHY

**Zero-Typing Principle:**
- User NEVER types anything except /start
- All interactions through buttons
- Every option is clickable
- Multi-step flows guided by buttons
- Clear visual feedback at each step

**Benefits:**
- ✅ No syntax errors from user input
- ✅ Faster interaction (no typing)
- ✅ Clear available options
- ✅ Guided workflows
- ✅ Mobile-friendly

---

## 🔄 FLOW ARCHITECTURE

### Flow Levels (Max 4 Depth)

```
Level 1: Main Menu (12 categories)
    ↓
Level 2: Category Submenu (commands in category)
    ↓
Level 3: Command Options (parameters/settings)
    ↓
Level 4: Confirmation/Final Action
```

**Navigation Rules:**
- Always provide "⬅️ Back" button (go up 1 level)
- Always provide "🏠 Main Menu" button (jump to Level 1)
- Never exceed 4 levels deep
- Use breadcrumbs to show location

### Breadcrumb Display

```
🏠 Main Menu > 📊 Trading Control > /positions > V3 Plugin
```

---

## 📋 BUTTON FLOW PATTERNS

### Pattern 1: Simple Direct Command

**Example:** `/status` (no parameters)

```
User clicks: [📊 System Commands]
    ↓
Shows: System Commands Menu
    ↓
User clicks: [📊 Bot Status]
    ↓
Bot executes: /status
    ↓
Shows: Status report with sticky header
```

**Button Flow:**
```
Main Menu
    ↓
[🎛️ System Commands]
    ↓
Category Menu:
┌─────────────────────────────────────┐
│  📊 Bot Status                       │
│  ⏸️ Pause Bot                        │
│  ▶️ Resume Bot                       │
│  ...                                 │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
    ↓ (User clicks "Bot Status")
    ↓
Shows status with no intermediate steps
```

**Callback Data:**
- `system_status` → Execute /status immediately

### Pattern 2: Single Selection

**Example:** `/pause` (choose what to pause)

```
User clicks: [⏸️ Pause Bot]
    ↓
Shows: Selection menu
    ↓
User selects: [V3 Plugin]
    ↓
Bot executes: Pause V3
    ↓
Shows: Confirmation message
```

**Button Flow:**
```
Main Menu > System Commands
    ↓
[⏸️ Pause Bot]
    ↓
Selection Screen:
┌─────────────────────────────────────┐
│  🔵 Pause V3 Only                   │
│  🟢 Pause V6 Only                   │
│  🔷 Pause Both Plugins              │
│  🤖 Pause Entire Bot                │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
    ↓ (User clicks "Pause V3 Only")
    ↓
Confirmation:
╔══════════════════════════════════════╗
║  ✅ V3 Plugin Paused                 ║
╠══════════════════════════════════════╣
║  All V3 strategies stopped           ║
║  Existing positions remain open      ║
║  No new trades will be taken         ║
╚══════════════════════════════════════╝

[▶️ Resume V3] [🏠 Main Menu]
```

**Callback Data:**
- `system_pause_v3` → Pause V3 plugin
- `system_pause_v6` → Pause V6 plugin
- `system_pause_both` → Pause both plugins
- `system_pause_all` → Pause entire bot

### Pattern 3: Multi-Step with Plugin Selection

**Example:** `/positions` (plugin → view positions)

```
User clicks: [📊 View Positions]
    ↓
Shows: Plugin selection
    ↓
User selects: [🔵 V3 Plugin]
    ↓
Bot shows: V3 positions list
```

**Button Flow:**
```
Main Menu > Trading Control
    ↓
[📊 View Positions]
    ↓
Plugin Selection:
┌─────────────────────────────────────┐
│  🔵 V3 Positions                    │
│  🟢 V6 Positions                    │
│  🔷 All Positions (Combined)        │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
    ↓ (User clicks "V3 Positions")
    ↓
Positions Display:
╔══════════════════════════════════════╗
║  🔵 V3 POSITIONS (3 active)          ║
╠══════════════════════════════════════╣
║  1️⃣ EURUSD BUY 0.05 lots            ║
║     Entry: 1.0820 | P&L: +$12.50    ║
║                                      ║
║  2️⃣ GBPUSD SELL 0.03 lots           ║
║     Entry: 1.2650 | P&L: -$5.20     ║
║                                      ║
║  3️⃣ USDJPY BUY 0.05 lots            ║
║     Entry: 151.20 | P&L: +$8.30     ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  ❌ Close All V3 Positions          │
│  🔄 Refresh                          │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```

**Callback Data:**
- `plugin_select_v3_positions` → Show V3 positions
- `plugin_select_v6_positions` → Show V6 positions
- `plugin_select_both_positions` → Show all positions
- `trading_closeall_v3` → Close all V3 positions
- `trading_refresh_positions` → Refresh display

### Pattern 4: Complex Multi-Step (4 levels)

**Example:** `/buy` (plugin → symbol → lot size → confirm)

```
User clicks: [💰 Place Buy Order]
    ↓
Step 1: Plugin selection
    ↓ [User selects V3]
Step 2: Symbol selection
    ↓ [User selects EURUSD]
Step 3: Lot size selection
    ↓ [User selects 0.05]
Step 4: Confirmation
    ↓ [User confirms]
Bot executes: Market buy order
```

**Complete Flow:**

**STEP 1: Plugin Selection**
```
Main Menu > Trading Control
    ↓
[💰 Place Buy Order]
    ↓
╔══════════════════════════════════════╗
║  🔌 SELECT PLUGIN                    ║
╠══════════════════════════════════════╣
║  Which plugin to use for this trade? ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  🔵 V3 Combined Logic               │
│  🟢 V6 Price Action                 │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `buy_plugin_v3` or `buy_plugin_v6`

**STEP 2: Symbol Selection**
```
🏠 Main Menu > Trading > Buy > V3 Plugin
    ↓
╔══════════════════════════════════════╗
║  💱 SELECT SYMBOL (V3)               ║
╠══════════════════════════════════════╣
║  Choose currency pair to trade       ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  💶 EURUSD  │  💷 GBPUSD            │
├─────────────────────────────────────┤
│  💴 USDJPY  │  💵 AUDUSD            │
├─────────────────────────────────────┤
│  📋 Show All Symbols                │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `buy_v3_symbol_EURUSD`, `buy_v3_symbol_GBPUSD`, etc.

**STEP 3: Lot Size Selection**
```
🏠 Main Menu > Trading > Buy > V3 > EURUSD
    ↓
╔══════════════════════════════════════╗
║  📊 SELECT LOT SIZE                  ║
╠══════════════════════════════════════╣
║  Symbol: EURUSD                      ║
║  Plugin: V3 Combined Logic           ║
║  Current Price: 1.0825               ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  0.01 lots│  0.03 lots              │
├─────────────────────────────────────┤
│  0.05 lots│  0.10 lots              │
├─────────────────────────────────────┤
│  0.20 lots│  0.50 lots              │
├─────────────────────────────────────┤
│  ⚙️ Custom Lot Size                  │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `buy_v3_EURUSD_lot_0.05`, etc.

**Exception: Custom Lot Size**
If user clicks "Custom Lot Size":
```
Bot: "Please enter lot size (e.g., 0.07):"
User types: 0.07
Bot validates and continues to Step 4
```
**Note:** This is the ONLY place user types!

**STEP 4: Confirmation**
```
🏠 Main Menu > Trading > Buy > V3 > EURUSD > 0.05 lots
    ↓
╔══════════════════════════════════════╗
║  ✅ CONFIRM TRADE                    ║
╠══════════════════════════════════════╣
║  Direction: BUY                      ║
║  Symbol: EURUSD                      ║
║  Plugin: V3 Combined Logic           ║
║  Lot Size: 0.05                      ║
║  Entry Price: 1.0825 (Market)        ║
║                                      ║
║  Estimated Risk: $25.00              ║
║  Stop Loss: 1.0815 (10 pips)         ║
║  Take Profit: 1.0855 (30 pips)       ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  ✅ Confirm & Execute Trade         │
├─────────────────────────────────────┤
│  ❌ Cancel                           │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** 
- `buy_v3_EURUSD_0.05_confirm` → Execute trade
- `buy_cancel` → Cancel and go back

**STEP 5: Execution Result**
```
╔══════════════════════════════════════╗
║  ✅ TRADE EXECUTED                   ║
╠══════════════════════════════════════╣
║  Symbol: EURUSD                      ║
║  Direction: BUY                      ║
║  Lot Size: 0.05                      ║
║  Entry Price: 1.08253                ║
║  Ticket: #12345678                   ║
║                                      ║
║  SL: 1.0815 (10 pips)                ║
║  TP: 1.0855 (30 pips)                ║
║                                      ║
║  Status: OPEN ✅                     ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  📊 View Positions                   │
│  💰 Place Another Trade             │
│  🏠 Main Menu                        │
└─────────────────────────────────────┘
```

**Full Callback Chain:**
```
buy_start → buy_plugin_v3 → buy_v3_symbol_EURUSD → buy_v3_EURUSD_lot_0.05 → buy_v3_EURUSD_0.05_confirm → EXECUTE
```

### Pattern 5: Settings/Configuration Flow

**Example:** `/setlot` (plugin → strategy → lot size)

```
User clicks: [⚙️ Set Lot Size]
    ↓
Step 1: Plugin selection
    ↓ [User selects V3]
Step 2: Strategy selection
    ↓ [User selects Logic1 OR All Strategies]
Step 3: Lot size selection
    ↓ [User selects 0.05]
Bot updates: Configuration saved
```

**Complete Flow:**

**STEP 1: Plugin Selection**
```
Main Menu > Risk Management
    ↓
[⚙️ Set Lot Size]
    ↓
╔══════════════════════════════════════╗
║  🔌 SELECT PLUGIN                    ║
╠══════════════════════════════════════╣
║  Configure lot size for which plugin?║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  🔵 V3 Combined Logic               │
│  🟢 V6 Price Action                 │
│  🔷 Both Plugins                    │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `setlot_plugin_v3`, `setlot_plugin_v6`, `setlot_plugin_both`

**STEP 2: Strategy Selection (for V3)**
```
🏠 Main Menu > Risk > Set Lot > V3
    ↓
╔══════════════════════════════════════╗
║  📋 SELECT STRATEGY (V3)             ║
╠══════════════════════════════════════╣
║  Configure lot size for which        ║
║  V3 strategy?                        ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  1️⃣ Logic 1 (5M Only)               │
│  2️⃣ Logic 2 (15M Only)              │
│  3️⃣ Logic 3 (1H Only)               │
├─────────────────────────────────────┤
│  🔷 All V3 Strategies               │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `setlot_v3_logic1`, `setlot_v3_logic2`, `setlot_v3_logic3`, `setlot_v3_all`

**STEP 2 ALTERNATIVE: Timeframe Selection (for V6)**
```
🏠 Main Menu > Risk > Set Lot > V6
    ↓
╔══════════════════════════════════════╗
║  📋 SELECT TIMEFRAME (V6)            ║
╠══════════════════════════════════════╣
║  Configure lot size for which        ║
║  V6 timeframe?                       ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  ⏰ 15M   │  ⏰ 30M                  │
├─────────────────────────────────────┤
│  ⏰ 1H    │  ⏰ 4H                   │
├─────────────────────────────────────┤
│  🔷 All V6 Timeframes               │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `setlot_v6_15m`, `setlot_v6_30m`, `setlot_v6_1h`, `setlot_v6_4h`, `setlot_v6_all`

**STEP 3: Lot Size Selection**
```
🏠 Main Menu > Risk > Set Lot > V3 > Logic1
    ↓
╔══════════════════════════════════════╗
║  📊 SELECT LOT SIZE                  ║
╠══════════════════════════════════════╣
║  Current: 0.03 lots                  ║
║  Strategy: Logic 1 (5M)              ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  0.01 lots│  0.03 lots ✅           │
├─────────────────────────────────────┤
│  0.05 lots│  0.10 lots              │
├─────────────────────────────────────┤
│  0.20 lots│  0.50 lots              │
├─────────────────────────────────────┤
│  1.00 lots│  2.00 lots              │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```
**Callback:** `setlot_v3_logic1_0.05`, etc.

**STEP 4: Confirmation**
```
╔══════════════════════════════════════╗
║  ✅ LOT SIZE UPDATED                 ║
╠══════════════════════════════════════╣
║  Strategy: Logic 1 (5M)              ║
║  Old Lot Size: 0.03                  ║
║  New Lot Size: 0.05                  ║
║                                      ║
║  Applied to:                         ║
║  • All Logic 1 signals               ║
║  • Future trades only                ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  ⚙️ Set More Parameters             │
│  🏠 Main Menu                        │
└─────────────────────────────────────┘
```

### Pattern 6: Toggle Commands (ON/OFF)

**Example:** `/logic1` (toggle Logic 1 strategy)

```
User clicks: [1️⃣ Logic 1 Control]
    ↓
Shows: Current status + toggle buttons
    ↓
User clicks: [▶️ Turn ON] or [⏸️ Turn OFF]
    ↓
Bot updates: Status changed
```

**Button Flow:**
```
Main Menu > V3 Strategy Control
    ↓
[1️⃣ Logic 1 Control]
    ↓
Status Screen:
╔══════════════════════════════════════╗
║  1️⃣ LOGIC 1 STRATEGY (5M)            ║
╠══════════════════════════════════════╣
║  Status: ACTIVE ✅                   ║
║  Timeframe: 5 Minutes                ║
║  Symbols: EURUSD, GBPUSD, USDJPY     ║
║  Lot Size: 0.05                      ║
║  Active Trades: 2                    ║
║  Today's P&L: +$45.30                ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  ⏸️ Turn OFF Logic 1                │
├─────────────────────────────────────┤
│  ⚙️ Configure Logic 1                │
│  📊 View Performance                 │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```

If status is OFF, show this instead:
```
┌─────────────────────────────────────┐
│  ▶️ Turn ON Logic 1                 │
├─────────────────────────────────────┤
│  ⚙️ Configure Logic 1                │
│  📊 View Performance                 │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```

**Callback Data:**
- `v3_logic1_on` → Turn ON Logic 1
- `v3_logic1_off` → Turn OFF Logic 1
- `v3_logic1_config` → Open configuration
- `v3_logic1_performance` → Show performance stats

### Pattern 7: List/View Commands

**Example:** `/daily` (plugin → view daily report)

```
User clicks: [📊 Daily Report]
    ↓
Plugin selection
    ↓ [User selects V3]
Bot shows: V3 daily report (no more steps)
```

**Button Flow:**
```
Main Menu > Analytics & Reports
    ↓
[📊 Daily Report]
    ↓
Plugin Selection:
┌─────────────────────────────────────┐
│  🔵 V3 Daily Report                 │
│  🟢 V6 Daily Report                 │
│  🔷 Combined Report                 │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
    ↓ (User clicks "V3 Daily Report")
    ↓
Report Display:
╔══════════════════════════════════════╗
║  📊 V3 DAILY REPORT                  ║
║  Date: 2026-01-21                    ║
╠══════════════════════════════════════╣
║  📈 Overall Performance              ║
║  Total Trades: 15                    ║
║  Wins: 9 (60%)                       ║
║  Losses: 6 (40%)                     ║
║  P&L: +$127.50                       ║
║                                      ║
║  📊 By Strategy                      ║
║  Logic 1: 5 trades, +$45.20          ║
║  Logic 2: 6 trades, +$62.30          ║
║  Logic 3: 4 trades, +$20.00          ║
║                                      ║
║  💱 By Pair                           ║
║  EURUSD: 7 trades, +$65.10           ║
║  GBPUSD: 5 trades, +$42.30           ║
║  USDJPY: 3 trades, +$20.10           ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  📅 Weekly Report                    │
│  📅 Monthly Report                   │
│  📊 Export Data                      │
│  🔄 Refresh                          │
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```

**Callback Data:**
- `analytics_daily_v3` → Show V3 daily report
- `analytics_weekly_v3` → Show weekly report
- `analytics_monthly_v3` → Show monthly report
- `analytics_export_v3_daily` → Export data
- `analytics_refresh` → Refresh data

---

## 🔧 STATE MANAGEMENT

### Conversation State Storage

```python
class ConversationStateManager:
    """Manage multi-step conversation states"""
    
    def __init__(self):
        self.states = {}  # {chat_id: ConversationState}
    
    def get_state(self, chat_id: int):
        """Get or create state for user"""
        if chat_id not in self.states:
            self.states[chat_id] = ConversationState()
        return self.states[chat_id]
    
    def clear_state(self, chat_id: int):
        """Clear state after completion"""
        if chat_id in self.states:
            del self.states[chat_id]

class ConversationState:
    """Store state for multi-step flows"""
    
    def __init__(self):
        self.command = None  # e.g., 'buy', 'setlot'
        self.step = 0  # Current step number
        self.data = {}  # Collected data
        self.breadcrumb = []  # Navigation path
        
    def add_data(self, key: str, value: any):
        """Add data collected in this step"""
        self.data[key] = value
        
    def next_step(self):
        """Move to next step"""
        self.step += 1
        
    def get_data(self, key: str, default=None):
        """Get previously collected data"""
        return self.data.get(key, default)
```

### Example: /buy Flow State

```python
# Step 1: User clicks "Place Buy Order"
state = ConversationState()
state.command = 'buy'
state.step = 1
state.breadcrumb = ['Main Menu', 'Trading Control', 'Buy']

# Step 2: User selects plugin "V3"
state.add_data('plugin', 'v3')
state.next_step()  # step = 2
state.breadcrumb.append('V3 Plugin')

# Step 3: User selects symbol "EURUSD"
state.add_data('symbol', 'EURUSD')
state.next_step()  # step = 3
state.breadcrumb.append('EURUSD')

# Step 4: User selects lot size "0.05"
state.add_data('lot_size', 0.05)
state.next_step()  # step = 4
state.breadcrumb.append('0.05 lots')

# Step 5: Execute
# Access all collected data:
plugin = state.get_data('plugin')  # 'v3'
symbol = state.get_data('symbol')  # 'EURUSD'
lot_size = state.get_data('lot_size')  # 0.05

# Execute trade
execute_buy_order(plugin, symbol, lot_size)

# Clear state
clear_state(chat_id)
```

---

## 📊 CALLBACK DATA NAMING

### Standard Format

```
{category}_{action}_{target}_{value}
```

**Examples:**
- `trading_buy_v3_EURUSD_0.05_confirm` → Execute buy
- `risk_setlot_v3_logic1_0.05` → Set lot size
- `v3_logic1_on` → Turn on Logic 1
- `analytics_daily_v3` → Show V3 daily report
- `system_pause_v3` → Pause V3 plugin

### Callback Data Structure

```python
def parse_callback_data(callback_data: str) -> dict:
    """Parse callback data into components"""
    
    parts = callback_data.split('_')
    
    return {
        'category': parts[0],  # e.g., 'trading', 'risk', 'v3'
        'action': parts[1],  # e.g., 'buy', 'setlot', 'logic1'
        'target': parts[2] if len(parts) > 2 else None,  # e.g., 'v3', 'EURUSD'
        'value': parts[3] if len(parts) > 3 else None,  # e.g., '0.05', 'confirm'
        'extra': parts[4:] if len(parts) > 4 else []  # Additional data
    }

# Example:
# parse_callback_data('trading_buy_v3_EURUSD_0.05_confirm')
# Returns:
# {
#     'category': 'trading',
#     'action': 'buy',
#     'target': 'v3',
#     'value': 'EURUSD',
#     'extra': ['0.05', 'confirm']
# }
```

### Callback Data Registry

```python
CALLBACK_REGISTRY = {
    # System Commands
    'system_status': 'Show bot status',
    'system_pause_v3': 'Pause V3 plugin',
    'system_pause_v6': 'Pause V6 plugin',
    'system_pause_both': 'Pause both plugins',
    'system_resume_v3': 'Resume V3 plugin',
    'system_resume_v6': 'Resume V6 plugin',
    
    # Trading Commands
    'trading_positions_v3': 'Show V3 positions',
    'trading_positions_v6': 'Show V6 positions',
    'trading_positions_both': 'Show all positions',
    'trading_buy_start': 'Start buy flow',
    'trading_sell_start': 'Start sell flow',
    'trading_closeall_v3': 'Close all V3 positions',
    
    # Risk Commands
    'risk_setlot_start': 'Start setlot flow',
    'risk_setsl_start': 'Start setsl flow',
    'risk_settp_start': 'Start settp flow',
    
    # V3 Commands
    'v3_logic1_on': 'Turn on Logic 1',
    'v3_logic1_off': 'Turn off Logic 1',
    'v3_logic1_config': 'Configure Logic 1',
    
    # V6 Commands
    'v6_15m_on': 'Turn on 15M timeframe',
    'v6_15m_off': 'Turn off 15M timeframe',
    
    # Analytics
    'analytics_daily_v3': 'Show V3 daily report',
    'analytics_weekly_v3': 'Show V3 weekly report',
    
    # Navigation
    'nav_back': 'Go back one level',
    'nav_main_menu': 'Return to main menu',
}
```

---

## 🎨 BUTTON LAYOUT GUIDELINES

### Button Sizes

**Single Button (Full Width):**
```
┌─────────────────────────────────────┐
│  📊 View Full Dashboard             │
└─────────────────────────────────────┘
```

**Two Buttons (50/50):**
```
┌─────────────────────────────────────┐
│  ✅ Confirm  │  ❌ Cancel           │
└─────────────────────────────────────┘
```

**Three Buttons (33/33/33):**
```
┌─────────────────────────────────────┐
│  🔵 V3  │  🟢 V6  │  🔷 Both       │
└─────────────────────────────────────┘
```

**Four Buttons (2x2 Grid):**
```
┌─────────────────────────────────────┐
│  0.01 lots│  0.03 lots              │
├─────────────────────────────────────┤
│  0.05 lots│  0.10 lots              │
└─────────────────────────────────────┘
```

### Max Buttons Per Row

- **Simple options:** 2 buttons max
- **Grid layout:** 2x2 or 3x3 max
- **Long labels:** 1 button per row

### Navigation Buttons (Always at Bottom)

```
┌─────────────────────────────────────┐
│  [Main content buttons here]        │
├─────────────────────────────────────┤
│  ⬅️ Back  │  🏠 Main Menu            │
└─────────────────────────────────────┘
```

Or single row:
```
┌─────────────────────────────────────┐
│  [Main content buttons here]        │
├─────────────────────────────────────┤
│         ⬅️ Back to Trading           │
│         🏠 Main Menu                 │
└─────────────────────────────────────┘
```

---

## ✅ ERROR PREVENTION

### Callback Data Validation

```python
async def handle_callback_query(update, context):
    """Handle button callback with validation"""
    
    query = update.callback_query
    callback_data = query.data
    chat_id = query.message.chat_id
    
    # Validate callback data exists in registry
    if callback_data not in CALLBACK_REGISTRY:
        await query.answer("Invalid button action!")
        logger.error(f"Unknown callback: {callback_data}")
        return
    
    # Answer callback (required!)
    await query.answer()
    
    # Parse callback data
    parsed = parse_callback_data(callback_data)
    
    # Route to appropriate handler
    await route_callback(parsed, chat_id, query.message.message_id)
```

### Handler Registration

```python
# Register ALL callback patterns
application.add_handler(CallbackQueryHandler(
    handle_system_callbacks,
    pattern=r'^system_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_trading_callbacks,
    pattern=r'^trading_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_risk_callbacks,
    pattern=r'^risk_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_v3_callbacks,
    pattern=r'^v3_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_v6_callbacks,
    pattern=r'^v6_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_analytics_callbacks,
    pattern=r'^analytics_.*'
))

application.add_handler(CallbackQueryHandler(
    handle_navigation_callbacks,
    pattern=r'^nav_.*'
))

# Catch-all for unknown callbacks
application.add_handler(CallbackQueryHandler(
    handle_unknown_callback
))
```

### Button State Validation

```python
async def validate_button_state(chat_id: int, callback_data: str) -> bool:
    """Validate if button action is valid for current state"""
    
    state = conversation_state_manager.get_state(chat_id)
    
    # Check if we're in the right step
    if callback_data.startswith('buy_'):
        # Buy flow - validate step
        if 'confirm' in callback_data and state.step < 4:
            return False  # Can't confirm before collecting all data
    
    return True
```

---

## 📋 IMPLEMENTATION CHECKLIST

### Core Components ✅
- [ ] ConversationStateManager class
- [ ] ConversationState class
- [ ] Callback data parser
- [ ] Callback registry
- [ ] Button layout builder

### Handler System ✅
- [ ] System command handlers
- [ ] Trading command handlers
- [ ] Risk command handlers
- [ ] V3 strategy handlers
- [ ] V6 timeframe handlers
- [ ] Analytics handlers
- [ ] Navigation handlers
- [ ] Unknown callback handler

### Flow Implementations ✅
- [ ] Simple direct commands (Pattern 1)
- [ ] Single selection (Pattern 2)
- [ ] Multi-step with plugin (Pattern 3)
- [ ] Complex 4-level flows (Pattern 4)
- [ ] Settings/config flows (Pattern 5)
- [ ] Toggle commands (Pattern 6)
- [ ] List/view commands (Pattern 7)

### Validation & Error Handling ✅
- [ ] Callback data validation
- [ ] Handler registration (all patterns)
- [ ] Button state validation
- [ ] Error messages
- [ ] Unknown callback handling

---

**STATUS:** Zero-Typing Button Flow System Complete ✅

