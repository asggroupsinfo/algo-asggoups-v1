# DEVIN: MANDATE 23 EXECUTION BRIEF

## 🎯 MISSION
Build **production-ready intelligent trading bot** with complete autonomous decision-making.

---

## 📋 WHAT TO BUILD

### **1. INTELLIGENT ENTRY (V3 & V6)**
When Pine sends `BULLISH_ENTRY` / `BEARISH_ENTRY`:
- Place **Order A** (Main, targets TP3)
- Place **Order B** (Quick profit, targets TP1 or fixed profit)
- Use Pine's TP1, TP2, TP3, SL from payload
- Smart lot sizing (risk-based calculation)

### **2. TP MANAGEMENT (Intelligent Profit Booking)**
- **TP1 Hit:** Check Pine updates (Trend, ADX, Confidence). If strong → hold for TP2. If weak → close 50%.
- **TP2 Hit:** Close 40%, trail SL to TP1, monitor for TP3.
- **TP3 Hit:** Close all.

### **3. SL HUNTING & RE-ENTRY**
When SL hits:
- Activate SL Hunting
- Monitor for 70% price recovery
- Check Pine conditions (Trend, ADX, Confidence)
- If all good → Re-enter
- **Separate hunting for Order A and Order B**

### **4. EXIT SIGNAL INTELLIGENCE**
When Pine sends `EXIT` signal:
- Check current profit
- Check Pine updates
- **Decision:**
  - Big profit + strong trend → Hold
  - Small profit + weak trend → Close immediately
  - Medium profit → Close 50%, protect rest

### **5. TELEGRAM BOT SEPARATION**
Split into 3 bots:
- **Controller Bot:** Commands (/start, /stop, /settings)
- **Notification Bot:** Trade alerts only
- **Analytics Bot:** Stats (/stats, /report)

### **6. LIVE SIMULATION TESTING**
Create test suite:
- Test 1: Entry → TP1 → TP2 → TP3
- Test 2: Entry → SL → 70% Recovery → Re-entry
- Test 3: TP1 → Weak conditions → Profit protection
- Test 4: Exit signal intelligence
- Test 5: Telegram separation

**ALL TESTS MUST PASS 100%**

---

## 🔧 HOW TO EXECUTE

1. **Use DeepThink MCP** to plan complex logic
2. **Scan existing code** (V3 & V6 plugins, Telegram)
3. **Implement features** one by one
4. **Test each feature** in simulation
5. **Fix bugs** immediately if tests fail
6. **Document** with code evidence

---

## ✅ DELIVERABLES

1. **Code:** Modified V3 (3 files), V6 (4 files), Telegram (3 files)
2. **Tests:** `test_live_simulation.py` with 100% pass
3. **Report:** `23_INTELLIGENT_TRADING_IMPLEMENTATION_REPORT.md`
4. **Proof:** Screenshots of 3 Telegram bots, test results

---

## 🚨 SUCCESS CRITERIA

- ✅ Entry places Order A + B with Pine TP/SL
- ✅ TP management with intelligent decisions
- ✅ SL Hunting with 70% recovery
- ✅ Exit intelligence (checks conditions)
- ✅ Smart lot sizing
- ✅ Telegram bots separated (3 running)
- ✅ Tests: 100% PASS

---

**Full details:** `23_COMPLETE_BOT_INTELLIGENCE.md`

**START NOW.**
