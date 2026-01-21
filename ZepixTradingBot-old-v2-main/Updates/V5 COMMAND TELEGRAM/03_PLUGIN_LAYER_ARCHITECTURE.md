# TELEGRAM BOT - PLUGIN LAYER ARCHITECTURE
**Version:** V5.0  
**Created:** January 21, 2026  
**Purpose:** Define which categories need plugin selection and integration strategy

---

## 🎯 OVERVIEW

**Plugin Selection:** Mechanism to choose V3, V6, or Both before executing plugin-aware commands

**Total Commands:** 144  
**Plugin-Aware:** 83 commands (58%)  
**System Commands:** 61 commands (42%)

---

## 📊 CATEGORY CLASSIFICATION

### Categories with Plugin Selection (8 categories, 83 commands)

| Category | Commands | Plugin Selection Required |
|----------|----------|--------------------------|
| 📊 Trading Control | 15/18 | ✅ YES (except balance, equity, trades) |
| 🛡️ Risk Management | 12/15 | ✅ YES (except global risk tier view) |
| 🔵 V3 Strategy Control | 12/12 | ✅ YES (all V3-specific) |
| 🟢 V6 Timeframe Control | 24/30 | ✅ YES (except global V6 status) |
| 📈 Analytics & Reports | 12/15 | ✅ YES (except combined dashboard) |
| 🔄 Re-Entry & Autonomous | 13/15 | ✅ YES (except global autonomous status) |
| 💰 Dual Order & Profit | 6/8 | ✅ YES (except profit stats view) |
| 🔌 Plugin Management | 5/10 | ✅ YES (when managing specific plugins) |

### Categories WITHOUT Plugin Selection (4 categories, 61 commands)

| Category | Commands | Reason |
|----------|----------|--------|
| 🎛️ System Commands | 10/10 | ❌ NO - Global bot control |
| 🕐 Session Management | 6/6 | ❌ NO - Global session info |
| 🔊 Voice & Notifications | 7/7 | ❌ NO - Global settings |
| ⚙️ Settings | Multiple | ❌ NO - Global configuration |

---

## 🔌 PLUGIN SELECTION FLOW

### Standard Flow for Plugin-Aware Commands

```
User clicks command button
        ↓
Check: Is command plugin-aware?
        ↓
    YES → Show Plugin Selection Screen
        ↓
User selects: V3, V6, or Both
        ↓
Store selection in context (5 min expiry)
        ↓
Execute command with plugin context
        ↓
Clear context after execution
```

### Plugin Selection Screen (Standard)

```
╔══════════════════════════════════════╗
║   🔌 SELECT PLUGIN FOR /positions    ║
╠══════════════════════════════════════╣
║  View positions for which plugin?    ║
║                                      ║
║  🔵 V3 Combined Logic                ║
║     └─ 3 strategies (5M/15M/1H)      ║
║                                      ║
║  🟢 V6 Price Action                  ║
║     └─ 4 timeframes (15M/30M/1H/4H)  ║
║                                      ║
║  🔷 Both Plugins                     ║
║     └─ Combined data                 ║
╚══════════════════════════════════════╝

┌─────────────────────────────────────┐
│  🔵 V3 Only   │  🟢 V6 Only         │
├─────────────────────────────────────┤
│         🔷 Both Plugins             │
├─────────────────────────────────────┤
│         ❌ Cancel                    │
└─────────────────────────────────────┘

Callback Data:
- plugin_select_v3_positions
- plugin_select_v6_positions
- plugin_select_both_positions
```

---

## 📋 DETAILED COMMAND MAPPING

### CATEGORY 1: System Commands (NO PLUGIN SELECTION)

| Command | Plugin Selection | Reason |
|---------|-----------------|--------|
| `/start` | ❌ NO | Main menu entry |
| `/help` | ❌ NO | Global help |
| `/status` | ⚠️ OPTIONAL | Can show combined or filtered |
| `/pause` | ⚠️ OPTIONAL | Can pause V3, V6, or Both |
| `/resume` | ⚠️ OPTIONAL | Can resume V3, V6, or Both |
| `/restart` | ❌ NO | Global restart |
| `/shutdown` | ❌ NO | Global shutdown |
| `/config` | ❌ NO | Global config |
| `/health` | ❌ NO | Global health |
| `/version` | ❌ NO | Global version |

