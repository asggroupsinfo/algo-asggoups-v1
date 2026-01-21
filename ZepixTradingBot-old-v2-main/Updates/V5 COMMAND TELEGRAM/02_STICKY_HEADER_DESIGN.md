# TELEGRAM BOT - STICKY HEADER DESIGN
**Version:** V5.0  
**Created:** January 21, 2026  
**Purpose:** Fixed header with clock, session, live symbols

---

## 🎯 OVERVIEW

**Purpose:** Every message from bot will have a FIXED HEADER at the top showing:
- 🕐 Current time (GMT)
- 📊 Active session
- 💱 Live symbol prices
- 🤖 Bot status indicator

**Update Frequency:** Header auto-refreshes every 30 seconds

---

## 📱 STICKY HEADER DESIGN

### Full Header Layout

```
╔══════════════════════════════════════╗
║   🤖 ZEPIX TRADING BOT V5.0          ║
╠══════════════════════════════════════╣
║  📊 Status: ACTIVE ✅                ║
║  🕐 Time: 14:35:22 GMT               ║
║  📈 Session: LONDON (Active)         ║
║  💱 EURUSD: 1.0825 | GBPUSD: 1.2645  ║
╚══════════════════════════════════════╝
```

### Compact Header (for long messages)

```
🤖 ACTIVE ✅ | 🕐 14:35 GMT | 📈 LONDON
💱 EUR:1.0825 GBP:1.2645 USD:151.20
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🕐 CLOCK COMPONENT

### Display Format

```
🕐 Time: 14:35:22 GMT
```

### Features
- **Real-time:** Updates every second (client-side)
- **Timezone:** Always GMT (trading standard)
- **Format:** HH:MM:SS
- **Visual:** Clock emoji + formatted time

### Implementation Logic

```python
def get_current_time_display():
    """Get formatted current time for header"""
    from datetime import datetime
    
    current_time = datetime.utcnow()
    time_str = current_time.strftime("%H:%M:%S")
    
    return f"🕐 Time: {time_str} GMT"
```

### Dynamic Updates

```python
# For Telegram messages, time is static when sent
# But can be updated via edit_message:

async def update_header_time(message_id, chat_id):
    """Update time in existing message"""
    new_time = get_current_time_display()
    # Edit message with new time
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=updated_content_with_new_time
    )
```

---

## 📈 SESSION COMPONENT

### Session Display

```
📈 Session: LONDON (Active)
```

### Session States

**1. Active Session:**
```
📈 Session: LONDON (Active) ✅
```

**2. Multiple Sessions (Overlap):**
```
📈 Sessions: LONDON + NEW YORK (Overlap) 🔥
```

**3. Between Sessions:**
```
📈 Session: Transition (NY closing soon) ⏳
```

**4. No Session:**
```
📈 Session: After Hours ⛔
```

### Session Data

```python
TRADING_SESSIONS = {
    'SYDNEY': {
        'start': '00:00',
        'end': '09:00',
        'emoji': '🇦🇺',
        'timezone': 'GMT'
    },
    'TOKYO': {
        'start': '01:00',
        'end': '10:00',
        'emoji': '🇯🇵',
        'timezone': 'GMT'
    },
    'LONDON': {
        'start': '08:00',
        'end': '17:00',
        'emoji': '🇬🇧',
        'timezone': 'GMT'
    },
    'NEW YORK': {
        'start': '13:00',
        'end': '22:00',
        'emoji': '🇺🇸',
        'timezone': 'GMT'
    }
}

def get_current_session():
    """Get active trading session(s)"""
    from datetime import datetime
    
    current_time = datetime.utcnow().time()
    active_sessions = []
    
    for session_name, details in TRADING_SESSIONS.items():
        start = datetime.strptime(details['start'], '%H:%M').time()
        end = datetime.strptime(details['end'], '%H:%M').time()
        
        if start <= current_time < end:
            active_sessions.append(session_name)
    
    if len(active_sessions) == 0:
        return "After Hours ⛔", []
    elif len(active_sessions) == 1:
        return f"{active_sessions[0]} (Active) ✅", active_sessions
    else:
        return f"{' + '.join(active_sessions)} (Overlap) 🔥", active_sessions

