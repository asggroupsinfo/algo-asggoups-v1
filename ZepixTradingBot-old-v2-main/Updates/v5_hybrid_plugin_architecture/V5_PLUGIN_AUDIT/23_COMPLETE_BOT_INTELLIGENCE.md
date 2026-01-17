# MANDATE 23: COMPLETE BOT INTELLIGENCE & PRODUCTION READINESS

**Date:** 2026-01-17  
**Priority:** CRITICAL - PRODUCTION DEPLOYMENT  
**Type:** Full System Integration & Testing  
**Objective:** Implement complete intelligent trading logic (Entry, TP Management, SL Hunting, Re-entry, Profit Protection) for both V3 and V6, verify Telegram bot separation, and achieve 100% live simulation test pass rate.

---

## 🎯 MISSION OVERVIEW

Build a **fully autonomous, intelligent trading bot** that:
1. Executes trades based on Pine Script alerts (V3 & V6)
2. Manages multi-level TP (TP1, TP2, TP3) with intelligent profit booking
3. Implements SL Hunting with 70% recovery re-entry
4. Uses real-time Pine updates (Trend, ADX, Confidence) for decision-making
5. Separates Telegram bots (Controller, Notifications, Analytics)
6. Passes 100% live simulation tests

---

## 📋 PART 1: INTELLIGENT TRADE EXECUTION

### **1.1 Entry Signal Processing (V3 & V6)**

**Requirements:**
- When `BULLISH_ENTRY` or `BEARISH_ENTRY` alert arrives:
  - Parse TP1, TP2, TP3 from Pine payload
  - Place **Order A** (Main position targeting TP3)
  - Place **Order B** (Quick profit at fixed profit level OR breakeven SL)
  
**Order A Configuration:**
- Entry: Market order
- SL: From Pine payload (`alert.sl`)
- TP: TP3 (for swing moves)
- Lot Size: Smart lot calculation (risk-based)

**Order B Configuration:**
- Entry: Market order (same time as Order A)
- SL: From Pine payload (`alert.sl`)
- TP: Fixed profit (e.g., 50% of TP1-Entry distance) OR TP1
- Lot Size: 50% of Order A lot size

**Code Location:**
- V3: `Trading_Bot/src/logic_plugins/v3_combined/combinedlogic_*.py`
- V6: `Trading_Bot/src/logic_plugins/v6_price_action_*/plugin.py`

**Implementation:**
```python
async def process_entry_signal(self, alert):
    # Parse Pine data
    entry_price = alert.price
    sl = alert.sl
    tp1, tp2, tp3 = alert.tp1, alert.tp2, alert.tp3
    
    # Smart lot calculation
    base_lot = await self.calculate_risk_based_lot(entry_price, sl)
    
    # Place Order A (Main)
    order_a = await self.place_order_a(
        symbol=alert.ticker,
        direction=alert.direction,
        lot=base_lot,
        sl=sl,
        tp=tp3  # Target big move
    )
    
    # Place Order B (Quick profit)
    order_b = await self.place_order_b(
        symbol=alert.ticker,
        direction=alert.direction,
        lot=base_lot * 0.5,
        sl=sl,
        tp=tp1  # Quick exit
    )
    
    # Store trade context for monitoring
    await self.store_trade_context(order_a, order_b, {
        'tp1': tp1, 'tp2': tp2, 'tp3': tp3,
        'entry': entry_price, 'sl': sl
    })
```

---

### **1.2 TP Management (Intelligent Profit Booking)**

**TP1 Hit Logic:**
When Order B hits TP1:
1. **Monitor Price** for TP2 opportunity
2. **Check Real-time Pine Updates:**
   - Trend still aligned?
   - ADX still strong?
   - Confidence score still high?
3. **Decision:**
   - If ALL conditions favorable → Keep Order A running, target TP2
   - If ANY condition weakens → Close 50% of Order A, secure profit

**TP2 Hit Logic:**
When price reaches TP2:
1. **Close 40% of Order A** (profit booking)
2. **Trail SL to TP1** (protect remaining 60%)
3. **Monitor for TP3:**
   - Check Pine updates
   - If trend reverses → Exit remaining
   - If trend continues → Let it run to TP3

**TP3 Hit Logic:**
- Close all remaining positions
- Log final profit

**Implementation:**
```python
async def monitor_tp_levels(self, trade_id):
    context = await self.get_trade_context(trade_id)
    current_price = await self.get_current_price(context['symbol'])
    
    # TP1 Check
    if self.is_tp_hit(current_price, context['tp1'], context['direction']):
        # Get latest Pine data
        latest_trend = await self.get_latest_trend_from_pine()
        latest_adx = await self.get_latest_adx_from_pine()
        latest_conf = await self.get_latest_confidence_from_pine()
        
        # Intelligent decision
        if self.is_favorable_for_tp2(latest_trend, latest_adx, latest_conf):
            self.logger.info("TP1 hit, conditions good, targeting TP2")
            # Keep running
        else:
            self.logger.info("TP1 hit, conditions weak, booking 50% profit")
            await self.close_partial(trade_id, percent=50)
    
    # TP2 Check
    if self.is_tp_hit(current_price, context['tp2'], context['direction']):
        await self.close_partial(trade_id, percent=40)
        await self.trail_sl_to_tp1(trade_id)
    
    # TP3 Check
    if self.is_tp_hit(current_price, context['tp3'], context['direction']):
        await self.close_all(trade_id)
```