**Special Case: `/status`, `/pause`, `/resume`**
- These can be either global OR plugin-specific
- Show both options:
  ```
  ┌─────────────────────────────────────┐
  │  📊 Global Status                    │
  ├─────────────────────────────────────┤
  │  🔵 V3 Status │  🟢 V6 Status       │
  └─────────────────────────────────────┘
  ```

### CATEGORY 2: Trading Control (PLUGIN SELECTION REQUIRED)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/positions` | ✅ YES | V3 and V6 have separate positions |
| `/pnl` | ✅ YES | Different P&L for each plugin |
| `/buy` | ✅ YES | Place order in specific plugin |
| `/sell` | ✅ YES | Place order in specific plugin |
| `/close` | ✅ YES | Close plugin-specific position |
| `/closeall` | ✅ YES | Close all for V3, V6, or Both |
| `/orders` | ✅ YES | Plugin-specific pending orders |
| `/history` | ✅ YES | Plugin-specific trade history |
| `/price` | ⚠️ OPTIONAL | Can be global or plugin-filtered |
| `/spread` | ⚠️ OPTIONAL | Can be global or plugin-filtered |
| `/partial` | ✅ YES | Partial close of plugin position |
| `/signals` | ✅ YES | Plugin-specific signals |
| `/filters` | ✅ YES | Plugin-specific entry filters |
| `/balance` | ❌ NO | Global account balance |
| `/equity` | ❌ NO | Global account equity |
| `/margin` | ❌ NO | Global margin info |
| `/symbols` | ❌ NO | Global symbol list |
| `/trades` | ⚠️ OPTIONAL | Can show all or plugin-filtered |

**Selection Flow Example: `/positions`**
```
User: /positions
↓
Bot: Shows plugin selection (V3, V6, Both)
↓
User: Selects V3
↓
Bot: Shows only V3 positions
```

### CATEGORY 3: Risk Management (PLUGIN SELECTION REQUIRED)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/setlot` | ✅ YES | V3 and V6 have different lot sizes |
| `/setsl` | ✅ YES | Different SL for each plugin/strategy |
| `/settp` | ✅ YES | Different TP for each plugin/strategy |
| `/dailylimit` | ✅ YES | Can set per-plugin or global |
| `/maxloss` | ✅ YES | Plugin-specific max loss |
| `/maxprofit` | ✅ YES | Plugin-specific max profit |
| `/risktier` | ✅ YES | Different tier for V3 vs V6 |
| `/slsystem` | ✅ YES | Plugin-specific SL system |
| `/trailsl` | ✅ YES | Plugin-specific trailing SL |
| `/breakeven` | ✅ YES | Plugin-specific breakeven |
| `/protection` | ✅ YES | Plugin-specific protection |
| `/multiplier` | ✅ YES | Plugin-specific multiplier |
| `/maxtrades` | ⚠️ OPTIONAL | Can be global or per-plugin |
| `/drawdownlimit` | ⚠️ OPTIONAL | Can be global or per-plugin |
| `/risk` | ❌ NO | Opens risk menu (selects inside) |

**Selection Flow Example: `/setlot`**
```
User: /setlot
↓
Bot: Plugin selection (V3, V6, Both)
↓
User: Selects V3
↓
Bot: Shows V3 strategies (Logic1/2/3)
↓
User: Selects "All V3 Strategies"
↓
Bot: Shows lot size options
↓
User: Selects 0.05 lots
↓
Bot: ✅ All V3 strategies now use 0.05 lots
```

### CATEGORY 4: V3 Strategy Control (ALWAYS V3 CONTEXT)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/logic1` | ❌ NO* | *Auto-context to V3 |
| `/logic2` | ❌ NO* | *Auto-context to V3 |
| `/logic3` | ❌ NO* | *Auto-context to V3 |
| `/logic1_on` | ❌ NO* | *Auto-context to V3 |
| `/logic1_off` | ❌ NO* | *Auto-context to V3 |
| `/logic2_on` | ❌ NO* | *Auto-context to V3 |
| `/logic2_off` | ❌ NO* | *Auto-context to V3 |
| `/logic3_on` | ❌ NO* | *Auto-context to V3 |
| `/logic3_off` | ❌ NO* | *Auto-context to V3 |
| `/logic1_config` | ❌ NO* | *Auto-context to V3 |
| `/logic2_config` | ❌ NO* | *Auto-context to V3 |
| `/logic3_config` | ❌ NO* | *Auto-context to V3 |
| `/v3` | ❌ NO* | *Auto-context to V3 |
| `/v3_config` | ❌ NO* | *Auto-context to V3 |
| `/logic_status` | ❌ NO* | *Auto-context to V3 |