# Usage:
session_text, active_list = get_current_session()
# Returns: "LONDON (Active) ✅", ['LONDON']
# Or: "LONDON + NEW YORK (Overlap) 🔥", ['LONDON', 'NEW YORK']
```

### Session Time Remaining

```python
def get_session_time_remaining():
    """Get time until session ends"""
    from datetime import datetime, timedelta
    
    current_time = datetime.utcnow()
    session_text, active_sessions = get_current_session()
    
    if not active_sessions:
        # Find next session
        next_session = get_next_session()
        return f"Next: {next_session['name']} in {next_session['time_until']}"
    
    # Get end time of current session
    session = TRADING_SESSIONS[active_sessions[0]]
    end_time = datetime.strptime(session['end'], '%H:%M').time()
    end_datetime = datetime.combine(current_time.date(), end_time)
    
    if end_datetime < current_time:
        end_datetime += timedelta(days=1)
    
    time_remaining = end_datetime - current_time
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    
    return f"{hours}h {minutes}m left"
```

### Enhanced Session Display

```
📈 Session: LONDON (Active) ✅ | 2h 25m left
```

Or for overlap:

```
📈 Sessions: LONDON + NY (Overlap) 🔥 | 45m left
```

---

## 💱 LIVE SYMBOLS COMPONENT

### Display Format

```
💱 EURUSD: 1.0825 | GBPUSD: 1.2645
```

### Multi-Symbol Display

```
💱 EUR:1.0825 GBP:1.2645 USD:151.20 AUD:0.6420
```

### Symbol Configuration

```python
# Default symbols to show in header
DEFAULT_HEADER_SYMBOLS = [
    'EURUSD',  # Euro vs US Dollar
    'GBPUSD',  # British Pound vs US Dollar  
    'USDJPY',  # US Dollar vs Japanese Yen
    'AUDUSD',  # Australian Dollar vs US Dollar
]

# User can customize which symbols to show
# Stored in user settings
```

### Price Fetching

```python
async def get_live_symbol_prices():
    """Fetch current prices for header symbols"""
    
    prices = {}
    
    # Get from MT5 (if connected)
    if mt5_client and mt5_client.is_connected():
        for symbol in DEFAULT_HEADER_SYMBOLS:
            try:
                tick = mt5_client.get_tick(symbol)
                if tick:
                    # Get bid price (or mid price)
                    price = (tick.bid + tick.ask) / 2
                    prices[symbol] = round(price, 5)
            except Exception as e:
                logger.error(f"Failed to get price for {symbol}: {e}")
                prices[symbol] = None
    
    return prices

# Example return:
# {
#     'EURUSD': 1.08245,
#     'GBPUSD': 1.26450,
#     'USDJPY': 151.205,
#     'AUDUSD': 0.64198
# }
```

### Price Formatting

```python
def format_symbol_prices(prices):
    """Format prices for header display"""
    
    formatted_parts = []
    
    for symbol, price in prices.items():
        if price is None:
            continue
        
        # Shorten symbol name for compact display
        short_symbol = symbol.replace('USD', '').replace('JPY', '')
        if not short_symbol:
            short_symbol = symbol[:3]
        
        # Format price based on symbol
        if 'JPY' in symbol:
            price_str = f"{price:.2f}"
        else:
            price_str = f"{price:.4f}"
        
        formatted_parts.append(f"{short_symbol}:{price_str}")
    
    return " ".join(formatted_parts)