---

### **1.3 SL Hunting & Re-entry (70% Recovery)**

**SL Hit Detection:**
When Order A or Order B hits SL:
1. **Activate SL Hunting Mode** for that specific order
2. **Monitor Price Recovery:**
   - Calculate 70% recovery level: `recovery_price = sl + (entry - sl) * 0.70`
3. **Re-entry Conditions:**
   - Price recovers to 70% level
   - Trend still aligned (check Pine)
   - ADX still strong
   - Confidence still acceptable

**Separate SL Hunting for Order A & B:**
- Order A SL Hunting: Re-enter with same lot size, target original TP3
- Order B SL Hunting: Re-enter with 50% lot, target original TP1

**Implementation:**
```python
async def handle_sl_hit(self, order_id, order_type):
    context = await self.get_trade_context_by_order(order_id)
    
    # Activate SL Hunting
    recovery_price = self.calculate_70_percent_recovery(
        entry=context['entry'],
        sl=context['sl'],
        direction=context['direction']
    )
    
    self.logger.info(f"SL Hit for {order_type}, activating SL Hunting. Recovery: {recovery_price}")
    
    # Start monitoring
    await self.start_sl_hunting_monitor(
        symbol=context['symbol'],
        recovery_price=recovery_price,
        order_type=order_type,
        original_context=context
    )

async def sl_hunting_monitor(self, hunt_id):
    hunt_data = await self.get_sl_hunt_data(hunt_id)
    current_price = await self.get_current_price(hunt_data['symbol'])
    
    if self.is_price_recovered(current_price, hunt_data['recovery_price'], hunt_data['direction']):
        # Check Pine conditions
        trend_ok = await self.check_trend_from_pine()
        adx_ok = await self.check_adx_from_pine()
        conf_ok = await self.check_confidence_from_pine()
        
        if trend_ok and adx_ok and conf_ok:
            self.logger.info("70% recovery + conditions met, re-entering")
            await self.execute_reentry(hunt_data)
        else:
            self.logger.info("70% recovery but conditions weak, skipping re-entry")
```

---

### **1.4 Exit Signal Processing**

**When `EXIT_BULLISH` or `EXIT_BEARISH` alert arrives:**
1. **Check Current Price**
2. **Check Trend** (from Pine)
3. **Check ADX** (from Pine)
4. **Check Confidence** (from Pine)
5. **Decision:**
   - If price near TP2/TP3 AND conditions still strong → Ignore exit, let it run
   - If price near entry AND conditions weak → Close immediately
   - If in profit but conditions deteriorating → Close 50%, trail SL

**Implementation:**
```python
async def process_exit_signal(self, alert):
    positions = await self.get_open_positions(alert.ticker)
    
    for pos in positions:
        current_profit_pips = self.calculate_profit_pips(pos)
        
        # Get Pine updates
        trend = await self.get_latest_trend()
        adx = await self.get_latest_adx()
        conf = await self.get_latest_confidence()
        
        # Intelligent exit decision
        if current_profit_pips > 50 and self.is_strong_trend(trend, adx, conf):
            self.logger.info("Exit signal but strong trend, holding position")
            continue
        elif current_profit_pips < 10:
            self.logger.info("Exit signal + small profit, closing immediately")
            await self.close_position(pos['id'])
        else:
            self.logger.info("Exit signal + moderate profit, closing 50%")
            await self.close_partial_position(pos['id'], 50)
```

---

## 📋 PART 2: SMART LOT SIZING & PROFIT PROTECTION

### **2.1 Smart Lot Calculation**

**Risk-Based Formula:**
```python
def calculate_smart_lot(self, entry, sl, risk_percent=1.0):
    account_balance = self.get_account_balance()
    risk_amount = account_balance * (risk_percent / 100)
    
    pip_value = self.get_pip_value(symbol)
    sl_pips = abs(entry - sl) / pip_value
    
    lot_size = risk_amount / (sl_pips * pip_value)
    
    # Apply limits
    max_lot = self.config.get('max_lot_size', 0.15)
    min_lot = self.config.get('min_lot_size', 0.01)
    
    return max(min_lot, min(lot_size, max_lot))
```

### **2.2 Profit Protection**

**Trailing SL Logic:**
- When TP1 hit → Move SL to breakeven
- When TP2 hit → Move SL to TP1
- When in 50+ pips profit → Trail SL 20 pips behind price