**Special Note:** These commands are V3-specific, so they automatically use V3 context. NO selection screen needed!

### CATEGORY 5: V6 Timeframe Control (ALWAYS V6 CONTEXT)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/v6_status` | ❌ NO* | *Auto-context to V6 |
| `/v6_control` | ❌ NO* | *Auto-context to V6 |
| `/v6_config` | ❌ NO* | *Auto-context to V6 |
| `/v6_menu` | ❌ NO* | *Auto-context to V6 |
| `/tf1m_on` | ❌ NO* | *Auto-context to V6 |
| `/tf1m_off` | ❌ NO* | *Auto-context to V6 |
| `/tf5m_on` | ❌ NO* | *Auto-context to V6 |
| `/tf5m_off` | ❌ NO* | *Auto-context to V6 |
| `/tf15m_on` | ❌ NO* | *Auto-context to V6 |
| `/tf15m_off` | ❌ NO* | *Auto-context to V6 |
| `/tf30m_on` | ❌ NO* | *Auto-context to V6 |
| `/tf30m_off` | ❌ NO* | *Auto-context to V6 |
| `/tf1h_on` | ❌ NO* | *Auto-context to V6 |
| `/tf1h_off` | ❌ NO* | *Auto-context to V6 |
| `/tf4h_on` | ❌ NO* | *Auto-context to V6 |
| `/tf4h_off` | ❌ NO* | *Auto-context to V6 |
| `/tf15m` | ❌ NO* | *Auto-context to V6 |
| `/tf30m` | ❌ NO* | *Auto-context to V6 |
| `/tf1h` | ❌ NO* | *Auto-context to V6 |
| `/tf4h` | ❌ NO* | *Auto-context to V6 |
| `/v6_performance` | ❌ NO* | *Auto-context to V6 |
| (all 30 V6 commands) | ❌ NO* | *Auto-context to V6 |

**Special Note:** All V6 commands automatically use V6 context!

### CATEGORY 6: Analytics & Reports (PLUGIN SELECTION REQUIRED)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/daily` | ✅ YES | V3 vs V6 daily report |
| `/weekly` | ✅ YES | V3 vs V6 weekly report |
| `/monthly` | ✅ YES | V3 vs V6 monthly report |
| `/compare` | ❌ NO | Always compares both |
| `/pairreport` | ✅ YES | Plugin-specific pair stats |
| `/strategyreport` | ✅ YES | Plugin-specific strategy stats |
| `/tpreport` | ✅ YES | Plugin-specific TP stats |
| `/stats` | ✅ YES | Plugin-specific stats |
| `/winrate` | ✅ YES | Plugin-specific win rate |
| `/drawdown` | ✅ YES | Plugin-specific drawdown |
| `/profit_stats` | ✅ YES | Plugin-specific profit stats |
| `/performance` | ⚠️ OPTIONAL | Can be global or filtered |
| `/dashboard` | ❌ NO | Shows combined dashboard |
| `/analytics` | ❌ NO | Opens analytics menu |
| `/export` | ✅ YES | Export plugin-specific data |

**Selection Flow Example: `/daily`**
```
User: /daily
↓
Bot: Plugin selection (V3, V6, Both)
↓
User: Selects V3
↓
Bot: Shows V3 daily report with:
     - V3 trades only
     - Logic1/2/3 breakdown
     - V3 pairs
     - V3 sessions
```