# Example:
# Input: {'EURUSD': 1.08245, 'GBPUSD': 1.26450}
# Output: "EUR:1.0825 GBP:1.2645"
```

### Price Change Indicators

```python
def get_price_with_change(symbol, current_price, previous_price):
    """Show price with change indicator"""
    
    if previous_price is None:
        return f"{symbol}: {current_price}"
    
    change = current_price - previous_price
    
    if change > 0:
        indicator = "🟢⬆"
    elif change < 0:
        indicator = "🔴⬇"
    else:
        indicator = "⚪➡"
    
    return f"{symbol}: {current_price} {indicator}"

# Example output:
# "EURUSD: 1.0825 🟢⬆"  # Price going up
# "GBPUSD: 1.2640 🔴⬇"  # Price going down
```

### Enhanced Symbol Display with Changes

```
💱 EUR:1.0825🟢⬆ GBP:1.2640🔴⬇ USD:151.20➡
```

---

## 🤖 BOT STATUS COMPONENT

### Status Display

```
📊 Status: ACTIVE ✅
```

### Status States

**1. Fully Active:**
```
📊 Status: ACTIVE ✅
```

**2. Paused:**
```
📊 Status: PAUSED ⏸️
```

**3. Partially Active:**
```
📊 Status: PARTIAL (V3:ON, V6:OFF) ⚠️
```

**4. Error State:**
```
📊 Status: ERROR ❌ (MT5 Disconnected)
```

**5. Maintenance:**
```
📊 Status: MAINTENANCE 🔧
```

### Status Logic

```python
def get_bot_status():
    """Get current bot status for header"""
    
    # Check MT5 connection
    mt5_connected = mt5_client and mt5_client.is_connected()
    
    # Check plugin status
    v3_active = plugin_manager.is_active('v3')
    v6_active = plugin_manager.is_active('v6')
    
    # Check if paused
    is_paused = trading_engine.is_paused()
    
    # Determine status
    if not mt5_connected:
        return "ERROR ❌ (MT5 Disconnected)", "error"
    
    if is_paused:
        return "PAUSED ⏸️", "paused"
    
    if v3_active and v6_active:
        return "ACTIVE ✅", "active"
    elif v3_active or v6_active:
        active_plugin = "V3" if v3_active else "V6"
        inactive_plugin = "V6" if v3_active else "V3"
        return f"PARTIAL ({active_plugin}:ON, {inactive_plugin}:OFF) ⚠️", "partial"
    else:
        return "INACTIVE ⛔ (All Plugins OFF)", "inactive"