**Breakeven Protection:**
- After 20 pips profit → Move SL to entry + 5 pips (secure small profit)

---

## 📋 PART 3: TELEGRAM BOT SEPARATION

### **3.1 Current Issue**

All Telegram functionality is in one bot (Controller). Need to separate into 3 bots:

| Bot | Purpose | Commands |
|-----|---------|----------|
| **Controller Bot** | Bot control, settings, manual trades | /start, /stop, /settings, /status, /manualtrade |
| **Notification Bot** | Trade notifications, alerts | (No commands, only sends notifications) |
| **Analytics Bot** | Performance stats, reports | /stats, /report, /performance, /trades |

### **3.2 Implementation**

**File Structure:**
```
Trading_Bot/src/telegram/
├── controller_bot.py      # Bot control
├── notification_bot.py    # Notifications only
├── analytics_bot.py       # Stats & reports
└── telegram_manager.py    # Coordinates all 3
```

**Verification:**
- Run all 3 bots simultaneously
- Test that Controller commands work
- Test that Notifications are sent separately
- Test that Analytics commands work
- Confirm no overlap

---

## 📋 PART 4: LIVE SIMULATION TESTING

### **4.1 Test Scenarios**

Create comprehensive test suite covering:

**Test 1: Entry → TP1 → TP2 → TP3 (Full Win)**
- Inject BULLISH_ENTRY alert
- Simulate price moving to TP1
- Verify Order B closes
- Verify Order A continues
- Simulate price to TP2
- Verify partial close (40%)
- Simulate price to TP3
- Verify full close

**Test 2: Entry → SL Hit → 70% Recovery → Re-entry**
- Inject BULLISH_ENTRY
- Simulate price hitting SL
- Verify SL Hunting activates
- Simulate 70% recovery
- Verify re-entry executes

**Test 3: Entry → TP1 → Weak Conditions → Exit**
- Inject BULLISH_ENTRY
- Simulate TP1 hit
- Inject weak Pine updates (low ADX, bearish trend)
- Verify bot closes 50% for profit protection

**Test 4: Exit Signal Intelligence**
- Inject BULLISH_ENTRY
- Simulate 60 pips profit
- Inject EXIT_BULLISH with strong trend
- Verify bot holds position (ignores exit)

**Test 5: Telegram Bot Separation**
- Send /status to Controller Bot
- Verify response
- Trigger trade notification
- Verify Notification Bot sends alert
- Send /stats to Analytics Bot
- Verify report generation

### **4.2 Test Execution**

**Command:**
```bash
cd Trading_Bot
pytest tests/test_live_simulation.py -v --tb=short
```

**Success Criteria:**
- ALL tests must PASS (100%)
- No errors in logs
- All 3 Telegram bots respond correctly

---

## 📋 PART 5: DELIVERABLES

### **5.1 Code Changes**

**Modified Files:**
1. V3 Plugins (3 files): Entry, TP management, SL hunting
2. V6 Plugins (4 files): Entry, TP management, SL hunting
3. Telegram bots (3 files): Separation implementation
4. Test suite (1 file): Live simulation tests

### **5.2 Documentation**

**Create:**
1. `23_INTELLIGENT_TRADING_IMPLEMENTATION_REPORT.md`
   - All features implemented
   - Code snippets (before/after)
   - Test results (100% pass proof)
   - Telegram bot separation proof

2. Update `Trading_Bot_Documentation/COMPLETE_TRADING_FLOW.md`
   - Entry → TP Management → SL Hunting → Re-entry flow
   - Decision trees with Pine data integration

### **5.3 Test Report**

**File:** `23_LIVE_SIMULATION_TEST_RESULTS.md`

**Include:**
- Test execution logs
- Screenshots of Telegram bots (3 separate)
- Trade execution proof (simulated)
- 100% pass rate confirmation

---

## ✅ ACCEPTANCE CRITERIA

**Task is COMPLETE only when:**
1. ✅ Entry logic places Order A + Order B with Pine TP/SL
2. ✅ TP1/TP2/TP3 management with intelligent decisions
3. ✅ SL Hunting with 70% recovery re-entry (separate for A & B)
4. ✅ Exit signal intelligence (checks price, trend, ADX, conf)
5. ✅ Smart lot sizing implemented
6. ✅ Profit protection (trailing SL, breakeven)
7. ✅ Telegram bots separated (3 bots running)
8. ✅ Live simulation tests: 100% PASS
9. ✅ Documentation complete with evidence

---

## 🚨 CRITICAL INSTRUCTIONS

1. **Use DeepThink MCP** for complex logic planning
2. **Scan ALL existing code** before making changes
3. **Test EVERY feature** in live simulation mode
4. **Fix bugs immediately** if any test fails
5. **Document EVERYTHING** with code evidence
6. **Zero tolerance** for incomplete features

---

**START EXECUTION NOW. This is the final step to production readiness.**