### CATEGORY 7: Re-Entry & Autonomous (PLUGIN SELECTION REQUIRED)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/slhunt` | ✅ YES | V3 and V6 have separate SL hunt |
| `/sl_hunt` | ✅ YES | (Same as slhunt) |
| `/tpcontinue` | ✅ YES | V3 and V6 have separate TP cont |
| `/tp_cont` | ✅ YES | (Same as tpcontinue) |
| `/reentry` | ✅ YES | Plugin-specific re-entry |
| `/reentry_config` | ✅ YES | Configure per plugin |
| `/recovery` | ✅ YES | Plugin-specific recovery |
| `/cooldown` | ✅ YES | Plugin-specific cooldown |
| `/chains` | ✅ YES | Plugin-specific chain status |
| `/autonomous` | ⚠️ OPTIONAL | Can control per plugin or both |
| `/chainlimit` | ✅ YES | Plugin-specific chain limit |
| `/reentry_v3` | ❌ NO* | *Auto-context to V3 |
| `/reentry_v6` | ❌ NO* | *Auto-context to V6 |
| `/autonomous_control` | ⚠️ OPTIONAL | Can be global or per-plugin |
| `/sl_hunt_stats` | ✅ YES | Plugin-specific stats |

### CATEGORY 8: Dual Order & Profit (PLUGIN SELECTION REQUIRED)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/dualorder` | ✅ YES | Configure per plugin |
| `/orderb` | ✅ YES | Plugin-specific Order B |
| `/order_b` | ✅ YES | (Same as orderb) |
| `/profit` | ✅ YES | Plugin-specific profit booking |
| `/booking` | ✅ YES | Plugin-specific booking |
| `/levels` | ✅ YES | Plugin-specific profit levels |
| `/partial` | ✅ YES | Plugin-specific partial close |
| `/profit_stats` | ⚠️ OPTIONAL | Can be global or per-plugin |

### CATEGORY 9: Plugin Management (CONTEXTUAL)

| Command | Plugin Selection | Why |
|---------|-----------------|-----|
| `/plugins` | ❌ NO | Shows all plugins |
| `/plugin` | ❌ NO | Opens plugin menu |
| `/enable` | ✅ YES | Select which to enable |
| `/disable` | ✅ YES | Select which to disable |
| `/upgrade` | ✅ YES | Select which to upgrade |
| `/rollback` | ✅ YES | Select which to rollback |
| `/shadow` | ✅ YES | Select which for shadow mode |
| `/plugin_toggle` | ✅ YES | Select which to toggle |
| `/v3_toggle` | ❌ NO* | *Auto-context to V3 |
| `/v6_toggle` | ❌ NO* | *Auto-context to V6 |
| `/plugin_status` | ❌ NO | Shows all plugin status |

### CATEGORY 10: Session Management (NO PLUGIN SELECTION)

All session commands are GLOBAL:
- `/session` - Global session overview
- `/london` - London session info
- `/newyork` - New York session info
- `/tokyo` - Tokyo session info
- `/sydney` - Sydney session info
- `/overlap` - Session overlap info

### CATEGORY 11: Voice & Notifications (NO PLUGIN SELECTION)

All voice/notification commands are GLOBAL:
- `/voice` - Global voice settings
- `/voice_menu` - Voice menu
- `/voice_test` - Test voice
- `/mute` - Global mute
- `/unmute` - Global unmute
- `/notifications` - Global notification settings
- `/clock` - Global clock display

---

## 🔄 PLUGIN CONTEXT MANAGEMENT

### Context Storage

```python
class PluginContextManager:
    """Manage plugin context per user"""
    
    def __init__(self):
        self.contexts = {}  # {chat_id: {'plugin': 'v3', 'command': '/positions', 'timestamp': ...}}
        self.expiry_seconds = 300  # 5 minutes
    
    def set_context(self, chat_id: int, plugin: str, command: str):
        """
        Store plugin selection for user.
        
        Args:
            chat_id: User's chat ID
            plugin: 'v3', 'v6', or 'both'
            command: Command being executed
        """
        from datetime import datetime
        
        self.contexts[chat_id] = {
            'plugin': plugin,
            'command': command,
            'timestamp': datetime.now()
        }
    
    def get_context(self, chat_id: int) -> Optional[str]:
        """
        Get stored plugin context for user.
        
        Returns:
            'v3', 'v6', 'both', or None if expired
        """
        from datetime import datetime, timedelta
        
        if chat_id not in self.contexts:
            return None
        
        ctx = self.contexts[chat_id]
        
        # Check expiry
        if datetime.now() - ctx['timestamp'] > timedelta(seconds=self.expiry_seconds):
            del self.contexts[chat_id]
            return None
        
        return ctx['plugin']
    
    def clear_context(self, chat_id: int):
        """Clear context after command execution"""
        if chat_id in self.contexts:
            del self.contexts[chat_id]
```