# Usage:
status_text, status_type = get_bot_status()
```

---

## 🎨 HEADER TEMPLATE SYSTEM

### Template Structure

```python
class StickyHeader:
    """Sticky header builder for all bot messages"""
    
    def __init__(self):
        self.include_status = True
        self.include_time = True
        self.include_session = True
        self.include_symbols = True
        self.compact_mode = False
    
    async def build_full_header(self):
        """Build full header with all components"""
        
        # Get all components
        status_text, _ = get_bot_status()
        time_text = get_current_time_display()
        session_text, _ = get_current_session()
        
        prices = await get_live_symbol_prices()
        symbols_text = format_symbol_prices(prices)
        
        # Build header
        header = f"""╔══════════════════════════════════════╗
║   🤖 ZEPIX TRADING BOT V5.0          ║
╠══════════════════════════════════════╣
║  📊 Status: {status_text:<23}║
║  {time_text:<35}║
║  📈 Session: {session_text:<23}║
║  💱 {symbols_text:<33}║
╚══════════════════════════════════════╝
"""
        return header
    
    async def build_compact_header(self):
        """Build compact header for long messages"""
        
        status_text, _ = get_bot_status()
        time_text = get_current_time_display()
        session_text, _ = get_current_session()
        
        prices = await get_live_symbol_prices()
        symbols_text = format_symbol_prices(prices)
        
        # Extract just the status
        status_short = status_text.split()[0]
        
        # Extract just the time
        time_short = time_text.split()[1]  # "14:35:22"
        
        # Extract just session name
        session_short = session_text.split('(')[0].strip()
        
        header = f"""🤖 {status_short} | 🕐 {time_short} | 📈 {session_short}
💱 {symbols_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return header
    
    async def build_minimal_header(self):
        """Build minimal header (just status + time)"""
        
        status_text, _ = get_bot_status()
        time_text = get_current_time_display()
        
        status_short = status_text.split()[0]
        time_short = time_text.split()[1]
        
        return f"🤖 {status_short} | 🕐 {time_short} GMT\n"
```

### Usage in Messages

```python
async def send_message_with_header(chat_id, content, header_type='full'):
    """Send message with sticky header"""
    
    header_builder = StickyHeader()
    
    if header_type == 'full':
        header = await header_builder.build_full_header()
    elif header_type == 'compact':
        header = await header_builder.build_compact_header()
    else:  # minimal
        header = await header_builder.build_minimal_header()
    
    full_message = header + "\n" + content
    
    await bot.send_message(
        chat_id=chat_id,
        text=full_message,
        parse_mode='HTML'
    )
```

---

## 🔄 AUTO-REFRESH MECHANISM

### Refresh Strategy

**Option 1: Edit Message (Recommended)**
```python
async def start_header_refresh(message_id, chat_id, interval=30):
    """Auto-refresh header every 30 seconds"""
    
    while True:
        await asyncio.sleep(interval)
        
        try:
            # Rebuild header with new data
            header_builder = StickyHeader()
            new_header = await header_builder.build_full_header()
            
            # Get current message content (without header)
            # ... extract content ...
            
            # Edit message with new header
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_header + "\n" + content,
                parse_mode='HTML'
            )
        
        except Exception as e:
            logger.error(f"Header refresh failed: {e}")
            break
```

**Option 2: New Message (Alternative)**
```python
# Send new message with updated header
# Delete old message
# This approach is more visible but creates message churn
```

### Smart Refresh Logic

```python
class HeaderRefreshManager:
    """Manage header refresh for multiple messages"""
    
    def __init__(self):
        self.active_refreshes = {}  # message_id -> task
        self.refresh_interval = 30  # seconds
    
    async def start_refresh(self, message_id, chat_id, content):
        """Start auto-refresh for a message"""
        
        # Create refresh task
        task = asyncio.create_task(
            self._refresh_loop(message_id, chat_id, content)
        )
        
        self.active_refreshes[message_id] = task
    
    async def _refresh_loop(self, message_id, chat_id, content):
        """Refresh loop for single message"""
        
        try:
            while True:
                await asyncio.sleep(self.refresh_interval)
                
                # Build new header
                header_builder = StickyHeader()
                new_header = await header_builder.build_full_header()
                
                # Edit message
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=new_header + "\n" + content,
                    parse_mode='HTML'
                )
        
        except asyncio.CancelledError:
            # Task cancelled, stop refresh
            pass
        except Exception as e:
            logger.error(f"Refresh error: {e}")
    
    def stop_refresh(self, message_id):
        """Stop refresh for a message"""
        
        if message_id in self.active_refreshes:
            task = self.active_refreshes[message_id]
            task.cancel()
            del self.active_refreshes[message_id]
    
    def stop_all_refreshes(self):
        """Stop all active refreshes"""
        
        for task in self.active_refreshes.values():
            task.cancel()
        
        self.active_refreshes.clear()

# Global instance
header_refresh_manager = HeaderRefreshManager()
```

---

## 📊 HEADER VARIATIONS BY MESSAGE TYPE

### 1. Status Message (Full Header)
```
╔══════════════════════════════════════╗
║   🤖 ZEPIX TRADING BOT V5.0          ║
╠══════════════════════════════════════╣
║  📊 Status: ACTIVE ✅                ║
║  🕐 Time: 14:35:22 GMT               ║
║  📈 Session: LONDON (Active)         ║
║  💱 EURUSD: 1.0825 | GBPUSD: 1.2645  ║
╚══════════════════════════════════════╝

[Status content here...]
```

### 2. Trade Notification (Compact Header)
```
🤖 ACTIVE ✅ | 🕐 14:35 GMT | 📈 LONDON
💱 EUR:1.0825 GBP:1.2645
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 TRADE OPENED
[Trade details...]
```

### 3. Quick Response (Minimal Header)
```
🤖 ACTIVE ✅ | 🕐 14:35 GMT

Command executed successfully!
```

### 4. Error Message (Alert Header)
```
🚨 ERROR ALERT 🚨
🕐 14:35:22 GMT

[Error details...]
```

---

## 💾 HEADER CACHING

### Cache Strategy

```python
class HeaderCache:
    """Cache header components to reduce computation"""
    
    def __init__(self, cache_duration=5):
        self.cache_duration = cache_duration  # seconds
        self.cache = {}
        self.cache_timestamps = {}
    
    async def get_component(self, component_name, builder_func):
        """Get cached component or rebuild"""
        
        from datetime import datetime, timedelta
        
        # Check if cached and still valid
        if component_name in self.cache:
            timestamp = self.cache_timestamps[component_name]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_duration):
                return self.cache[component_name]
        
        # Rebuild component
        value = await builder_func()
        
        # Update cache
        self.cache[component_name] = value
        self.cache_timestamps[component_name] = datetime.now()
        
        return value

# Global cache
header_cache = HeaderCache(cache_duration=5)

# Usage:
async def get_cached_symbol_prices():
    """Get symbol prices (cached for 5 seconds)"""
    return await header_cache.get_component(
        'symbol_prices',
        get_live_symbol_prices
    )
```

---

## 🎯 USER CUSTOMIZATION

### Customizable Options

```python
class UserHeaderPreferences:
    """Store user preferences for header display"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = self._load_preferences()
    
    def _load_preferences(self):
        """Load from database or default"""
        return {
            'show_time': True,
            'show_session': True,
            'show_symbols': True,
            'show_status': True,
            'header_style': 'full',  # full, compact, minimal
            'symbols': ['EURUSD', 'GBPUSD', 'USDJPY'],  # Custom symbols
            'show_price_changes': True,
            'timezone': 'GMT',  # User can choose timezone
        }
    
    def get_header_style(self):
        """Get preferred header style"""
        return self.preferences['header_style']
    
    def set_header_style(self, style):
        """Set header style"""
        if style in ['full', 'compact', 'minimal']:
            self.preferences['header_style'] = style
            self._save_preferences()
    
    def get_symbols(self):
        """Get symbols to display"""
        return self.preferences['symbols']
    
    def set_symbols(self, symbols):
        """Set custom symbols"""
        self.preferences['symbols'] = symbols
        self._save_preferences()
```

### Customization Menu

```
⚙️ HEADER SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━

Current Style: FULL

┌─────────────────────────────────────┐
│  📐 Full Header│  📦 Compact        │
├─────────────────────────────────────┤
│  📝 Minimal   │                     │
├─────────────────────────────────────┤
│  💱 Symbol Settings                 │
├─────────────────────────────────────┤
│  🔄 Toggle Components               │
├─────────────────────────────────────┤
│  🏠 Main Menu                       │
└─────────────────────────────────────┘
```

---

## 📋 IMPLEMENTATION CHECKLIST

### Core Components ✅
- [ ] Clock component with GMT time
- [ ] Session detector with overlap support
- [ ] Live symbol price fetcher
- [ ] Bot status indicator
- [ ] Header template builder

### Advanced Features ✅
- [ ] Auto-refresh mechanism
- [ ] Header caching system
- [ ] User customization
- [ ] Multiple header styles (full/compact/minimal)
- [ ] Price change indicators

### Integration ✅
- [ ] Integrate with all command handlers
- [ ] Add to notification system
- [ ] Add to error messages
- [ ] Add to status updates

---

## 🔧 TECHNICAL IMPLEMENTATION

### Core Header Class

```python
"""
Sticky Header System
Complete implementation
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio
import logging

logger = logging.getLogger(__name__)

class StickyHeaderSystem:
    """Complete sticky header system"""
    
    def __init__(self, mt5_client, plugin_manager, trading_engine):
        self.mt5_client = mt5_client
        self.plugin_manager = plugin_manager
        self.trading_engine = trading_engine
        
        # Components
        self.session_manager = SessionManager()
        self.price_fetcher = PriceFetcher(mt5_client)
        self.cache = HeaderCache()
        self.refresh_manager = HeaderRefreshManager()
        
        # Default config
        self.default_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
    
    async def build_header(
        self, 
        style: str = 'full',
        custom_symbols: Optional[List[str]] = None
    ) -> str:
        """
        Build header based on style.
        
        Args:
            style: 'full', 'compact', or 'minimal'
            custom_symbols: Custom symbol list (None = use default)
        
        Returns:
            Formatted header string
        """
        
        if style == 'full':
            return await self._build_full_header(custom_symbols)
        elif style == 'compact':
            return await self._build_compact_header(custom_symbols)
        else:
            return await self._build_minimal_header()
    
    async def _build_full_header(self, symbols=None):
        """Build full header"""
        
        # Get components (use cache)
        status = await self.cache.get_component(
            'status',
            self._get_bot_status
        )
        
        time_str = self._get_current_time()
        
        session = await self.cache.get_component(
            'session',
            self.session_manager.get_current_session
        )
        
        prices = await self.cache.get_component(
            'prices',
            lambda: self.price_fetcher.get_prices(symbols or self.default_symbols)
        )
        
        # Format
        header = f"""╔══════════════════════════════════════╗