### Command Interceptor

```python
class CommandInterceptor:
    """Intercept plugin-aware commands"""
    
    # Commands that need plugin selection
    PLUGIN_AWARE_COMMANDS = {
        # Trading
        'positions', 'pnl', 'buy', 'sell', 'close', 'closeall',
        'orders', 'history', 'partial', 'signals', 'filters',
        
        # Risk
        'setlot', 'setsl', 'settp', 'dailylimit', 'maxloss', 'maxprofit',
        'risktier', 'slsystem', 'trailsl', 'breakeven', 'protection', 'multiplier',
        
        # Analytics
        'daily', 'weekly', 'monthly', 'pairreport', 'strategyreport', 
        'tpreport', 'stats', 'winrate', 'drawdown', 'profit_stats', 'export',
        
        # Re-entry
        'slhunt', 'sl_hunt', 'tpcontinue', 'tp_cont', 'reentry', 'reentry_config',
        'recovery', 'cooldown', 'chains', 'chainlimit', 'sl_hunt_stats',
        
        # Dual Order
        'dualorder', 'orderb', 'order_b', 'profit', 'booking', 'levels', 'partial',
        
        # Plugin Management
        'enable', 'disable', 'upgrade', 'rollback', 'shadow', 'plugin_toggle',
    }
    
    # Commands with auto-context (V3-specific)
    V3_AUTO_CONTEXT = {
        'logic1', 'logic2', 'logic3',
        'logic1_on', 'logic1_off', 'logic2_on', 'logic2_off', 'logic3_on', 'logic3_off',
        'logic1_config', 'logic2_config', 'logic3_config',
        'v3', 'v3_config', 'logic_status', 'v3_toggle', 'reentry_v3',
    }
    
    # Commands with auto-context (V6-specific)
    V6_AUTO_CONTEXT = {
        'v6_status', 'v6_control', 'v6_config', 'v6_menu', 'v6_performance',
        'tf1m_on', 'tf1m_off', 'tf5m_on', 'tf5m_off',
        'tf15m_on', 'tf15m_off', 'tf30m_on', 'tf30m_off',
        'tf1h_on', 'tf1h_off', 'tf4h_on', 'tf4h_off',
        'tf15m', 'tf30m', 'tf1h', 'tf4h',
        'v6_toggle', 'reentry_v6',
        # ... all 30 V6 commands
    }
    
    def __init__(self, context_manager: PluginContextManager):
        self.context_manager = context_manager
    
    def should_show_selection(self, command: str, chat_id: int) -> bool:
        """
        Check if plugin selection screen should be shown.
        
        Returns:
            True if selection screen needed, False otherwise
        """
        
        # Strip leading slash
        cmd = command.lstrip('/')
        
        # Auto-context commands - no selection needed
        if cmd in self.V3_AUTO_CONTEXT:
            self.context_manager.set_context(chat_id, 'v3', command)
            return False
        
        if cmd in self.V6_AUTO_CONTEXT:
            self.context_manager.set_context(chat_id, 'v6', command)
            return False
        
        # Plugin-aware commands - check if context exists
        if cmd in self.PLUGIN_AWARE_COMMANDS:
            existing_context = self.context_manager.get_context(chat_id)
            
            if existing_context:
                # Context exists and not expired, use it
                return False
            else:
                # No context, show selection
                return True
        
        # Not plugin-aware, no selection needed
        return False
```

---

## 📊 SUMMARY

### Plugin Selection Statistics

| Selection Type | Count | Percentage |
|---------------|-------|------------|
| **Always Show Selection** | 83 | 58% |
| **V3 Auto-Context** | 15 | 10% |
| **V6 Auto-Context** | 30 | 21% |
| **No Selection Needed** | 16 | 11% |
| **TOTAL** | 144 | 100% |

### Implementation Strategy

1. ✅ **Create PluginContextManager** - Store user selections with 5-min expiry
2. ✅ **Create CommandInterceptor** - Check if selection needed
3. ✅ **Create Plugin Selection UI Builder** - Consistent selection screen
4. ✅ **Integrate with Command Handlers** - Check context before execution
5. ✅ **Add Auto-Context Logic** - Automatic V3/V6 context for specific commands

---

**STATUS:** Plugin Layer Architecture Complete ✅