║   🤖 ZEPIX TRADING BOT V5.0          ║
╠══════════════════════════════════════╣
║  📊 Status: {status:<23}║
║  🕐 Time: {time_str}           ║
║  📈 Session: {session:<23}║
║  💱 {prices:<33}║
╚══════════════════════════════════════╝
"""
        return header
    
    async def _build_compact_header(self, symbols=None):
        """Build compact header"""
        
        status = await self._get_bot_status()
        time_str = self._get_current_time()
        session = await self.session_manager.get_current_session()
        prices = await self.price_fetcher.get_prices(symbols or self.default_symbols)
        
        # Shorten
        status_short = status.split()[0]
        time_short = time_str.split()[0]  # Just HH:MM
        session_short = session.split('(')[0].strip()
        
        return f"""🤖 {status_short} | 🕐 {time_short} | 📈 {session_short}
💱 {prices}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    async def _build_minimal_header(self):
        """Build minimal header"""
        
        status = await self._get_bot_status()
        time_str = self._get_current_time()
        
        status_short = status.split()[0]
        
        return f"🤖 {status_short} | 🕐 {time_str} GMT\n"
    
    async def _get_bot_status(self) -> str:
        """Get current bot status"""
        
        mt5_ok = self.mt5_client and self.mt5_client.is_connected()
        v3_on = self.plugin_manager.is_active('v3')
        v6_on = self.plugin_manager.is_active('v6')
        paused = self.trading_engine.is_paused()
        
        if not mt5_ok:
            return "ERROR ❌"
        if paused:
            return "PAUSED ⏸️"
        if v3_on and v6_on:
            return "ACTIVE ✅"
        if v3_on or v6_on:
            return "PARTIAL ⚠️"
        return "INACTIVE ⛔"
    
    def _get_current_time(self) -> str:
        """Get formatted current time"""
        return datetime.utcnow().strftime("%H:%M:%S")
```

---

**STATUS:** Sticky Header Design Complete ✅

